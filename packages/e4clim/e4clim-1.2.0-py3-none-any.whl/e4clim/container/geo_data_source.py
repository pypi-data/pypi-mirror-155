"""Geographic-data and mask base definitions."""
from abc import ABC, abstractmethod
from collections import OrderedDict
import difflib
import geopandas as gpd
from io import BytesIO
from orderedset import OrderedSet
import oyaml as yaml
import pandas as pd
from pathlib import Path
from pkg_resources import resource_stream
import requests
import typing as tp
import xarray as xr
import zipfile
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools
from .data_source import DataSourceBase
from .gridded_data_source import GriddedDataSourceBase
from .parsing_single_data_source import ParsingSingleDataSourceBase
from .mask import get_point_region_membership

AreasType = tp.MutableSet[str]
AreaPlacesType = tp.MutableMapping[str, e4tp.PlaceNamesType]
AreaRegionsType = AreaPlacesType
RegionNamesType = e4tp.PlaceNamesType
RegionPlaceType = tp.MutableMapping[str, str]
PlaceRegionsType = AreaPlacesType
PlaceSourcesType = tp.MutableMapping[str, tp.MutableMapping[
    str, tp.Union[str, e4tp.PlaceNamesType]]]
AreaPlacesSourcesType = tp.MutableMapping[str, PlaceSourcesType]
PlaceAreaType = tp.MutableMapping[str, str]
PlaceIndicesType = tp.MutableMapping[str, int]

#: Geographic-variable name.
GEO_VARIABLE_NAME: tp.Final[str] = 'border'


class GeoDataSourceBase(DataSourceBase):
    #: Area and zones/regions description per data sources.
    area_places_sources: AreaPlacesSourcesType
    #: Area-zones/regions mapping for data source.
    area_places: AreaPlacesType
    #: Area-regions mapping for data source.
    area_regions: AreaRegionsType
    #: Place-area mapping.
    place_area: PlaceAreaType
    #: Areas.
    areas: AreasType
    #: Region-zone/region mapping.
    region_place: RegionPlaceType
    #: Zone/region-region mapping.
    place_regions: PlaceRegionsType
    #: Data-source region names.
    region_names: RegionNamesType
    #: Zone/region names.
    place_names: e4tp.PlaceNamesType
    #: Zone/region indices = None
    place_indices: PlaceIndicesType

    @abstractmethod
    def make_mask(self, data_src: GriddedDataSourceBase,
                  **kwargs) -> xr.Dataset:
        ...

    def get_total_bounds(self, epsg: int = 4326,
                         **kwargs) -> tp.Sequence[float]:
        raise NotImplementedError


