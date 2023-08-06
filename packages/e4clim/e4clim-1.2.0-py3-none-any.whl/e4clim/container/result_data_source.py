from collections import OrderedDict
from orderedset import OrderedSet
from pathlib import Path
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools
from .parsing_single_data_source import ParsingSingleDataSourceBase


class ResultDataSourceBase(ParsingSingleDataSourceBase):
    """Base result data."""

    _parent: 'e4clim.context.context_result.ContextResult'

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str = None, variable_names: e4tp.StrIterableType = None,
                 task_names: e4tp.StrIterableType = None, **kwargs) -> None:
        """Initialize feature as data source.

        :param parent: Result manager to which data is associated.
        :param name: Data name.
        :param variable_names: Name(s) of variable(s) composing dataset.
        :param task_names: Names of potential tasks for container to perform.
        """
        # Set components per variable
        variable_names_safe = tools.ensure_collection(
            variable_names, OrderedSet)
        variable_component_names = OrderedDict()
        if variable_names_safe is not None:
            for variable_name in variable_names_safe:
                variable_component_names[variable_name] = OrderedSet(
                    [parent.parent.component_name])

        kwargs.update({
            'parent': parent, 'name': name,
            'variable_component_names': variable_component_names,
            'cfg': parent.cfg, 'task_names': task_names})
        super(ResultDataSourceBase, self).__init__(**kwargs)

    @property
    def parent(self) -> 'e4clim.context.context_result.ContextResult':
        return self._parent

    def get_data_directory(self, makedirs: bool = True, **kwargs) -> Path:
        """Get path to data directory.

        :param makedirs: Make directories if needed.

        :returns: Data directory path.
        """
        return self.med.cfg.get_project_data_directory(
            self.parent.parent, makedirs=makedirs)


class Feature(ResultDataSourceBase):
    """Feature data source."""

    #: Extractor.
    _extractor: 'e4clim.context.context_result.ExtractorBase'

    #: Data-source estimation-stage.
    _stage: str

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 stage: str, **kwargs) -> None:
        """Initialize feature as data source.

        :param parent: Result manager to which data is associated.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
        """
        self._stage = stage
        self._extractor = parent.extractors[stage]

        # Variables from extractors or as parent
        variable_names = (self.extractor.variable_names or
                          OrderedSet([parent.result_name]))

        # Add task names
        task_names = OrderedSet(['extract__{}'.format(stage),
                                 'write__{}'.format(stage)])

        # Build result-manager data source with extractor variables
        name = '{}_{}'.format(parent.parent.name, self.stage)
        super(Feature, self).__init__(
            parent, name=name, task_names=task_names,
            variable_names=variable_names, **kwargs)

    @property
    def extractor(self) -> 'e4clim.context.context_result.ExtractorBase':
        return self._extractor

    @property
    def stage(self) -> str:
        return self._stage

    def parse(self, variable_component_names: e4tp.VCNType = None,
              **kwargs) -> e4tp.DatasetType:
        """Parse data from the input source and return dataset."""
        return self.extractor.transform(stage=self.stage, **kwargs)

    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.DatasetType:
        """Extract or read feature from input data,
        store it in the :py:attr:`features` member, and save it to file.
        """
        # Get extractor for stage
        if self.task_mng.get('extract__{}'.format(self.stage)):
            data_src_name = self.extractor.data_sources[self.stage].name
            self.info(
                'Extracting {} feature to {} {} from {}'.format(
                    self.parent.parent.name, self.stage,
                    self.parent.name, data_src_name))

            # Extract feature from the input data
            self.update(self.parse(
                variable_component_names=variable_component_names, **kwargs))

            # Write all variables of feature
            if self.task_mng.get('write__{}'.format(self.stage)):
                self.write(**kwargs)

            # Update task manager
            self.task_mng['extract__{}'.format(self.stage)] = False
        else:
            # Read feature for variable
            self.info(
                '{} feature to {} {} already extracted'.format(
                    self.parent.parent.name, self.stage, self.parent.name))
            kwargs_read = kwargs.copy()
            kwargs_read[
                'variable_component_names'] = self.variable_component_names
            self.read(**kwargs_read)

        return self.data

    def get_data_postfix(self, with_src_name: bool = False,
                         **kwargs) -> str:
        """Get feature postfix.

        :param with_src_name: Whether to prefix postfix with source name.

        :returns: Postfix.
        """
        # Get input data postfix
        data_src = self.extractor.data_sources[self.stage]
        feature_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Add modifier postfix
        if ((self.parent.modifier is not None) and
                (self.stage in ['predict', 'output'])):
            feature_postfix += (self.parent.modifier.
                                get_extractor_postfix(**kwargs))

        # Add feature postfix
        feature_postfix += self.extractor.get_extractor_postfix(**kwargs)

        return feature_postfix

    def get_data_path(self, variable_name: str = None,
                      makedirs: bool = True, **kwargs) -> Path:
        """Get data-source filepath using extractor "get_data_path"
        method if possible.

        :param variable_name: Data variable.
        :param makedirs: Make directories if needed.

        :returns: Filepath.
        """
        if self.extractor.get_data_path is not None:
            return self.extractor.get_data_path(
                variable_name, makedirs, **kwargs)
        else:
            if self.extractor.no_extraction:
                return self.extractor.data_sources[self.stage].get_data_path(
                    variable_name, makedirs, external=True, **kwargs)
            else:
                return super(Feature, self).get_data_path(
                    variable_name, makedirs, **kwargs)


