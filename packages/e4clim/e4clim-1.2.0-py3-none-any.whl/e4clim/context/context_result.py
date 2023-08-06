from collections import OrderedDict
from pathlib import Path
import typing as tp
from e4clim.container.single_data_source import SingleDataSourceBase
from e4clim.container.result_data_source import (
    Feature, Prediction, ResultDataSourceBase)
from e4clim.container.strategy import (
    EstimatorBase, ExtractorBase, ModifierBase, StrategyBase)
from e4clim import context
import e4clim.typing as e4tp

ExtractorsType = tp.MutableMapping[str, ExtractorBase]
FeaturesType = tp.MutableMapping[str, Feature]
StrategiesType = tp.MutableMapping[str, StrategyBase]


class ContextResult(SingleDataSourceBase):
    """Manager for prediction results or output variables associated with a
    component."""

    #: Data sources.
    data_sources: e4tp.ParsingDataSourcesType

    #: Estimator.
    estimator: tp.Optional[EstimatorBase]

    #: Stage to extractor mapping.
    extractors: ExtractorsType

    #: Feature extractor
    feature_extractor: tp.Optional[ExtractorBase]

    #: Features for each stage. Used in feature-extraction cases.
    features: FeaturesType

    #: Modifier.
    modifier: tp.Optional[ModifierBase]

    #: Output extractor
    output_extractor: tp.Optional[ExtractorBase]

    # Precise types of of sub-class attributes
    _parent: 'context.context_component.ContextComponent'

    #: Prediction result data source.
    prediction: tp.Optional['Prediction']

    #: Result data source. Either :py:attr:`prediction`
    #:  or :py:attr:`features['output']`.
    result: ResultDataSourceBase

    #: Result name.
    _result_name: str

    #: Strategies.
    strategies: StrategiesType

    def __init__(self, parent:
                 'context.context_component.ContextComponent',
                 name: str, cfg: e4tp.CfgType, **kwargs) -> None:
        """Initialize result context.

        :param parent: Parent component context.
        :param name: Name.
        :param cfg: Configuration.

        .. seealso:: Result manager builder:
          :py:class:`e4clim.build.result_manager.BuilderContextResult`
        """
        super(ContextResult, self).__init__(parent, name, cfg=cfg, **kwargs)

        result_name = self.cfg.get('result_name')
        if result_name is not None:
            self._result_name = str(result_name)
        else:
            self._result_name = self.name

        self.strategies = OrderedDict()
        self.data_sources = OrderedDict()
        self.features = OrderedDict()
        self.extractors = OrderedDict()

        self.estimator = None
        self.feature_extractor = None
        self.modifier = None
        self.output_extractor = None
        self.prediction = None

    @property
    def parent(self) -> 'context.context_component.ContextComponent':
        return self._parent

    @property
    def result_name(self) -> str:
        return self._result_name

    def get_data(self, **kwargs) -> e4tp.DatasetType:
        """Get output from prediction if :py:attr:`estimator` is not `None`,
        or directly from (extracted) output data source, and store it in
        :py:attr:`result`.

        :returns: Dataset :py:attr:`data`.
        """
        # # Make sure that variable names not in keyword arguments
        # if 'variable_component_names' in kwargs:
        #     del kwargs['variable_component_names']
        return self.result.get_data(**kwargs)

    def get_data_postfix(self, **kwargs) -> str:
        """Get prediction postfix.

        :returns: Postfix.
        """
        return self.result.get_data_postfix(**kwargs)

    def get_data_path(self, variable_name: str = None,
                      makedirs: bool = True, **kwargs) -> Path:
        """Get data-source filepath using extractor "get_data_path"
        method if possible.

        :param variable_name: Data variable.
        :param makedirs: Make directories if needed.

        :returns: Filepath.
        """
        return self.result.get_data_path(
            variable_name=variable_name, makedirs=makedirs)