class GeoParsingSingleDataSourceBase(GeoDataSourceBase,
                                     ParsingSingleDataSourceBase):
    """Geographic data-source abstract base class."""

    data: e4tp.GeoDatasetMutableType

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Convenience constructor for default geographic data source.

        :param parent: Data-source context.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        kwargs['variable_component_names'] = GEO_VARIABLE_NAME
        super(GeoParsingSingleDataSourceBase, self).__init__(
            parent, name, cfg=cfg, data_as_dict=True, **kwargs)

        # Get mappings and list
        self._init_regions_places(**kwargs)

    def __getitem__(self, variable_name: str) -> gpd.GeoDataFrame:
        """Get variable data from :py:attr:`data`.

        :param variable_name: Variable name.

        :returns: Variable.
        """
        return self.data[variable_name]

    def get(self, variable_name: str, default=None) -> tp.Optional[
            gpd.GeoDataFrame]:
        """Get variable data from :py:attr`data`.

        :param variable_name: Variable name.
        :param default: Default value.

        :returns: Variable.
        """
        return self.data.get(variable_name, default)

    def __setitem__(self, variable_name: str, data: gpd.GeoDataFrame) -> None:
        """Set item in :py:attr:`data`.

        :param variable_name: Variable name.
        :param data: Data of variable to set.
        """
        self.data[variable_name] = data

    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.GeoDatasetMutableType:
        """Read or parse data from a given source and store it in
        :py:attr:`data` member.

        :param variable_component_names: Names of components per variable.

        :returns: Dataset :py:attr:`data`.
        """
        data = super(GeoParsingSingleDataSourceBase, self).get_data(
            variable_component_names=variable_component_names, **kwargs)

        # Check type
        data_safe = {}
        for src_name, gdf in data.items():
            assert isinstance(gdf, gpd.GeoDataFrame), (
                'Data for "{}" is not "geopandas.GeoDataFrame"'.format(
                    src_name))
            data_safe[src_name] = gdf

        return data_safe

    def get_place_regions_for_source(
            self, src_name: str, area: str = None,
            component_name: str = None, **kwargs) -> tp.Tuple[
                PlaceRegionsType, RegionPlaceType]:
        """Get zone/region-regions and region-zone/region mappings
        for data source and area.

        :param src_name: Data-source name for which to get place names.
        :param area: Area for which to get place names. If `None`,
          places are returned for all areas.
        :param component_name: Component name for which to get place names,
          based on the data sources used by component managers with the same
          component name. If `None`, all places are considered,
          independently of the component.

        :returns: zone/region-regions and region-zone/region mappings.
        """
        areas = [area] if area is not None else self.areas
        src_area_place_regions = OrderedDict()
        for area in areas:
            if component_name is not None:
                # Check if component source is used by component
                area_context_components: tp.List[tp.Optional[
                    'e4clim.context.context_component.ContextComponent']] = [
                    cm for cm in self.med.context_components.values() if (
                        (cm.area == area) and
                        (cm.component_name == component_name) and
                        (src_name in cm.data_sources))]
            else:
                # Dummy dictionary
                area_context_components = [None]

            # Get place-regions mapping for area and data source
            if len(area_context_components) > 0:
                for place_name, src_regions in self.area_places_sources[
                        area].items():
                    if src_name in src_regions:
                        src_area_place_regions[
                            place_name] = tools.ensure_collection(src_regions[
                                src_name], list)

        # Get region-place mapping
        src_area_region_place = OrderedDict()
        for place_name, region_names in src_area_place_regions.items():
            for region_name in region_names:
                src_area_region_place[region_name] = place_name

        return src_area_place_regions, src_area_region_place

    def get_total_bounds(self, epsg: int = 4326,
                         **kwargs) -> tp.Sequence[float]:
        """Get array of min and max coordinates on each axis.

        :param epsg: EPSG code specifying output projection.

        :returns: Array with min x, min y, max x, max y.
        """
        data = self.get_data(
            variable_component_names=self.variable_component_names,
            **kwargs)[GEO_VARIABLE_NAME]

        # Transform to right CRS
        data_to_crs = data.to_crs(epsg=epsg) if epsg else data

        # Return total bounds
        return data_to_crs.total_bounds

    def read_place_coordinates(self, **kwargs) -> pd.DataFrame:
        """Read centroid coordinates of zones/regions.

        :returns: Centroid coordinates of places.
        """
        # Set filepath
        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon{}.csv'.format(
            self.get_data_postfix(with_src_name=True, **kwargs))
        filepath = Path(file_dir, filename)

        # Open and read coordinates from file
        with open(filepath, 'r') as f:
            df_coord_places = pd.read_csv(f, index_col=0)

        return df_coord_places

    def write_place_coordinates(self, **kwargs) -> None:
        """Write centroid coordinates of zones/regions."""
        # Get coordinates as data frame
        gdf = self[GEO_VARIABLE_NAME]
        df_coord = pd.DataFrame(index=gdf.index, columns=['lat', 'lon'])

        for place in gdf.index:
            # Get place centroid in source coordinates
            pt0 = gdf.loc[place].geometry.centroid

            # Convert to reference CRS
            pt = gpd.GeoSeries(pt0, crs=gdf.crs).to_crs(epsg=4326).values[0]
            df_coord.loc[place] = [pt.y, pt.x]

        # Set filepath
        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon{}.csv'.format(
            self.get_data_postfix(with_src_name=True, **kwargs))
        filepath = Path(file_dir, filename)

        # Write coordinates to file
        df_coord.to_csv(filepath)

    def _init_regions_places(self, **kwargs) -> None:
        """Set region-to-zone/region mapping :py:attr:`region_place`,
        zone/region-names list :py:attr:`place_names` and
        zone/region-to-regions mapping :py:attr:`place_regions`.

        .. note:: :py:attr:`areas` are to areas in
          `context_components_per_area` of mediator configuration, if defined,
          or to all areas in :py:attr:`area_places_sources`.

        .. seealso:: :py:meth:`_get_area_places_sources`.
        """
        # Get area and zones/regions description per data sources
        self.area_places_sources = self._get_area_places_sources(**kwargs)

        # Get all areas from components or all described areas
        areas = OrderedSet(self.med.cfg.get('context_components_per_area') or
                           self.area_places_sources)

        # Loop over areas to define places and regions
        self.area_places = OrderedDict()
        self.area_regions = OrderedDict()
        self.region_place = OrderedDict()
        self.place_regions = OrderedDict()
        self.place_names = []
        self.areas = OrderedSet()
        for area in areas:
            # Loop over place-source names pairs
            place_sources = self.area_places_sources.get(area)
            if place_sources is not None:
                for place_name, src_regions in place_sources.items():
                    # Try to get region names for this data source
                    if self.name in src_regions:
                        # Add area
                        self.areas.add(area)

                        # Add place to place names
                        self.place_names.append(place_name)

                        # Add place to area
                        self.area_places.setdefault(
                            area, []).append(place_name)

                        # Get place region-names.
                        region_names = tools.ensure_collection(
                            src_regions[self.name], list)

                        # If the region is not given assume same as place
                        if region_names is None:
                            region_names = [place_name]

                        # Add regions to area
                        if area not in self.area_regions:
                            self.area_regions[area] = []
                        for region_name in region_names:
                            self.area_regions[area].append(region_name)

                        # Add place-regions pair
                        self.place_regions[place_name] = tools.ensure_collection(
                            region_names, list)

                        # Add region-place pair
                        self.region_place.update(
                            {region_name: place_name
                             for region_name in region_names})

        # Get place-area mapping
        self.place_area = OrderedDict()
        for area, place_names in self.area_places.items():
            self.place_area.update(
                {place_name: area for place_name in place_names})

        # Get data-source region names
        self.region_names = list(self.region_place)

        # Get place indices
        self.place_indices = _get_place_indices(self.place_names, **kwargs)

    def _get_area_places_sources(self, **kwargs) -> AreaPlacesSourcesType:
        """Get zones/regions from file given by `places_filepath` entry of
        geo configuration.

        :returns: Places.
        """
        cfg_area_places_sources_filepath = tools.get_required_iterable_str_entry(
            self.med.geo_cfg, 'places_filepath', list)
        area_places_sources_filepath = Path(*cfg_area_places_sources_filepath)
        with open(area_places_sources_filepath, 'r') as f:
            area_places_sources = yaml.load(f, Loader=yaml.FullLoader)

        return area_places_sources


