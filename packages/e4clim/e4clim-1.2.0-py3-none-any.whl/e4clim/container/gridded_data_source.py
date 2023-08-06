"""Gridded-data base definitions."""
from abc import ABC, abstractmethod
from collections import OrderedDict
from cartopy.crs import CRS
from copy import deepcopy
import iris
import numpy as np
from pathlib import Path
from scipy.spatial import cKDTree
import typing as tp
import xarray as xr
import e4clim
import e4clim.typing as e4tp
from .parsing_single_data_source import ParsingSingleDataSourceBase


#: Default dimensions.
DEFAULT_DIMS: tp.Final[tp.Tuple[str, str]] = 'lat', 'lon'


class GriddedDataSourceBase(ParsingSingleDataSourceBase, ABC):
    """Gridded data-source abstract base class. Requires :py:meth:`get_grid`
    method to be implemented."""

    #: Geographic data source.
    geo_src: tp.Optional[
        'e4clim.container.geo_data_source.GeoDataSourceBase']

    #: Geographic dimensions. Default values.
    _dims: tp.Tuple[str, str]

    #: Mask.
    mask: xr.Dataset

    #: Mask for area.
    mask_for_area: tp.Optional[xr.Dataset]

    #: Points in area.
    points_in_area: xr.DataArray

    #: Stacked flags for grid points in area.
    _is_in_stack: xr.DataArray

    #: Gridded dataset.
    gridded: bool = True

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize setting gridded to `True`.

        :param parent: Data-sources context.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        super(GriddedDataSourceBase, self).__init__(
            parent, name, cfg=cfg, **kwargs)

        self.geo_src = self.med.geo_src

        # Set to default dimensions (can be changed by children)
        self._dims = DEFAULT_DIMS

        # Add get_mask task
        self.task_mng['get_mask'] = True

        self.mask_for_area = None

    @property
    def dims(self) -> tp.Tuple[str, str]:
        """Get dimensions."""
        return self._dims

    def get_grid(self, *args, **kwargs) -> e4tp.CoordsType:
        """Return data-source grid used to make mask.

        :returns: Dataset coordinates.
        """
        filepath = self.get_grid_filepath(*args, **kwargs)

        self.info('Reading sample {} data from {}'.format(self.name, filepath))
        with xr.open_dataset(filepath) as ds:
            lat = ds.get('lat')
            if lat is None:
                lat = ds.get('latitude')
            lon = ds.get('lon')
            if lon is None:
                lon = ds.get('longitude')

            # Get grid coordinates
            coords = (lat.copy(deep=True).coords
                      if len(lat.shape) > 1 else
                      OrderedDict({
                          'lat': lat.copy(deep=True).values,
                          'lon': lon.copy(deep=True).values}))

        return coords

    @abstractmethod
    def get_grid_filepath(self, *args, **kwargs) -> Path:
        """Return grid filepath.

        :returns: Grid filepath.
        """
        ...

    def get_mask(
            self, ds: xr.Dataset = None, for_area: bool = None,
            **kwargs) -> xr.Dataset:
        """Get structured mask or mask for area.

        :param ds: Gridded dataset from which to infer whether the grid
          is stacked (for area) or not.
        :param for_area: Whether the grid is for the area or not.

        :returns: Mask.

        :raises AssertionError: if :py:obj:`ds` and :py:obj:`stacked`
          arguments are both `None`.
        """
        if for_area is None:
            assert ds is not None, (
                'Either "ds" or "for_area" argument required')

            for_area = 'stacked_dim' in ds.coords

        if for_area:
            # Get stacked mask
            self.get_mask_for_area(**kwargs)
            mask = self.mask_for_area
        else:
            # Get mask
            self.get_structured_mask(**kwargs)
            mask = self.mask

        assert mask is not None, '"mask" is None'

        return mask

    def get_structured_mask(self, **kwargs) -> None:
        """Get structured mask from :py:attr:`geo_src` for the given
        gridded data source and store it in :py:attr:`mask` data-source member.
        """
        assert self.geo_src is not None, (
            '"geo_src" attribute of "med" attribute required')

        # Get the mask
        if self.task_mng.get('get_mask'):
            # Make the mask
            self.info('Making {} mask for {}'.format(
                self.geo_src.name, self.name))
            kwargs_new = deepcopy(kwargs)
            kwargs_new['data_src'] = self
            self.mask = self.geo_src.make_mask(**kwargs_new)

            # Save the mask
            self.write_mask(**kwargs_new)

            # Update task manager
            self.task_mng['get_mask'] = False
        else:
            # Read mask
            self.info('{} mask for {} already made'.format(
                self.geo_src.name, self.name))
            self.read_mask(**kwargs)

    def get_mask_for_area(self, **kwargs) -> None:
        """Get stacked mask for area from :py:attr:`geo_src`
        for the given gridded data source and store it in
        :py:attr:`mask_for_area` data-source member.

        .. seealso:: :py:meth:_get_points_in_area
        """
        if self.mask_for_area is None:
            # Get mask
            self.get_structured_mask(**kwargs)

            # Get points in area
            self._get_points_in_area(**kwargs)

            # Store stacked mask
            self.mask_for_area = self.mask.stack(stacked_dim=self.dims)[
                {'stacked_dim': self._is_in_stack}]

    def get_grid_postfix(self, **kwargs) -> str:
        """Return empty grid postfix string.

        returns: Grid postfix.
        """
        return ''

    def get_mask_postfix(self, **kwargs) -> str:
        """Get mask postfix for data source.

        :returns: Postfix
        """
        assert self.geo_src is not None, (
            '"geo_src" attribute of "med" attribute required')

        grid_postfix = self.get_grid_postfix(**kwargs)
        geo_postfix = self.geo_src.get_data_postfix(**kwargs)
        postfix = '_{}{}_{}{}'.format(
            self.geo_src.name, geo_postfix, self.name, grid_postfix)

        return postfix

    def get_mask_path(self, makedirs: bool = True, **kwargs) -> Path:
        """Get mask file path for data source.

        :param makedirs: Make directories if needed.

        :returns: Filepath.
        """
        file_dir = self.med.cfg.get_project_data_directory(
            self, makedirs=makedirs, **kwargs)
        filename = 'mask{}'.format(self.get_mask_postfix(**kwargs))
        filepath = Path(file_dir, filename)

        return filepath

    def read_mask(self, **kwargs) -> None:
        """Default implementation: read mask dataset as
        :py:class:`xarray.Dataset`.
        """
        assert self.geo_src is not None, (
            '"geo_src" attribute of "med" attribute required')

        filepath = '{}.nc'.format(self.get_mask_path(makedirs=False, **kwargs))
        self.info('Reading {} mask for {} from {}'.format(
            self.geo_src.name, self.name, filepath))
        self.mask = xr.load_dataset(filepath)

    def write_mask(self, **kwargs) -> None:
        """Default implementation: write mask as
        :py:class:`xarray.Dataset` to netcdf.
        """
        assert self.geo_src is not None, (
            '"geo_src" attribute of "med" attribute required')

        filepath = '{}.nc'.format(self.get_mask_path(**kwargs))
        self.info('Writing {} mask for {} to {}'.format(
            self.geo_src.name, self.name, filepath))
        self.mask.to_netcdf(filepath)

    def get_regional_mean(
            self, ds: xr.Dataset = None, **kwargs) -> e4tp.DatasetType:
        """Average dataset over regions given by mask.

        :param ds: Dataset to average.

        :returns: Dataset containing regional means.

        :raises AssertionError: if :py:obj:`ds` argument is `None`.
        """
        assert ds is not None, '"ds" argument required'

        self.info('Getting regional averages on {} grid'.format(self.name))

        mask = self.get_mask(ds=ds)

        # Get regional mean
        gp = ds.groupby(mask['mask'])

        # Get group means
        res = gp.mean(gp._group_dim, keep_attrs=True)

        # Remove unnecessary regions out of non-empty ones
        # and replace coordinates
        (filled_indices, idx1, idx2) = np.intersect1d(
            mask['region_index'].values, list(gp.groups),
            return_indices=True)
        res = res.loc[{'mask': filled_indices}]
        res = res.rename(mask='region')
        res['region'] = mask['region'].values[idx1]

        # Transpose region and time dimensions,
        # keeping other dimensions behind
        dim_list = list(res.dims)
        dim_list.remove('region')
        dim_list.insert(0, 'region')
        dim_list.remove('time')
        dim_list.insert(0, 'time')
        res = res.transpose(*dim_list)

        return res

    def get_total_mean(self, ds: xr.Dataset, **kwargs) -> xr.Dataset:
        """Average dataset over all grid points,
        independently of mask.

        :param ds: Dataset to average.

        :returns: Dataset containing mean.
        """
        self.info('Getting {} total mean'.format(self.name))

        # Group dimensions may either original or stacked ones
        try:
            res = ds.mean(self.dims, keep_attrs=True)
        except ValueError:
            res = ds.mean(ds.stacked_dim, keep_attrs=True)

        return res

    def crop_area(self, ds: xr.Dataset = None, **kwargs) -> e4tp.DatasetType:
        """Crop :py:obj:`ds` for data source
        over area covered by mask regions.

        :param ds: Dataset to crop.

        :returns: Cropped dataset.

        :raises AssertionError: if :py:obj:`ds` argument is `None`.

        .. seealso:: :py:meth:get_mask_for_area
        """
        assert ds is not None, '"ds" argument required'

        self.info('Cropping area for {}'.format(self.name))

        # Make mask for area
        self.get_mask_for_area(**kwargs)

        # Select region, removing other points
        res = ds.stack(stacked_dim=self.dims)[
            {'stacked_dim': self._is_in_stack.values}]

        return res

    def _get_points_in_area(self, **kwargs) -> None:
        """Get grid points in area."""
        if ((not hasattr(self, 'points_in_area')) or
                (not hasattr(self, '_is_in_stack'))):
            is_in = xr.zeros_like(self.mask['mask'], dtype=bool)
            for reg_idx in self.mask.region_index.astype(float).values:
                is_in |= (self.mask['mask'] == reg_idx)

            # Add points in area mask to regional mask dataset
            self.points_in_area = is_in

            self._is_in_stack = self.points_in_area.stack(
                stacked_dim=self.dims)


