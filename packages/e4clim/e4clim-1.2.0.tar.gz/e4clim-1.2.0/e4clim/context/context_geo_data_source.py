from orderedset import OrderedSet
import typing as tp
from e4clim.container.base import ContainerBase
from e4clim.container.geo_data_source import GeoDataSourceBase
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import ContextBase
from .context_multi_data_sources import _get_single_or_multi_data_src_name


class ContextGeoDataSource(ContextBase):
    """Geographic data source context."""

    #: Geographic data-source configuration.
    _data_src: GeoDataSourceBase

    def __init__(self, parent: ContainerBase,
                 name: str = 'context_geo_data_source', cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize geographic data source context.

        :param parent: Parent.
        :param name: Name
        :param cfg: Configuration.
        """
        super(ContextGeoDataSource, self).__init__(
            name, cfg=cfg, parent=parent, **kwargs)

    @property
    def data_src(self) -> GeoDataSourceBase:
        return self._data_src

    def build(self) -> None:
        """Build context.

        :raises AssertionError: if data source is not
          :py:class:e4clim.container.geo_data_source.GeoDataSourceBase`.
        """
        if self.cfg.cfg is None:
            self.warning(
                'No geographic data source configuration provided: skipping')
            self._data_src = None
        else:
            # Add data sources for areas required by components
            data_src_names = self._get_data_src_names_for_all_areas()
            self.med.build_data_source(data_src_names, isgeo=True)

            # Assign convenience member pointing to (multiple) geo data source
            multi_data_src_name = _get_single_or_multi_data_src_name(
                data_src_names)
            data_src = self.med.data_sources[multi_data_src_name]

            assert isinstance(data_src, GeoDataSourceBase), (
                '"{}" in "data_sources" attribute of "med" attribute '
                'should be "GeoDataSourceBase"'.format(multi_data_src_name))

            self._data_src = data_src

    def _get_data_src_names_for_all_areas(self) -> tp.MutableSet[str]:
        """Get data-source names for all areas.

        :returns: Data-source names.
        """
        cfg_data = tools.get_required_mapping_entry(self.cfg, 'data')
        cfg_contexts = tools.get_required_mapping_entry(
            self.med.cfg, 'context_components_per_area')
        data_src_names = []
        for area in cfg_contexts:
            data_src_names.append(tools.get_required_str_entry(cfg_data, area))

        return OrderedSet(data_src_names)
