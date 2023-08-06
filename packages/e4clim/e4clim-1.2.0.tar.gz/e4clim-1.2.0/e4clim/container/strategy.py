"""Strategy base definitions."""
from abc import ABC, abstractmethod
from collections import OrderedDict
from orderedset import OrderedSet
from pathlib import Path
import pickle
import typing as tp
import xarray as xr
from e4clim import context
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import ContainerBase
from .result_data_source import Feature


class StrategyBase(ContainerBase):
    """Abstract strategy."""

    #: Data sources the strategy depends on.
    _data_sources: e4tp.ParsingDataSourcesType

    #: Variable names for each stage.
    _stage_variable_component_names: e4tp.StageToVCNMutableType

    _parent: 'context.context_result.ContextResult'

    def __init__(self,
                 parent: 'context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, task_names:
                 e4tp.StrIterableType = OrderedSet(), **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent result context.
        :param name: Name.
        :param cfg: Configuration.

        .. seealso:: Strategy builder:
          :py:class:`e4clim.build.strategy.BuilderStrategy`
        """
        #: Data sources the strategy depends on.
        self._data_sources = OrderedDict()

        #: Variable names for each stage.
        self._stage_variable_component_names = OrderedDict()

        # Initialize as container with output variable as parent
        kwargs.update({
            'name': name, 'cfg': cfg, 'parent': parent,
            'task_names': task_names})
        super(StrategyBase, self).__init__(**kwargs)

    @property
    def parent(self) -> 'context.context_result.ContextResult':
        return self._parent

    @property
    def data_sources(self) -> e4tp.ParsingDataSourcesType:
        return self._data_sources

    @property
    def stage_variable_component_names(self) -> e4tp.StageToVCNMutableType:
        return self._stage_variable_component_names


class EstimatorBase(StrategyBase, ABC):
    """Estimator abstract base class. Requires :py:meth:`fit` and
    :py:meth:`predict` methods to be implemented."""

    #: Coefficients to be fitted
    coef: tp.Any

    def __init__(self,
                 parent: 'context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs):
        """Estimator constructor.

        :param parent: Parent result manager.
        :param name: Strategy name.
        :param cfg: Estimator configuration.
        """

        # Try updating task names in keyword arguments if possible
        kwargs.update({'parent': parent, 'name': name, 'cfg': cfg})
        # Initialize as container
        super(EstimatorBase, self).__init__(**kwargs)

    @abstractmethod
    def fit(self, data_src_in: Feature, data_src_out: Feature,
            **kwargs) -> None:
        """Fit estimator abstract method."""
        pass

    @abstractmethod
    def predict(self, data_src_in: Feature, **kwargs) -> e4tp.DatasetType:
        """Predict with estimator abstract method."""
        pass

    def get_estimator_postfix(self, **kwargs) -> str:
        """Default implementation: get an empty postfix string.

        :returns: Postfix.
        """
        return ''

    def get_fit_postfix(self, **kwargs) -> str:
        """Get fit postfix (component, feature, estimator).

        :returns: Postfix.
        """
        # Feature postfix
        feature_postfix = self.parent.features['fit'].get_data_postfix(
            **kwargs)

        # Output data postfix
        data_src = self.parent.extractors['output'].data_sources[
            'output']
        output_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Estimator postfix
        estimator_postfix = self.get_estimator_postfix(**kwargs)

        # Fit postfix
        fit_postfix = '{}{}{}'.format(
            feature_postfix, output_postfix, estimator_postfix)

        return fit_postfix

    def get_fit_path(self, makedirs: bool = True, **kwargs) -> Path:
        """Get fit filepath.

        :param makedirs: Make directories if needed.

        :returns: Filepath.
        """
        filename = '{}_estimator{}'.format(
            self.parent.parent.name, self.get_fit_postfix(**kwargs))
        data_dir = self.parent.parent.get_data_directory(
            makedirs=makedirs, **kwargs)
        filepath = Path(data_dir, filename)

        return filepath

    def read(self, **kwargs) -> None:
        """Read estimator with pickle."""
        try:
            # Try to read as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            self.info('Reading {} {} {} estimator from {}'.format(
                self.parent.parent.name, self.parent.name, self.name,
                filepath))
            self.coef = xr.load_dataarray(filepath)
        except FileNotFoundError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            self.info('Reading {} {} {} estimator from {}'.format(
                self.parent.parent.name, self.parent.name, self.name,
                filepath))
            with open(filepath, 'rb') as f:
                self.coef = pickle.load(f)

    def write(self, **kwargs) -> None:
        """Write estimator with pickle."""
        try:
            # Try to write as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            self.info('Writing {} {} {} estimator to {}'.format(
                self.parent.parent.name, self.parent.name, self.name,
                filepath))
            self.coef.to_netcdf(filepath)
        except AttributeError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            self.info('Writing {} {} {} estimator to {}'.format(
                self.parent.parent.name, self.parent.name, self.name,
                filepath))
            # Otherwise, write as pickle
            with open(filepath, 'wb') as f:
                pickle.dump(self.coef, f)


class ExtractorBase(StrategyBase, ABC):
    """Extractor base class."""

    #: Estimation stages.
    stages: set

    #: Transformation flag. If `True`, no extraction is performed.
    no_extraction: bool

    #: Variable names.
    variable_names: e4tp.StrIterableType

    get_data_path: tp.Optional[tp.Callable[..., Path]] = None

    def __init__(self,
                 parent: 'context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None,
                 variable_names: e4tp.StrIterableType = None,
                 stages: e4tp.StrIterableType = {'fit', 'predict', 'output'},
                 **kwargs) -> None:
        """Extractor constructor.

        :param parent: Parent result manager.
        :param name: Strategy name.
        :param cfg: Estimator configuration.
        :param variable_names: Name(s) of variable(s) to be extracted.
        :param stages: Stages at which extraction is performed.
        """
        #: Estimation stages.
        self.stages = set(stages)

        #: Transformation flag. If `True`, no extraction is performed.
        self.no_extraction = False

        # Initialize as container
        kwargs.update({'parent': parent, 'name': name, 'cfg': cfg})
        super(ExtractorBase, self).__init__(**kwargs)

        self.set_variable_names(variable_names)

    @abstractmethod
    def transform(self, **kwargs) -> e4tp.DatasetType:
        """Abstract transform method."""
        ...

    def set_variable_names(
            self, variable_names: e4tp.StrIterableType = None) -> None:
        """Set variable names.

        :param variable_names: Name(s) of variable(s) to be extracted.
        """
        self.variable_names = tools.ensure_collection(
            variable_names, OrderedSet) or OrderedSet()

    def get_extractor_postfix(self, **kwargs) -> str:
        """Default implementation: get an empty extractor postfix string.

        :returns: Postfix.
        """
        return ''


class ModifierBase(ExtractorBase, ABC):
    """Modifier base class. Differs from :py:class:`ExtractorBase
    by the signature of the :py:attr:`transform` method only."""

    @abstractmethod
    def transform(self, ds: xr.Dataset = None,
                  **kwargs) -> e4tp.DatasetType:
        """Abstract transform method."""
        ...


class DefaultExtractor(ExtractorBase):
    """Default extractor implementation.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self,
                 parent: 'context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Default extractor constructor.

        :param parent: Parent result manager.
        :param name: Strategy name.
        :param cfg: Estimator configuration.
        """
        super(DefaultExtractor, self).__init__(
            parent=parent, name=name, cfg=cfg,
            variable_names=parent.result_name, **kwargs)

        # Flag that no transformation is to be performed, unless explicitly
        # asked with `'write'` entry of configuration (for instance if
        # modifier active)
        self.no_extraction = not self.cfg.get('write')

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Default transform: return equal or modified data source
        for the component and all variables and prevent writing.

        :param stage: Modeling stage: `'fit'`, `'predict'`, or `'output'`.

        :returns: Dataset.

        .. warning:: If a modifier is active, its 'transform' method
          replaces any such method present in :py:obj:`kwargs['transform']`.
        """
        assert stage is not None, '"stage" argument is not optional here'

        if self.parent.modifier is not None:
            if (hasattr(self.parent.modifier.cfg, 'stage') and
                    (self.parent.modifier.cfg['stage'] != stage)):
                pass
            else:
                # Add modifier transformation to keyword arguments
                kwargs['transform'] = self.parent.modifier.transform

        # Get data
        data_src = self.data_sources[stage]
        data = data_src.get_data(**kwargs)

        ds = {}
        for variable_name, da in data.items():
            if isinstance(da, xr.DataArray) or isinstance(da, xr.Dataset):
                # Try to select component
                try:
                    da = da.sel(component=self.parent.parent.component_name)
                except (ValueError, KeyError):
                    pass

            # Add data array to dataset
            ds[variable_name] = da

        # Prevent writing if same data
        if self.no_extraction:
            self.parent.features[stage].task_mng['write__' + stage] = False

        # Return equal data for component
        return ds


# Alias default feature and output extractor
DefaultFeatureExtractor = DefaultOutputExtractor = DefaultExtractor