class Prediction(ResultDataSourceBase):
    """Prediction data source."""

    #: Estimator.
    _estimator: 'e4clim.context.context_result.EstimatorBase'

    #: Features.
    _features: 'e4clim.context.context_result.FeaturesType'

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 estimator: 'e4clim.context.context_result.EstimatorBase',
                 **kwargs) -> None:
        """Initialize prediction as data source.

        :param parent: Result manager to which data is associated.
        """
        self._estimator = estimator
        self._features = parent.features

        # Add task names
        task_names = OrderedSet(['fit', 'predict'])

        # Build result-manager data source
        name = '{}_prediction'.format(parent.parent.name)
        variable_names = tools.ensure_collection(
            parent.result_name, OrderedSet)
        super(Prediction, self).__init__(
            parent, name=name, variable_names=variable_names,
            task_names=task_names, **kwargs)

    @property
    def estimator(self) -> 'e4clim.context.context_result.EstimatorBase':
        return self._estimator

    @property
    def features(self) -> 'e4clim.context.context_result.FeaturesType':
        return self._features

    def fit(self, **kwargs) -> None:
        """Fit estimator.

        .. note:: Input and output data for the fitting are read from file.
          They should thus be extracted before.
        """
        # Read or fit
        stage = 'fit'
        if self.task_mng.get(stage):
            # Get input feature
            self.features[stage].get_data(*kwargs)

            # Get output data
            self.features['output'].get_data(**kwargs)

            # Fit estimator
            self.info('Fitting {} {} estimator'.format(
                self.parent.parent.name, self.parent.name))
            self.estimator.fit(self.features[stage],
                               self.features['output'], **kwargs)

            # Save the fitted estimator
            self.estimator.write(**kwargs)

            # Update task managern
            self.task_mng[stage] = False
        else:
            # Load the estimator coefficients from file
            self.info('{} {} estimator already fitted'.format(
                self.parent.parent.name, self.parent.name))
            self.estimator.read(**kwargs)

    def parse(self, variable_component_names: e4tp.VCNType = None,
              **kwargs) -> e4tp.DatasetType:
        """Parse data from the input source and return dataset."""
        stage = 'predict'

        # Get estimator
        self.fit(**kwargs)

        # Get feature to predict
        self.features[stage].get_data(**kwargs)

        return self.estimator.predict(self.features[stage], **kwargs)

    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.DatasetType:
        """Predict and store result to :py:attr:`prediction` member.

        .. note:: Input data for the prediction is read from file.
          It should thus be extracted before.
        """
        # Make sure that variable names not in keyword arguments
        if 'variable_component_names' in kwargs:
            del kwargs['variable_component_names']

        stage = 'predict'
        if self.task_mng.get(stage):
            # Apply
            self.info('Predicting {} {}'.format(
                self.parent.parent.name, self.parent.name))
            # Extract feature from the input data
            self.update(self.parse(
                variable_component_names=variable_component_names, **kwargs))

            # Save
            # Warning: input data to fit estimator will be forgotten
            self.write(**kwargs)

            # Update task manager
            self.task_mng[stage] = False
        else:
            # Read prediction
            self.info('{} {} already predicted'.format(
                self.parent.parent.name, self.parent.name))
            kwargs_read = kwargs.copy()
            kwargs_read['variable_component_names'] = self.variable_component_names
            self.read(**kwargs_read)

        return self.data

    def get_data_postfix(self, **kwargs) -> str:
        """Get prediction postfix.

        :returns: Postfix.
        """
        postfix = self.estimator.get_fit_postfix(**kwargs)

        # Add feature-for-prediction postfix if needed
        if self.features['predict'] is not self.features['fit']:
            postfix = self.features['predict'].get_data_postfix(
                **kwargs) + postfix

        return postfix
