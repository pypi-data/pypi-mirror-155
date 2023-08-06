"""Definition of modifier upsampling wind assuming Weibull distribution
with constant shape parameter."""
import numpy as np
from orderedset import OrderedSet
import pandas as pd
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.spatial import cKDTree
from scipy.special import gamma, erf, erfinv
from scipy.linalg import cholesky
from sklearn import linear_model
import xarray as xr
from e4clim.container.strategy import ExtractorBase
from e4clim.utils import tools
from e4clim.utils.climate import get_wind_magnitude


class Strategy(ExtractorBase):
    """Modifier upsampling wind assuming that intra-day distribution follows
    a Weibull distribution with mean given by daily-mean and with a constant
    constant shape parameter per grid-point.

    .. warning:: For performance, computed source parameters are
      adapted to the destination grid in :py:meth:`_adapt_to_dst_grid`
      only once. This implies that the destination grid should
      not change between applications of the modifier with :py:meth:`apply`.

    .. todo:: Finish managing several space dimensions by stacking if needed.
    """

    def __init__(self, parent, name, cfg=None, **kwargs):
        """Naming constructor.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        :type parent: :py:class:`ContextResult`
        :type name: str
        :type cfg: mapping
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

        #: Ratio-to-shape function.
        self.ratio_to_shape_fun = None
        #: Shape coefficients.
        self.shape = None
        #: Standard deviation-mean ratio.
        self.ratio = None
        #: Fit score.
        self.score = None
        #: Nearest-neighbors tree to interpolate between grids.
        self.nn_tree = None
        #: Shape coefficients per day on destination grid.
        self.shape_dst_day = None
        #: Correlation matrix.
        self.corr = None
        #: Correlation matrix after conversion to normal distribution.
        self.corr_norm = None
        #: Nearest-neighbors index from :py:func:`numpy.unique`.
        self.nn_idx = None
        #: Nearest-neighbors inverse-index from :py:func:`numpy.unique`.
        self.nn_idx_unique_inverse = None
        #: Correlation-matrix after conversion to normal distribution
        #: on destination grid.
        self.corr_norm_dst_unique = None
        #: Lower-triangular matrix from Cholesky decomposition of
        #: correlation-matrix for normal distributions on destination grid.
        self.ltri_corr_norm_dst_unique = None
        #: Whether adaptation to destination grid is needed.
        self._adapt = True
        #: Number of hours in a day.
        self._n_hours = 24
        #: Space-dimension name.
        self._space_dim = 'stacked_dim'

        # Add initialization task
        self.task_mng.update({'make': True})

        # Get ratio to shape function
        shape_minmax = (1., 10.)
        shape_rng = np.arange(*shape_minmax, 0.01)
        ratio_rng = shape_to_ratio(shape_rng)
        self.ratio_to_shape_fun = interp1d(
            ratio_rng, shape_rng, kind='cubic', fill_value=shape_minmax,
            bounds_error=False)

    def update_input_variable_names(self,  **kwargs):
        """Add input variable names."""
        #: Required input-variables.
        self.input_variable_names = OrderedSet([
            'zonal_wind', 'meridional_wind'])

        # Define variable to component names
        self.input_variable_component_names = {
            variable_name: OrderedSet([self.parent.parent.component_name])
            for variable_name in self.input_variable_names}

    def make(self, time_dim_name='time', **kwargs):
        """Compute shape parameter per grid-point and correlation matrix."""
        filename = '{}{}.nc'.format(
            self.name, self.get_extractor_postfix(**kwargs))
        file_dir = self.med.cfg.get_project_data_directory(self)
        filepath = Path(file_dir, filename)

        if self.task_mng.get('make'):
            # Get data source to make modifier
            data_src = self.data_sources['make']
            self.info(
                'Making {} modifier from {} data source'.format(
                    self.name, data_src.name))

            # Make mask for gridded data source (loading input data)
            data_src.get_structured_mask(**kwargs)

            # Functions to apply to gridded data
            functions = [data_src.crop_area, get_wind_magnitude]

            # Get dataset with wind magnitude
            ds = data_src.parse_finalize(
                transform=tools.Composer(*functions),
                variable_component_names=self.input_variable_component_names)
            da = ds['wind_magnitude']

            # Get source dataset spatial coordinates
            space_coord = ds.coords[self._space_dim]
            n_gp = len(space_coord)

            # Get group of hours for each day
            gp = da.resample(**{time_dim_name: 'D'})

            # Get mean and standard deviation
            da_mean = gp.mean(time_dim_name)
            da_std = gp.std(time_dim_name)

            # Get high-passed intraday time series
            da_daily = da_mean.reindex(time=da.indexes[time_dim_name],
                                       method='ffill')
            da_intraday = da - da_daily

            # Get intra-day correlation-matrix of Weibull variables
            self.corr = xr.DataArray(
                np.corrcoef(da_intraday, rowvar=False), coords=[
                    (self._space_dim + '_i', range(n_gp)),
                    (self._space_dim + '_j', range(n_gp))])

            # Initialize regressor
            reg = linear_model.LinearRegression()

            # Initialize shape and score
            da_snapshot = da_mean.isel(**{time_dim_name: 0}, drop=True)
            self.shape = xr.zeros_like(da_snapshot)
            self.ratio = xr.zeros_like(da_snapshot)
            self.score = xr.zeros_like(da_snapshot)

            # Compute shape at each location
            scale_daily = xr.full_like(da_mean, None)
            for xi in space_coord:
                self._get_shape_at_loc({space_coord.name: xi},
                                       da_mean, da_std, reg)

            # Get hourly-sampled daily shape parameter for each grid point
            scale_daily = get_weibull_scale_from_mean_shape(
                da_mean, self.shape)
            scale_daily = scale_daily.reindex(time=da.indexes[time_dim_name],
                                              method='ffill')

            # Convert assumed Weibull random-variables to standard ones
            # This means than all daily means are zero, or high-pass filtered
            da_norm = weibull_to_normal(da, scale_daily, self.shape)

            # Get multivariate normal correlation matrix
            self.corr_norm = xr.DataArray(
                np.corrcoef(da_norm, rowvar=False), coords=[
                    (self._space_dim + '_i', range(n_gp)),
                    (self._space_dim + '_j', range(n_gp))])

            # Create dataset to write
            ds = xr.Dataset({
                'shape': self.shape, 'ratio': self.ratio, 'score': self.score,
                'corr': self.corr, 'corr_norm': self.corr_norm})

            # Unstack if needed
            if 'stacked_dim' in ds.dims:
                ds_us = ds.unstack('stacked_dim')
                ds_us.attrs['stacked'] = 1
            else:
                ds_us = ds

            # Write datset
            ds_us.to_netcdf(filepath)

            # Update task manager
            self.task_mng['make'] = False
        else:
            self.info('{} modifier already initialized: reading '
                      'from {}'.format(self.name, filepath))
            # Read dataset and copy to unlock
            ds_us = xr.load_dataset(filepath)

            # Stack if needed
            if ds_us.attrs.get('stacked'):
                ds = ds_us.stack(stacked_dim=['lat', 'lon']).dropna(
                    'stacked_dim')
            else:
                ds = ds_us

            # Set attributes
            self.shape = ds['shape']
            self.ratio = ds['ratio']
            self.score = ds['score']
            self.corr = ds['corr']
            self.corr_norm = ds['corr_norm']

        # Get source-grid spatial coordinates
        self.src_latlon = np.array([self.shape['lat'],
                                    self.shape['lon']]).T

        # Create nearest neighbor tree for source grid
        self.nn_tree = cKDTree(self.src_latlon)

    def transform(self, ds: xr.Dataset = None,
                  time_dim_name: str = 'time', **kwargs) -> xr.Dataset:
        """Upsample dataset. Wind is upsampled using i.i.d.
        realisations of a Weibull distribution with constant scale
        parameter computed from an hourly data source with :py:meth:`make`.
        All other variables are trivially up-sampled.

        :param ds: Dataset containing daily-mean wind-magnitude.

        :returns: Upsampled dataset.

        .. note:: The interpolation from the source data grid
          to the destination data grid uses neirest neighbors.
          if the the destination grid is thinner than the source
          grid, this will result is a positive semi-definite matrix,
          thus preventing the Cholesky decomposition. To avoid this,
          the correlation matrix for the subset of independent variables
          is computed (by counting a neighbor only once). The normal
          variables are then computed and repeated to match the original
          number of destination variables.

        .. warning:: Datasets should contain `'lat'` and `'lon'`
          coordinates.
        """
        assert ds is not None, '"ds" argument should be given here'

        # Make modifier
        self.update_input_variable_names(**kwargs)
        self.make(**kwargs)
        self.info('Up-sampling dataset with {} modifier'.format(
            self.name))

        # Select wind magnitude
        da = ds['wind_magnitude']

        # Upsample other variables
        td = ds.indexes[time_dim_name]
        delta_day = pd.Timedelta(self._n_hours - 1, unit='H')
        th = pd.date_range(start=td[0], freq='H', end=td[-1] + delta_day)
        ds_up = ds.resample(time='H').ffill().reindex(time=th, method='ffill')
        da_up = da.reindex(time=th)
        dst_space_coord = da.coords[self._space_dim]
        da_snapshot = da_up.isel(**{time_dim_name: 0}, drop=True)

        # Adapt modifier parameters to destination grid if needed
        self._adapt_to_dst_grid(da_snapshot)

        # Generate samples for each day
        for date in da.indexes[time_dim_name]:
            # Get mean wind-magnitude for a given date
            da_day_mean = da.sel(**{time_dim_name: date}, drop=True)

            # Create time index for the day
            time_day = pd.date_range(
                start=date, end=(date + delta_day), freq='H')
            coord_time_day = (time_dim_name, time_day)

            # Get scale parameters for this date on destination grid
            scale_dst_day = get_weibull_scale_from_mean_shape(
                da_day_mean, self.shape_dst)

            # Sample independent multivariate-standard samples
            n_gp_unique = self.ltri_corr_norm_dst_unique.shape[0]
            norm_sample_iid_unique = np.random.normal(
                size=(len(time_day), n_gp_unique))

            # Get correlated multivariate-standard samples
            nsc_unique = np.dot(self.ltri_corr_norm_dst_unique,
                                norm_sample_iid_unique.T).T

            # Duplicate independent variables which are not unique
            nsc = nsc_unique[:, self.nn_idx_unique_inverse]
            normal_sample_corr = xr.DataArray(
                nsc, coords=[coord_time_day, dst_space_coord])

            # Convert to Weibull random variables
            weibull_sample_corr = normal_to_weibull(
                normal_sample_corr, scale_dst_day, self.shape_dst_day)

            # Add day to upsampled array
            da_up.loc[{time_dim_name: slice(
                time_day[0], time_day[-1])}] = weibull_sample_corr.transpose(
                    time_dim_name, self._space_dim)

        ds_up['wind_magnitude'] = da_up

        return ds_up

    def get_extractor_postfix(self, **kwargs):
        """Get climate modifier postfix.

        returns: Postfix.
        rtype: str
        """
        data_src = self.data_sources['make']
        return '{}_upsample_weibull_{}{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            data_src.name, data_src.get_data_postfix(**kwargs))

    def _get_shape_at_loc(self, loc, da_mean, da_std, reg):
        """Estimate shape parameter at location."""
        # Fit
        da_mean = da_mean.where(~(da_mean.isnull() | np.isinf(da_mean)), 0)
        da_std = da_std.where(~(da_std.isnull() | np.isinf(da_std)), 0)
        X = da_mean.loc[loc].expand_dims('variable', 1).values
        y = da_std.loc[loc].values
        reg.fit(X, y)

        # Convert ratio to shape and store score
        self.ratio.loc[loc] = reg.coef_[0]
        self.shape.loc[loc] = self.ratio_to_shape_fun(
            reg.coef_[0])
        self.score.loc[loc] = reg.score(X, y)

    def _interpolate_shape_correlation(self, space_coord):
        """Interpolate Weibull-shape and standard-correlation parameters.

        :param space_coord: Spacial coordinate.
        :type space_coord: :py:class:`xarray.DataArray`
        """
        # if self.shape._level_coords:
        # Get destination-grid spatial coordinates
        dst_latlon = np.array([space_coord['lat'].values,
                               space_coord['lon'].values]).T

        # Get all neirest neighbors indices if needed
        if self.nn_idx is None:
            self.nn_idx = np.empty((len(dst_latlon),), dtype=int)
            for i in range(len(dst_latlon)):
                self.nn_idx[i] = self.nn_tree.query(dst_latlon[i])[1]

        # Get unique indices, in case upsampling grid
        self.nn_idx_unique, self.nn_idx_unique_inverse = np.unique(
            self.nn_idx, return_inverse=True)
        space_coord_unique = space_coord[self.nn_idx_unique]
        sc = range(len(space_coord_unique))

        # Interpolate weibull shape and standard correlation parameters
        self.shape_dst = xr.DataArray(self.shape[self.nn_idx],
                                      coords=[space_coord])
        self.corr_norm_dst_unique = xr.DataArray(
            self.corr_norm[self.nn_idx_unique, self.nn_idx_unique],
            coords=[(space_coord.name + '_unique_i', sc),
                    (space_coord.name + '_j', sc)])

        # else:
        #     # Linear interpolation for gridded data
        #     shape_dst = self.shape.interp_like(da_snapshot, method='linear')

    def _adapt_to_dst_grid(self, da):
        """Adapt modifier parameters to grid of given array.

        :param da: Array with space coordinates to which to adapt
          attributes.
        :type da: :py:class:`xarray.DataArray`
        """
        if self._adapt:
            # Get space coordinate
            space_coord_dst = da.coords[self._space_dim]

            # Interpolate scale parameters from source to destination grid
            self._interpolate_shape_correlation(space_coord_dst)

            # Tile shape along hours
            tile_dims = (self._n_hours,) + (1,) * len(da.shape)
            self.shape_dst_day = np.tile(self.shape_dst, tile_dims)

            # Get Cholesky decomposition
            ltri = cholesky(self.corr_norm_dst_unique,
                            lower=True, check_finite=False)
            self.ltri_corr_norm_dst_unique = xr.DataArray(
                ltri, coords=self.corr_norm_dst_unique.coords)

            # Prevent adapting in the future
            self._adapt = False


def shape_to_ratio(shape):
    """Get standard deviation-mean ratio of Weibull distribution for
    a given shape parameter.
    """
    return np.sqrt(gamma(1 + 2. / shape) / gamma(1 + 1. / shape)**2 - 1.)


def normal_to_weibull(normal_samples, weibull_scale, weibull_shape,
                      normal_loc=0., normal_scale=1.):
    """Transform univariate normally distributed samples to
    Weibull distributed samples.

    :param normal_samples: Normally distributed samples.
    :param weibull_scale: Scale parameter of destination Weibull distribution.
    :param weibull_shape: Shape parameter of destination Weibull distribution.
    :param normal_loc: Mean of source normal distribution.
    :param normal_scale: Standard deviation of source normal distribution.
    :type normal_samples: :py:class:`float`, collection
    :type weibull_scale: :py:class:`float`, collection
    :type weibull_shape: :py:class:`float`, collection
    :type normal_loc: :py:class:`float`, collection
    :type normal_scale: :py:class:`float`, collection

    :returns: Weibull-distributed samples.
    :rtype: :py:class:`float`, collection
    """
    return weibull_scale * (-np.log(
        (1 - erf((normal_samples - normal_loc) /
                 (np.sqrt(2) * normal_scale))) / 2))**(1. / weibull_shape)


def weibull_to_normal(weibull_samples, weibull_scale, weibull_shape,
                      normal_loc=0., normal_scale=1., threshold=1.e-6):
    """Transform univariate Weibull-distributed samples to
    normally distributed samples.

    :param normal_samples: Weibull-distributed samples.
    :param weibull_scale: Scale parameter of destination Weibull distribution.
    :param weibull_shape: Shape parameter of destination Weibull distribution.
    :param normal_loc: Mean of source normal distribution.
    :param normal_scale: Standard deviation of source normal distribution.
    :param threshold: Distance below (above) 1 (-1) for after which values
      given to the inverse error function are clipped to avoid infinite values.
    :type normal_samples: :py:class:`float`, collection
    :type weibull_scale: :py:class:`float`, collection
    :type weibull_shape: :py:class:`float`, collection
    :type normal_loc: :py:class:`float`, collection
    :type normal_scale: :py:class:`float`, collection
    :type threshold: float

    :returns: Normally distributed samples.
    :rtype: :py:class:`float`, collection
    """
    # Clip values close to zero to avoid infinity in wtn
    da = 1 - 2 * np.exp(-(weibull_samples / weibull_scale)**weibull_shape)
    da_clip = xr.where(da < 1. - threshold, da, 1. - threshold)
    da_clip = xr.where(da_clip > -1. + threshold, da_clip, -1. + threshold)

    return np.sqrt(2) * normal_scale * erfinv(da_clip) + normal_loc


def get_weibull_scale_from_mean_shape(mean, shape):
    """Get Weibull scale parameter from mean and
    shape parameter.

    :param mean: Mean of Weibull distribution.
    :param shape: Shape parameter of Weibull distribution.
    :type mean: :py:class:`float`, collection
    :type shape: :py:class:`float`, collection

    :returns: Scale parameter of Weibull distribution:
    :rtype: :py:class:`float`, collection
    """
    return mean / gamma(1. + 1. / shape)