class GeoParsingDataSourceDefault(GeoParsingSingleDataSourceBase):
    """Default geographic data source."""

    def make_mask(self, data_src: GriddedDataSourceBase,
                  **kwargs) -> xr.Dataset:
        """Make mask for a given gridded data source, store the
        regions' geometries to :py:attr:`data` member.

        :param data_src: Gridded data source.

        :returns: Mask dataset.
        """
        return _make_mask(self, data_src, **kwargs)

    @abstractmethod
    def get_filename(self, area: str = None, **kwargs) -> e4tp.PathType:
        """Get filename abstract method.

        :param area: Area.

        :returns: Filename.
        """
        ...

    def read_file(self, area: str, **kwargs) -> gpd.GeoDataFrame:
        """Read downloaded geographical data for area.

        :param area: Geographical area for which to read the data.

        :returns: Geographic data frame.
        """
        src_dir = self.med.cfg.get_external_data_directory(
            self, makedirs=False, **kwargs)

        # Get directory for area
        filename = self.get_filename(area=area, **kwargs)
        filepath = Path(src_dir, filename)

        # Read geographical file for area
        read_file_kwargs = self.cfg.get('read_file_kwargs') or {}
        gdf_area = gpd.read_file(filepath, **read_file_kwargs)

        return gdf_area

    def parse(self, *args, **kwargs) -> tp.Mapping[str, gpd.GeoDataFrame]:
        """Parse geographical data for all areas.

        :returns: Geographical array with geometries.

        .. note:: The geographic data is aggregated by zone.
          A zone could be the region itself,
          in which case no aggregation is performed.

        """
        child_column = tools.get_required_str_entry(self.cfg, 'child_column')

        gdf = None
        for area in self.areas:
            # Read file
            gdf_area = self.read_file(area, **kwargs)

            # Handle parent/child columns
            if 'parent_column' in self.cfg:
                # Get country code
                country_code = get_country_code(area, code='alpha-2')

                # Select country
                gdf_area_sel = gdf_area[gdf_area.loc[
                    :, self.cfg['parent_column']] == country_code]

                # GB/UK exception
                if (country_code == 'GB') and (len(gdf_area_sel) == 0):
                    gdf_area_sel = gdf_area[gdf_area.loc[
                        :, self.cfg['parent_column']] == 'UK']

                gdf_area = gdf_area_sel

            # Index by child-column
            gdf_area = gdf_area.set_index(child_column)[['geometry']]

            region_names = self.area_regions[area]
            if (len(region_names) == 1) and (area in region_names):
                # Manage country case
                gdf_area.loc[:, 'zone'] = area
                gdf_area = gdf_area.dissolve(by='zone')
            else:
                # Select requested regions for area
                gdf_area = gdf_area.loc[region_names]

                # Aggregate by zone taking places from region-place mapping
                # to preserve order.
                gdf_area.loc[:, 'zone'] = [self.region_place[region_name]
                                           for region_name in gdf_area.index]
                gdf_area = gdf_area.dissolve(by='zone')

            # Merge area
            gdf = gdf_area if gdf is None else pd.concat([gdf, gdf_area])

        # Add variable data to data source
        self.update({GEO_VARIABLE_NAME: gdf})

        # Write coordinates of places' centroids
        self.write_place_coordinates(**kwargs)

        return {GEO_VARIABLE_NAME: gdf}

    def read(self, *args, **kwargs) -> None:
        """Read source dataset as :py:class:`geopandas.GeoDataFrame`
        from file.
        """
        if self.task_mng['read__{}'.format(GEO_VARIABLE_NAME)]:
            filepath = self.get_data_path(
                variable_name=GEO_VARIABLE_NAME, makedirs=False, **kwargs)

            self.info('Reading {} for {} from {}'.format(
                GEO_VARIABLE_NAME, self.name, filepath))
            self[GEO_VARIABLE_NAME] = gpd.read_file(filepath).set_index('zone')

            # Update task manager
            self.task_mng['read__{}'.format(GEO_VARIABLE_NAME)] = False

    def write(self, *args, **kwargs) -> None:
        """Write source :py:class:`geopandas.GeoDataFrame` dataset to file.
        """
        if self.task_mng.get('write__{}'.format(GEO_VARIABLE_NAME)):
            filepath = self.get_data_path(
                variable_name=GEO_VARIABLE_NAME, **kwargs)

            self.info('Writing {} for {} to {}'.format(
                GEO_VARIABLE_NAME, self.name, filepath))
            gdf = self.get(GEO_VARIABLE_NAME)
            assert gdf is not None, 'Data for "{}" variable required'.format(
                GEO_VARIABLE_NAME)

            gdf.reset_index().to_file(filepath)