def crop_area(data_src: GriddedDataSourceBase, ds: xr.Dataset = None,
              **kwargs) -> e4tp.DatasetType:
    """Crop :py:obj:`ds` for data source
    over area covered by mask regions for given gridded data source.

    :param data_src: Data source.
    :param ds: Dataset to crop.

    :returns: Cropped dataset.

    :raises AssertionError: if :py:obj:`ds` argument is `None`.

    .. seealso:: :py:meth:get_mask_for_area
    """
    assert ds is not None, '"ds" argument required'

    data_src.info('Cropping area for {}'.format(data_src.name))

    # Make mask for area
    data_src.get_mask_for_area(**kwargs)

    # Select region, removing other points
    res = ds.stack(stacked_dim=data_src.dims)[
        {'stacked_dim': data_src._is_in_stack.values}]

    return res


def get_geodetic_crs(cube: 'iris.cube.Cube') -> tp.Tuple[
        tp.List['iris.coords.DimCoord'], tp.Optional[CRS], tp.Optional[CRS]]:
    """Get geodetic Coordinate Reference System (CRS) from arbitrary system.

    :param cube: Iris cube from which to manage grids associated with
      dataset.

    :returns: Longitudes and latitudes, source CRS and geodetic CRS.

    .. seealso:: :py:func:`get_geodetic_array`
    """
    # Get the coordinate system
    cs = cube.coord_system()

    # Get coordinates
    coords = [cube.coord('grid_longitude'), cube.coord('grid_latitude')]

    # Check if coordinate system is defined
    if cs is None:
        return coords, None, None

    # Get source CRS
    src_crs = cs.as_cartopy_crs()

    # Get geodetic CRS
    dst_crs = src_crs if src_crs.is_geodetic() else src_crs.as_geodetic()

    return coords, src_crs, dst_crs


