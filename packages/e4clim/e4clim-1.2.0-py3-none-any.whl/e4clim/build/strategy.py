from collections import OrderedDict
from orderedset import OrderedSet
import typing as tp
from e4clim.config import import_class_from_cfg
from e4clim.container.base import ContainerBase
from e4clim.container.data_source import DataSourceBase
from e4clim.container.parsing_multi_data_source import (
    ParsingMultiDataSourceBase)
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.container.strategy as strategy_mod
from e4clim.context.context_result import ContextResult
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import BuilderBase, DirectorBase


class BuilderStrategy(BuilderBase):
    """Strategy builder."""

    _product: strategy_mod.StrategyBase
    _director: 'DirectorStrategy'

    def __init__(self, **kwargs) -> None:
        super(BuilderStrategy, self).__init__(ContainerBase)

    @property
    def product(self) -> strategy_mod.StrategyBase:
        return self._product

    @property
    def director(self) -> 'DirectorStrategy':
        return self._director

    def set_class(self, parent: ContextResult, name: str) -> None:
        """Set class.

        :param parent: Result context.
        :param name: Name.

        :raises AssertionError: if :py:attr:`cfg` attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute required'

        self._cls = (import_class_from_cfg(self.cfg) or
                     _import_default_strategy_class(parent, name))

    def build_data_sources(self, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Add data sources from configuration.

        :param cfg: Configuration from which to get data source.
          If `None`, the strategy configuration is used.

        :raises AssertionError: if

            * both :py:obj:`cfg` argument and :py:attr:`cfg` attribute
              is `None`,
            * Data sources are neither
              :py:class:`e4clim.container.parsing_multi_data_source.ParsingMultiDataSourceBase` nor
              :py:class:`e4clim.container.parsing_single_data_source.ParsingSingleDataSourceBase`.

        """
        if cfg is None:
            assert self.cfg is not None, (
                'Either "cfg" argument of "cfg" attribute required')
            cfg_data = tools.get_required_mapping_entry(self.cfg, 'data')
        else:
            cfg_data = tools.get_required_mapping_entry(cfg, 'data')

        build_data_sources_for_strategy(self.product, cfg_data, **kwargs)


class DirectorStrategy(DirectorBase):
    """Strategy director."""

    _builder: BuilderStrategy

    @property
    def builder(self) -> BuilderStrategy:
        return self._builder

    @builder.setter
    def builder(self, builder: BuilderStrategy) -> None:
        self._builder = builder

    def make(self, cfg: e4tp.CfgType = None, parent: ContextResult = None,
             name: str = None, **kwargs) -> strategy_mod.StrategyBase:
        """Make strategy.

        :param cfg: Strategy configuration.
        :param parent: Parent container to which to add strategy.
        :param name: Strategy name.

        :returns: Strategy.

        :raises AssertionError: if

            * :py:obj:`cfg` argument is not a mapping.
            * :py:obj:`name` argument is `None`,
            * :py:obj:`parent` argument is `None`.

        """
        assert name is not None, '"name" argument required'
        assert parent is not None, '"parent" argument required'

        self.builder.configure(cfg, parent=parent, name=name)

        self.builder.set_class(parent, name)

        self.builder.reset(parent, name, self.builder.cfg, **kwargs)
        self.builder.product.info('{} strategy injected in {} {}'.format(
            name, parent.parent.name, parent.name))

        # Add data sources
        if cfg is not None:
            assert isinstance(cfg, tp.Mapping), (
                '"cfg" argument should be a mapping')
            if 'data' in cfg:
                self.builder.build_data_sources(**kwargs)

        return self.builder.product


def _import_default_strategy_class(
        parent: ContextResult,
        strategy_name: str) -> tp.Type[strategy_mod.StrategyBase]:
    """Get default class from this module.

    :param container: Parent container to which to add strategy.
    :param strategy_name: Strategy name.

    :returns: Default strategy class name and module.
    """
    # Get default class name from this module
    strategy_class_name = 'Default' + ''.join(
        act_name.title()
        for act_name in strategy_name.split('_'))
    parent.warning(
        "No 'class' found in {} configuration: "
        "using {} class strategy".format(
            strategy_name, strategy_class_name))
    strategy_class = getattr(strategy_mod, strategy_class_name)

    return strategy_class


def build_data_sources_for_strategy(
        strategy: strategy_mod.StrategyBase,
        cfg_data: tp.Mapping[str, tp.Any] = None,
        **kwargs) -> None:
    """Add data sources from configuration.

    :param strategy: Strategy.
    :param cfg_data: Data configuration for strategy.

    :raises AssertionError: if

        * both :py:obj:`cfg` argument and :py:attr:`cfg` attribute
          is `None`,
        * Data sources are neither
          :py:class:`e4clim.container.parsing_multi_data_source.ParsingMultiDataSourceBase` nor
          :py:class:`e4clim.container.parsing_single_data_source.ParsingSingleDataSourceBase`.

    """
    if cfg_data is None:
        cfg_data = tools.get_required_mapping_entry(strategy.cfg, 'data')

    for stage in cfg_data:
        data_src_variable_names = tools.get_required_mapping_entry(
            cfg_data, stage)
        data_src_variable_component_names = _get_data_src_vcn_for_strategy(
            strategy, stage, data_src_variable_names)

        data_src = _build_data_source(
            strategy, data_src_variable_component_names)
        assert (isinstance(data_src, ParsingMultiDataSourceBase) or
                isinstance(data_src, ParsingSingleDataSourceBase)), (
                    'Data source should be either'
                    '"ParsingMultiDataSourceBase" or'
                    '"ParsingSingleDataSourceBase"')
        strategy.data_sources[stage] = data_src

        # Add data sources as children
        strategy.update_children({
            strategy.data_sources[stage].name:
            strategy.data_sources[stage]})


def _build_data_source(
        strategy: strategy_mod.StrategyBase,
        data_src_variable_component_names: e4tp.VCNType) -> DataSourceBase:
    """Add data source to application and parent result context."""
    data_src = strategy.med.build_data_source(
        data_src_variable_component_names, strategy.parent)

    return data_src


def _get_data_src_vcn_for_strategy(
        strategy: strategy_mod.StrategyBase,
        stage: str, data_src_variable_names:
        e4tp.StrToVCNType) -> e4tp.VCNType:
    """Get variable to component names for data source at stage.

    :param strategy: Strategy.
    :param stage: Stage.
    :param data_src_variable_names: Data source to variable component
      names.

    :returns: Variable component names.
    """
    strategy.stage_variable_component_names[stage] = OrderedDict()
    data_src_variable_component_names = OrderedDict()

    for data_src_name, variable_names in (
            data_src_variable_names.items()):
        # Make sure variable names is a set
        variable_names = tools.ensure_collection(variable_names, OrderedSet)

        # Create variable-component names mapping for data source
        variable_component_names = OrderedDict(
            {variable_name: OrderedSet(
                [strategy.parent.parent.component_name])
             for variable_name in variable_names})

        # Add data source to mapping
        data_src_variable_component_names[
            data_src_name] = variable_component_names

        # Add variable names to set
        strategy.stage_variable_component_names[stage].update(
            variable_component_names)

    return data_src_variable_component_names