class GeoParsingDataSourceDefaultDownload(
        GeoParsingDataSourceDefault, ABC):
    """Add default download method to default geographic data source."""

    #: Flag allowing several downloads per area.
    ONE_DOWNLOAD_PER_AREA: bool = False

    @ abstractmethod
    def get_url(self, area: str = None, **kwargs) -> str:
        """Get URL abstract method.

        :param area: Area.

        :returns: URL.
        """
        ...

    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> tp.MutableSet[str]:
        """Download geographic data defining geometries of areas/zones/regions.

        :returns: Names of downloaded variables.

        .. warning:: Requires :py:meth:`get_url` and :py:meth:`get_filename`
          methods to be implemented.
        """
        src_dir = self.med.cfg.get_external_data_directory(self, **kwargs)
        previous_urls = []
        for area in self.areas:
            # Get URL and filename for area
            url = self.get_url(area=area, **kwargs)
            filename = self.get_filename(area=area, **kwargs)

            # Prevent downloading non-area specific data multiple times
            if url not in previous_urls:
                # Download geographic data for area
                self.info(
                    'Downloading {} geographic data for {} from {}'.format(
                        self.name, area, url))
                download_from_url(url, filename, src_dir)

                if self.ONE_DOWNLOAD_PER_AREA:
                    # Prevent future downloads
                    previous_urls.append(url)

        return {GEO_VARIABLE_NAME}


