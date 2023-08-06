from shapely.geometry import MultiPoint
import numpy as np
import typing as tp
import xarray as xr
import geopandas as gpd
from e4clim import container
import e4clim.typing as e4tp

#: WGS84 CRS.
CRS_WGS84: tp.Final[int] = 4326


def get_point_region_membership(
        cfg_src: e4tp.CfgType, gdf: gpd.GeoDataFrame,
        place_indices: 'container.geo_data_source.PlaceIndicesType',
        coords: e4tp.CoordsType) -> xr.Dataset:
    """Assign grid-points of dataset to electricity places.

    :param cfg_src: Data-source configuration.
    :param gdf: Regions' geometries.
    :param place_indices: Dictionary assigning each plae name to a place ID.
      IDs of places of interest should be larger or equal to 2.
    :param coords: Input data coordinates assigned to electricity places.

    :returns: Dataset containing mask assigning each grid-point to a place.
    """
    ds = _get_empty_mask(coords)

    # Add region indices
    coords_region = ('region', list(place_indices.keys()))
    ds['region_index'] = xr.DataArray(
        list(place_indices.values()), coords=[coords_region])

    points = _get_coord_points_in_crs(ds, gdf.crs)

    # Assign points to regions
    for ipt, pt in enumerate(points):
        # Select place to which this point belongs to, if any
        within = gdf.contains(pt)
        if within.any():
            # Get place name
            zone = gdf[within].index[0]

            # Get corresponding zone and save zone ID in mask
            # If region in no zone, set to 1
            iy, ix = np.unravel_index(ipt, ds['mask'].shape)
            ds['mask'][iy, ix] = place_indices[zone] if zone else 1

    # Remove empty regions
    idx_filled = np.in1d(ds.region_index, np.unique(ds.mask))
    ds = ds.loc[{'region': idx_filled}]

    return ds


def _get_empty_mask(coords: e4tp.CoordsType) -> xr.Dataset:
    """Get empty mask with electricity-places coordinate.

    :param coords: Input data coordinates assigned to electricity places.

    return: Dataset.
    """
    ds = xr.Dataset()

    # Get dims and coords for regular and irregular grids
    if isinstance(coords, xr.core.coordinates.Coordinates):
        dim_names = list(coords.dims)
        dims = tuple(coords[dim].shape[0] for dim in dim_names)
        nd_mask = np.zeros(dims, dtype=int)
        ds['mask'] = xr.DataArray(nd_mask, dims=dim_names, coords=coords)
    else:
        dim_names = list(coords)
        dims = tuple(len(v) for v in coords.values())
        nd_mask = np.zeros(dims, dtype=int)
        coords_safe = tp.cast(tp.Mapping[tp.Hashable, tp.Any], coords)
        ds['mask'] = xr.DataArray(nd_mask, dims=dim_names, coords=coords_safe)

    return ds


def _get_coord_points_in_crs(ds: xr.Dataset, crs: str) -> gpd.GeoSeries:
    """Get geographic series of points corresponding to the `'lon'` and `'lat'`
    coordinates of the dataset and convert them to given CRS.

    :param ds: Dataset from which to get coordinate points.
    :param crs: Destination CRS.

    :returns: Geographic series of points.
    """
    if len(ds['lon'].shape) > 1:
        lon, lat = ds['lon'].values, ds['lat'].values
    else:
        lon, lat = np.meshgrid(ds['lon'], ds['lat'])
    mp = MultiPoint(list(zip(lon.flatten(), lat.flatten())))

    return gpd.GeoSeries(list(mp.geoms), crs=CRS_WGS84).to_crs(crs)
