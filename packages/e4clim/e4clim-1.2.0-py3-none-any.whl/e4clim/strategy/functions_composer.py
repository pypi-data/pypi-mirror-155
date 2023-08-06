"""Extractor defining transform method from functions composition."""
from collections import OrderedDict
from importlib import import_module
import typing as tp
import e4clim
from e4clim.build.strategy import build_data_sources_for_strategy
from e4clim.container.gridded_data_source import GriddedDataSourceBase
from e4clim.container.strategy import ExtractorBase
import e4clim.typing as e4tp
from e4clim.utils import tools


class Strategy(ExtractorBase):
    """Extractor defining transform method from functions composition."""

    #: Functions composed to define :py:meth:`transform` method.
    _functions: tp.List[tp.Any]

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None,
                 functions: tp.List[tp.Any] = None, **kwargs) -> None:
        """Constructor defining transform method from functions composition.

        :param parent: Result manager of variable to estimate.
        :param name: Strategy name.
        :param cfg: Strategy configuration.

        .. note:: Functions to compose must be provided as a list
          from the `functions` entry of the configuration.
        """
        super(Strategy, self).__init__(
            parent=parent, name=name, cfg=cfg, **kwargs)

        if functions is None:
            # Import functions
            functions_paths = tools.get_required_iterable_str_entry(
                self.cfg, 'functions', list)
            self._functions = [import_function(fp) for fp in functions_paths]
        else:
            # Assign user-defined functions
            self._functions = functions

        # Add data sources
        if 'data' in self.cfg:
            if self.data_sources is None:
                self.data_sources = OrderedDict()
            build_data_sources_for_strategy(self, **kwargs)

        # Set variable names from data
        variable_names: tp.Set = set()
        for data_src in self.data_sources.values():
            variable_names.update(data_src.variable_component_names)
        self.set_variable_names(variable_names)

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Composed function.

        :param stage: Modeling stage: `'fit'`, `'predict'` or `'output'`.

        :returns: Transformed dataset.

        :raises AssertionError: if

            * :py:obj:`stage` attribute is `None`,
            * data source is not :py:class:`GriddedDataSourceBase`.

        """
        assert stage is not None, '"stage" argument is not optional here'

        # Select gridded data source
        data_src = self.data_sources[stage]
        variable_component_names = self.stage_variable_component_names[stage]
        assert isinstance(data_src, GriddedDataSourceBase), (
            'Data source for "{}" should be "ParsingMultiDataSourceBase"'
            ''.format(stage))

        transform_function = tools.Composer(*self._functions)

        # Get wind generation from climate data
        ds = data_src.parse_finalize(
            transform=transform_function,
            variable_component_names=variable_component_names)

        return ds


def import_function(function_path: str) -> tp.Callable[..., e4tp.DatasetType]:
    """Import function.

    :param function_path: Function path.
    :type function_path: str

    :return: Imported function.
    :rtype: function
    """
    # Get module path and function name
    fun_path_split = function_path.split('.')
    module_path = '.'.join(fun_path_split[:-1])
    function_name = fun_path_split[-1]

    # Import function module
    module = import_module(module_path)

    # Return function
    return getattr(module, function_name)