def download_from_url(url: str, filename: e4tp.PathType,
                      src_dir: e4tp.PathType) -> None:
    """Download geographic data defining borders for areas/zones/regions
    and return geometries.

    :param url: URL from which to download data.
    :param filename: Downloaded-file name.
    :param src_dir: Data destination directory.

    .. note:: This function is not directly called from this module,
      but from API's included in this package(e.g. GISCO).
    """
    # Download data for region
    filepath = Path(src_dir, filename)
    r = requests.get(url)
    if r.status_code != 200:
        raise FileNotFoundError(url)

    # Extract, if needed, or write file
    if url[-4:] == '.zip':
        zip_ref = zipfile.ZipFile(BytesIO(r.content))
        zip_ref.extractall(src_dir)
        zip_ref.close()
    else:
        with open(filepath, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def get_country_code(area: str, code: str = 'alpha-2') -> str:
    """Get country code.

    :param area: Country name.
    :param code: Code name.

    :returns: Country code.
    """
    # Read country codes
    resource_name = '../data/iso_country_codes.csv'
    with resource_stream(__name__, resource_name) as stream:
        cc_data = pd.read_csv(stream, index_col=0)
    area_name = difflib.get_close_matches(
        area, cc_data.index.tolist(), n=1)[0]

    return cc_data.loc[area_name, code]


def _get_place_indices(place_names: e4tp.PlaceNamesType,
                       **kwargs) -> PlaceIndicesType:
    """Get place indices in mask.

    :param place_names: Place names.

    :returns: Index per place name.
    """
    # Create dictionary of places (independent of data grid)
    place_ids = list(range(2, len(place_names) + 2))
    place_indices = OrderedDict(zip(place_names, place_ids))

    return place_indices


def _make_mask(geo_src, data_src: GriddedDataSourceBase,
               **kwargs) -> xr.Dataset:
    """Make mask for a given gridded data source, store the
    regions' geometries to :py:attr:`data` member.

    :param geo_src: Geographic data source.
    :param data_src: Gridded data source.

    :returns: Mask dataset.
    """
    # Get regions' geometries
    geo_src.get_data(
        variable_component_names=geo_src.variable_component_names, **kwargs)

    # Select a single variable that has been downloaded if possible
    vcn = _get_data_src_vcn_to_make_mask(data_src)

    # Download data to read the grid
    data_src.manage_download(variable_component_names=vcn, **kwargs)

    # Get data coordinates
    coords = data_src.get_grid(**kwargs)

    # Get point region membership
    geo_src.info('Assigning points to regions')
    ds_mask = get_point_region_membership(
        geo_src.cfg, geo_src.get(GEO_VARIABLE_NAME), geo_src.place_indices,
        coords)

    # Add geographic data-source name
    ds_mask.attrs['data_source'] = geo_src.name

    return ds_mask


def _get_data_src_vcn_to_make_mask(
        data_src: GriddedDataSourceBase) -> e4tp.VCNStrictMutableType:
    """Get variable component names to make mask selecting a single
    variable that has already been downloaded if possible.

    :param data_src: Data source for which to make mask.

    :returns: Variable component names.
    """
    vcn: e4tp.VCNStrictMutableType
    if data_src.tasks is not None:
        download_tasks = {task: flag for task, flag in data_src.tasks.items()
                          if task.split('__')[0] == 'download'}
        vcn = {task.split('__')[-1]: set() for task, flag in download_tasks.items()
               if not flag}
        if not vcn:
            vcn = {list(download_tasks)[0].split('__')[-1]: set()}
    else:
        vcn = {list(data_src.variable_component_names)[0]: set()}

    return vcn