def get_geodetic_array(ds: xr.Dataset, coords: 'iris.coords.DimCoord',
                       src_crs: CRS, dst_crs: CRS) -> xr.Dataset:
    """ Return an array from a file making sure that geodetic longitudes
    `lon` and latitudes `lat` are included.

    :param ds: Original dataset.

    :returns: Geodetic array.

    .. seealso:: :py:func:`get_geodetic_crs`
    """
    if ('lat' not in ds.coords) or ('lon' not in ds.coords):
        # Get source grid
        x, y = coords[0].points, coords[1].points
        if x.shape != y.shape:
            x, y = np.meshgrid(x, y)

        # Convert coordinates to geodetic
        dst_coords = dst_crs.transform_points(src_crs, x, y)

        # Add the coordinates to the array
        coords_names = [c.variable_name for c in coords]
        src_coords = [(cn, ds.coords[cn]) for cn in coords_names[::-1]]
        ds.coords['lon'] = xr.DataArray(dst_coords[:, :, 0],
                                        coords=src_coords)
        ds.coords['lat'] = xr.DataArray(dst_coords[:, :, 1],
                                        coords=src_coords)

    return ds


def get_nearest_neighbor(
        ds: e4tp.XArrayDataType, ref_lat: float, ref_lon: float,
        lat_label: str = 'lat', lon_label: str = 'lon',
        nn_tree: cKDTree = None, drop: bool = False,
        **kwargs) -> e4tp.XArrayDataType:
    """Evaluate dataset at point nearest to the given point.

    :param ds: Dataset to evaluate.
    :param ref_lat: Reference-point latitude.
    :param ref_lon: Reference-point longitude.
    :param lat_label: Label of latitude coordinate in dataset.
    :param lon_label: Label of longitude coordinate in dataset.
    :param nn_tree: Nearest-neighbor tree.
      in which case it is computed for the dataset grid.
    :param drop: Whether to drop horizontal dimensions.

    :returns: Selected data.
    """
    if nn_tree is None:
        # Get dataset latitude and longitudes
        LAT, LON = ds[lat_label].values, ds[lon_label].values
        if len(LAT.shape) == 1:
            LAT, LON = np.meshgrid(LAT, LON)
        lat, lon = LAT.flatten(), LON.flatten()
        ds_latlon = np.array([lat, lon]).T

        # Create nearest neighbor tree
        nn_tree = cKDTree(ds_latlon)

    # Get nearest neighbor
    ref_latlon = np.array([ref_lat, ref_lon])
    nn_dist, nn_idx = nn_tree.query(ref_latlon)

    # Select data using where in case lat/lon not coordinates
    nn_latlon = ds_latlon[nn_idx]
    ds_nn = ds.where((ds[lat_label] == nn_latlon[0]) &
                     (ds[lon_label] == nn_latlon[1]), drop=True)

    # Squeeze horizontal coordinates
    ds_nn = ds_nn.squeeze(drop=drop)

    ds_nn.attrs['nearest_neighbor_index'] = nn_idx
    ds_nn.attrs['nearest_neighbor_distance'] = nn_dist

    return ds_nn
