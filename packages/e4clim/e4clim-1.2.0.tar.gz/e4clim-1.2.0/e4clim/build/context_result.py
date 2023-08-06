from e4clim.container.multi_data_source import MultiDataSourceBase
from e4clim.container.result_data_source import Feature, Prediction
from e4clim.container.strategy import StrategyBase
from e4clim.context.context_component import ContextComponent
from e4clim.context.context_result import ContextResult
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import BuilderBase, DirectorBase
from .strategy import DirectorStrategy


class BuilderContextResult(BuilderBase):
    """Result context builder."""

    _product: ContextResult
    _director: 'DirectorContextResult'

    def __init__(self, **kwargs) -> None:
        super(BuilderContextResult, self).__init__(ContextResult)

    @property
    def product(self) -> ContextResult:
        return self._product

    @property
    def director(self) -> 'DirectorContextResult':
        return self._director

    def build_strategies(self, **kwargs) -> None:
        """Build strategies.

        :raises AssertionError: if :py:attr:`cfg` attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute required'

        strategies_cfg = tools.get_required_mapping_entry(
            self.cfg, 'strategies', {})
        for name, cfg in strategies_cfg.items():
            strategy = self._request_strategy(
                cfg, self.product, name, **kwargs)
            self._set_strategy(name, strategy)

    def add_data_sources(self) -> None:
        """Add data sources required by result context from all of its
        strategies."""
        for strategy in self.product.strategies.values():
            if strategy.data_sources is not None:
                self.build_strategy_data_source(strategy)

    def _request_strategy(self, *args, **kwargs) -> StrategyBase:
        """Request strategy."""
        strategy = self.director.make_strategy(*args, **kwargs)

        return strategy

    def _set_strategy(self, name: str, strategy: StrategyBase) -> None:
        """Set strategy.

        :param name: Strategy name.
        :param strategy: Strategy.
        """
        setattr(self.product, name, strategy)
        self.product.strategies[name] = strategy

    def build_strategy_data_source(self, strategy: StrategyBase) -> None:
        """Add data source for strategy.

        :param strategy: Strategy.
        """
        for data_src in strategy.data_sources.values():
            # Add as single data source
            self.product.data_sources.update({data_src.name: data_src})

            # Add as single data sources from multiple data source
            if isinstance(data_src, MultiDataSourceBase):
                self.product.data_sources.update({
                    single_data_src.name: single_data_src
                    for single_data_src in
                    data_src.data_sources.values()})

    def build_extractors_and_data_attributes(self, **kwargs) -> None:
        """Build data attributes making sure that extractors are built before.
        """
        self.build_extractors(**kwargs)

        self.build_data_attributes(**kwargs)

    def build_extractors(self, **kwargs) -> None:
        """Initialize extractors."""
        if self.product.output_extractor is not None:
            # Add output extractor
            self.product.extractors['output'] = self.product.output_extractor

        if self.product.feature_extractor is not None:
            # Add feature extractors for all stages
            for stage in 'fit', 'predict':
                self.product.extractors[
                    stage] = self.product.feature_extractor

    def build_data_attributes(self, **kwargs) -> None:
        """Initialize data attributes.

        .. warning: : : py: meth: `build_extractors` must be called before.
        """
        # Initialize output-feature data source
        self.product.features['output'] = Feature(
            self.product, stage='output', **kwargs)

        if self.product.estimator is not None:
            # Initialize prediction data source
            self.product.prediction = Prediction(
                self.product, self.product.estimator, **kwargs)

            # Assign prediction to result
            self.product.result = self.product.prediction
        else:
            # Assign output feature to result
            self.product.result = self.product.features['output']

        # Plug result methods to output variable
        self.product.update_variables(
            self.product.result.variable_component_names, **kwargs)
        self.product.data = self.product.result.data

        if self.product.feature_extractor is not None:
            # Initialize features, associated with inputs
            self.build_features(**kwargs)

    def build_features(self, **kwargs) -> None:
        """Build features for result context."""
        # Add new feature to fit
        stage = 'fit'
        self.product.features[stage] = Feature(
            self.product, stage=stage, **kwargs)

        # Add feature to predict
        stage = 'predict'
        if stage in self.product.extractors[stage].data_sources:
            # Create feature to predict
            self.product.features[stage] = Feature(
                self.product, stage=stage, **kwargs)
        else:
            # Feature to pedict same as feature to fit
            fit_stage = 'fit'
            self.product.features[stage] = self.product.features[fit_stage]
            self.product.extractors[stage] = self.product.extractors[fit_stage]
            self.product.extractors[stage].data_sources[
                stage] = self.product.extractors[stage].data_sources[fit_stage]


class DirectorContextResult(DirectorBase):
    """Result context director."""

    _builder: BuilderContextResult

    _deputy_strategy: DirectorStrategy

    def __init__(self, builder: BuilderContextResult,
                 deputy_strategy: DirectorStrategy) -> None:
        super(DirectorContextResult, self).__init__(builder)
        self._deputy_strategy = deputy_strategy

    @property
    def builder(self) -> BuilderContextResult:
        return self._builder

    @builder.setter
    def builder(self, builder: BuilderContextResult) -> None:
        self._builder = builder

    @property
    def deputy_strategy(self) -> DirectorStrategy:
        return self._deputy_strategy

    def make(self, cfg: e4tp.CfgType = None, parent: ContextComponent = None,
             name: str = None, **kwargs) -> ContextResult:
        """Make result context.

        :param cfg: Result-context configuration.
        :param parent: Parent component context.
        :param name: Result-context name.

        :returns: Result context.

        :raises AssertionError: if

            * "name" argument is `None`,
            * "parent" argument is `None`.

        """
        assert name is not None, '"name" argument required'
        assert parent is not None, '"parent" argument required'

        self.builder.configure(cfg, parent=parent, name=name)

        self.builder.reset(parent, name, self.builder.cfg, **kwargs)
        self.builder.product.info('{} result injected in {} component'.format(
            name, parent.name))

        self.builder.build_strategies(**kwargs)

        self.builder.add_data_sources()

        self.builder.build_extractors_and_data_attributes(**kwargs)

        return self.builder.product

    def make_strategy(self, *args, **kwargs) -> StrategyBase:
        """Make strategy.

        :returns: strategy.
        """
        strategy = self.deputy_strategy.make(*args, **kwargs)

        return strategy
