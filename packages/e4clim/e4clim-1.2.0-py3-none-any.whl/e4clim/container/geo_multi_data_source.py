from collections import OrderedDict
from copy import copy
from orderedset import OrderedSet
import pandas as pd
import xarray as xr
import e4clim
import e4clim.typing as e4tp
from . import geo_data_source as gds
from .gridded_data_source import GriddedDataSourceBase
from .multi_data_source import _set_data_sources
from .multi_data_source import MultiDataSourceBase


class GeoParsingMultiDataSourceBase(
        MultiDataSourceBase, gds.GeoDataSourceBase):
    """Multiple geographic data source.
    Redefines :py:meth:`get` method to merge (geographic) variable
    in all single data sources into a single
    :py:class:`pandas.GeoDataFrame`."""
    data: e4tp.GeoDatasetMutableType

    _data_sources: e4tp.GeoSingleDataSourcesType

    @property
    def data_sources(self) -> e4tp.GeoSingleDataSourcesType:
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources:
                     e4tp.GeoSingleDataSourcesType) -> None:
        _set_data_sources(self, data_sources)

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 data_sources: e4tp.SingleDataSourcesType,
                 task_names: e4tp.StrIterableType = OrderedSet(),
                 default_tasks_value: bool = True, **kwargs) -> None:
        """Build with :py:class:`.data_source.MultiDataSource` constructor.

        :param parent: Data-sources context.
        :param data_sources: Data sources dictionary.
        :param task_names: Names of potential tasks for container to perform.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none.
        """
        # Initialize as data source
        super(GeoParsingMultiDataSourceBase, self).__init__(
            parent, data_sources, task_names=OrderedSet(),
            default_tasks_value=True, **kwargs)

        # Initialize regions and places merging from single data sources
        self._init_regions_places(**kwargs)

    def make_mask(self, data_src: GriddedDataSourceBase,
                  **kwargs) -> xr.Dataset:
        """Make mask for a given gridded data source, store the
        regions' geometries to :py:attr:`data` member.

        :param data_src: Gridded data source.

        :returns: Mask dataset.
        """
        return gds._make_mask(self, data_src, **kwargs)

    def _init_regions_places(self, **kwargs) -> None:
        """Set region-to-zone/region mapping :py:attr:`region_place`,
        zone/region-names set :py:attr:`place_names` and
        zone/region-to-regions mapping :py:attr:`place_regions`
        merging from single data sources.

        :raises AssertionError: if 

            * :py:attr:`data_sources` attribute does not exist,
            * data sources in :py:attr:`data_sources` attribute are not
             :py:class:`gds.GeoParsingDataSourceBase`'s.

        """
        # Make sure that the initialization is called after
        # the parents constructors are called
        assert hasattr(self, 'data_sources'), (
            '"data_sources" attribute required.')

        # Get zones/regions description from any single data source
        data_src = self.data_sources[list(self.data_sources)[0]]
        assert isinstance(data_src, gds.GeoParsingSingleDataSourceBase), (
            'Data sources in "data_sources" attribute should be '
            '"GeoDataSourceBase"s')
        self.area_places_sources = data_src.area_places_sources

        # Merge attributes
        self.region_place = OrderedDict()
        self.place_regions = OrderedDict()
        self.place_indices = OrderedDict()
        self.area_places = OrderedDict()
        self.place_area = OrderedDict()
        self.place_names = OrderedSet()
        self.region_names = OrderedSet()
        self.areas = OrderedSet()
        for data_src in self.data_sources.values():
            assert isinstance(data_src, gds.GeoParsingSingleDataSourceBase), (
                'Data sources in "data_sources" attribute should be '
                '"GeoDataSourceBase"s')

            # Merge mappings
            self.region_place.update(data_src.region_place)
            self.place_regions.update(data_src.place_regions)
            self.place_area.update(data_src.place_area)
            # Allow for multiple data sources per area
            for area, places in data_src.area_places.items():
                self.area_places[area] = places

            # Merge sets
            for place_name in data_src.place_names:
                self.place_names.add(place_name)
            for region_name in data_src.region_names:
                self.region_names.add(region_name)
            for area in data_src.areas:
                self.areas.add(area)

        # Get place indices
        self.place_indices = gds._get_place_indices(self.place_names, **kwargs)

    def get_data(self, **kwargs) -> e4tp.GeoDatasetMutableType:
        """Load geographic data from multiple geographic data sources
        and merge the geographic data into one geographic data frame.

        :returns: Dataset :py:attr:`data`.

        :raises AssertionError: if data sources in :py:attr:`data_sources`
          attribute are not :py:class:`gds.GeoParsingDataSourceBase`'s.
        """
        gdf = None

        # Get reference CRS
        data_sources = copy(self.data_sources)
        crs_as_data_src = self.med.geo_cfg.get('crs_as')
        skip_data_src = ''
        if crs_as_data_src:
            crs_as_data_src_safe = str(crs_as_data_src)
            data_src = data_sources[crs_as_data_src_safe]
            assert isinstance(data_src, gds.GeoParsingSingleDataSourceBase), (
                'Data sources in "data_sources" attribute should be '
                '"GeoDataSourceBase"s')
            gdf = data_src.get_data(**kwargs)[gds.GEO_VARIABLE_NAME]
            crs = gdf.crs
            skip_data_src = crs_as_data_src_safe

        for src_name, data_src in data_sources.items():
            if src_name != skip_data_src:
                assert isinstance(data_src, gds.GeoParsingSingleDataSourceBase), (
                    'Data sources in "data_sources" attribute should be '
                    '"GeoDataSourceBase"s')
                # Get data for geo variable of single source
                gdf_single = data_src.get_data(**kwargs)[gds.GEO_VARIABLE_NAME]

                if crs_as_data_src:
                    # Convert to reference CRS
                    gdf_single = gdf_single.to_crs(crs)

                # Merge geographic data frame
                gdf = gdf_single if gdf is None else pd.concat(
                    [gdf, gdf_single])

        # Assign
        data = {gds.GEO_VARIABLE_NAME: gdf}

        self.data = data

        return data
