from collections import OrderedDict
import typing as tp
from e4clim.container.base import ContainerBase
from e4clim.container.data_source import DataSourceBase
import e4clim.typing as e4tp
from e4clim.utils import tools
from .context_multi_data_sources import ContextMultiDataSourcesMixin


class ContextDataSources(ContextMultiDataSourcesMixin):
    """Data-sources context."""
    #: Data-sources mapping.
    _data_sources: e4tp.DataSourcesType

    def __init__(self, parent: ContainerBase,
                 name: str = 'context_data_sources', cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize data-source context.

        :param parent: Parent.
        :param name: Name.
        :param cfg: Configuration.
        """
        super(ContextDataSources, self).__init__(
            parent, name, cfg=cfg, **kwargs)

        #: Data-sources mapping.
        self._data_sources = OrderedDict()

    @property
    def data_sources(self) -> e4tp.DataSourcesType:
        return self._data_sources

    def build(self, data_src_variable_component_names: e4tp.StrToVCNStrictType,
              parent: ContainerBase = None, isgeo: bool = False,
              **kwargs) -> DataSourceBase:
        """ Build single or multiple data source depending on whether
        :py:obj:`src_dict` has keys.

        :param data_src_variable_component_names: Mapping with multiple
          (source name, variable_component_names mapping)
          (key, value) pairs, sequence of source names, or source name.
        :param parent: Container for which to load the source.
        :param isgeo: Whether data source is
          :py:class`e4clim.container.geo.GeoDataSourceBase`.

        :returns: Data source.
        """
        # Get test
        not_str = not isinstance(data_src_variable_component_names, str)
        is_col = isinstance(data_src_variable_component_names,
                            tp.Collection)
        multiple = len(data_src_variable_component_names) > 1

        if (not_str and is_col and multiple):
            # Add multiple data source
            multi_data_src = self.build_multi_data_source(
                data_src_variable_component_names, parent=parent, isgeo=isgeo,
                **kwargs)

            return multi_data_src
        else:
            # Add single data source
            data_src_name, variable_component_names = (
                _extract_data_src_variable_component_names(
                    data_src_variable_component_names, **kwargs))
            single_data_src = self.build_single_data_source(
                data_src_name,
                variable_component_names=variable_component_names,
                parent=parent, **kwargs)

            return single_data_src


def _extract_data_src_variable_component_names(
        data_src_variable_component_names: e4tp.StrToVCNStrictType,
        **kwargs) -> tp.Tuple[str, e4tp.VCNType]:
    """Extract data-source name and variable to component names mapping.

    :param data_src_variable_component_names: Mapping from data-source name
      to mapping from variable to component names.

    :returns: Data-source name and variable-component names mapping.
    """
    if isinstance(data_src_variable_component_names, tp.Mapping):
        data_src_name = list(data_src_variable_component_names)[0]

        variable_component_names = data_src_variable_component_names[data_src_name]
    else:
        # Try to get variables from keyword arguments,
        # otherwise, leave None
        variable_component_names = kwargs.pop(
            'variable_component_names', None)
        data_src_name = str(*tools.ensure_collection(
            data_src_variable_component_names, list))

    return data_src_name, variable_component_names
