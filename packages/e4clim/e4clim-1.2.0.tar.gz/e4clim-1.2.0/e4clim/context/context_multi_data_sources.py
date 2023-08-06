from collections import OrderedDict
from orderedset import OrderedSet
from e4clim.container.base import ContainerBase
from e4clim.container.geo_multi_data_source import GeoParsingMultiDataSourceBase
from e4clim.container.multi_data_source import MultiDataSourceBase
from e4clim.container.parsing_multi_data_source import (
    ParsingMultiDataSourceBase)
from .context_single_data_sources import ContextSingleDataSourcesMixin
import e4clim.typing as e4tp
from e4clim.utils import tools


class ContextMultiDataSourcesMixin(ContextSingleDataSourcesMixin):
    """To mix with :py:class:`.context_data_sources.ContextDataSources`
    to manage multi-data sources."""

    _data_sources: e4tp.DataSourcesType

    def __init__(self, parent: ContainerBase,
                 name: str = 'context_data_sources', cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize data-source context.

        :param parent: Parent.
        :param name: Name.
        :param cfg: Configuration.
        """
        super(ContextMultiDataSourcesMixin, self).__init__(
            parent, name, cfg=cfg, **kwargs)

    def build_multi_data_source(
            self,
            data_src_variable_component_names: e4tp.StrToVCNType,
            parent: ContainerBase = None, isgeo: bool = False,
            **kwargs) -> MultiDataSourceBase:
        """Initialize multiple data source, inject to context,
        and return it as well.

        :param data_src_variable_component_names: Mapping with multiple
          (source name, variable_component_names mapping)
          (key, value) pairs, sequence of source names, or source name.
        :param parent: Container for which to add data source.
        :param isgeo: Whether data source is
          :py:class`.geo.GeoDataSourceBase`.

        :returns: Multiple data source.
        """
        ds_vcn_safe = _ensure_data_src_mapping(
            data_src_variable_component_names)

        data_sources = self.build_single_data_source_of_multi(
            ds_vcn_safe, parent)

        multi_data_src = self.build_multi_data_source_if_needed(
            data_sources, isgeo)

        return multi_data_src

    def build_single_data_source_of_multi(
            self, data_src_variable_component_names: e4tp.StrToVCNType,
            parent: ContainerBase = None) -> e4tp.SingleDataSourcesType:
        """Add single data sources of multiple data source.

        :param data_src_variable_component_names: Mapping from data-source name
          to mapping from variable to component names.
        :param parent: Container for which to load the source.

        :returns: Mapping of data sources.
        """
        data_sources = OrderedDict()
        for src_name, variable_component_names in (
                data_src_variable_component_names.items()):
            data_src = self.build_single_data_source(
                src_name, variable_component_names=variable_component_names,
                parent=parent)

            # Add data source to multi-data source dictionary
            data_sources[src_name] = data_src

        return data_sources

    def build_multi_data_source_if_needed(
            self, data_sources: e4tp.SingleDataSourcesType,
            isgeo: bool) -> MultiDataSourceBase:
        """Verify that multiple data source not already added by other
        containers and add it.

        :param data_sources: Mapping of data sources.
        :param isgeo: Whether data source is :py:class`.geo.GeoDataSourceBase`.

        :returns: Multiple data source.
        """
        multi_src_name = ParsingMultiDataSourceBase.get_name(data_sources)
        if multi_src_name in self._data_sources:
            # Get existing multiple data source
            multi_data_src = self._data_sources[multi_src_name]

            assert isinstance(multi_data_src, MultiDataSourceBase), (
                '"multi_data_src" is not a "MultiDataSourceBase"')

            # Update multiple data source with potential new data sources
            multi_data_src.data_sources = data_sources

            return multi_data_src
        else:
            # Create multiple data source from data sources dictionary
            multi_data_src_new = (
                GeoParsingMultiDataSourceBase(self, data_sources) if isgeo
                else ParsingMultiDataSourceBase(self, data_sources))

            # Inject multiple data source to context
            self._data_sources[multi_src_name] = multi_data_src_new

            return multi_data_src_new


def _ensure_data_src_mapping(
        data_src_variable_component_names:
        e4tp.StrToVCNType) -> e4tp.StrToVCNType:
    """If a collection of source names is given, transform it
    to a mapping from source names to None (variable_names).

    :param data_src_variable_component_names: Collection of data-source
      names or mapping from data-source name
      to mapping from variable to component names.
    """
    ds_vcn_safe = OrderedDict()
    for src_name in data_src_variable_component_names:
        vcn = data_src_variable_component_names.get(src_name)
        if vcn is None:
            ds_vcn_safe[src_name] = OrderedSet()
        else:
            ds_vcn_safe[src_name] = data_src_variable_component_names[src_name]

    return ds_vcn_safe


def _get_single_or_multi_data_src_name(
        data_src_names: e4tp.StrIterableType) -> str:
    """Get single or multiple data source name.

    :param data_src_names: Data-source names.

    :returns: Data-source name.
    """
    data_src_names_safe = tools.ensure_collection(data_src_names, list)

    if len(data_src_names_safe) > 1:
        return MultiDataSourceBase.get_name(data_src_names_safe)
    else:
        return data_src_names_safe[0]
