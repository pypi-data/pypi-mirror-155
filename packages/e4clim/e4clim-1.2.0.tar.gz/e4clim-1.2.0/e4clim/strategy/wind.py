"""Wind-farm model definition."""
import numpy as np
import pandas as pd
from pkg_resources import resource_stream
from scipy.interpolate import interp1d
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.gridded_data_source import GriddedDataSourceBase
from e4clim.container.strategy import ExtractorBase
import e4clim.typing as e4tp
from e4clim.utils.climate import (
    get_air_density_at_height, get_wind_at_height, get_wind_magnitude)
from e4clim.utils.learn import get_transform_function

#: Available-dataset names.
VARIABLE_NAMES: tp.Final[tp.Set[str]] = {'generation', 'capacityfactor'}


class Strategy(ExtractorBase):
    """Wind-farm model."""
    #: Default result name.
    DEFAULT_RESULT_NAME: tp.Final[str] = 'capacityfactor'

    #: Cut-in speed.
    cut_in_speed: tp.Optional[xr.DataArray]
    #: Cut-out speed.
    cut_out_speed: tp.Optional[xr.DataArray]
    #: Power-curve powers.
    power_curve: tp.Optional[xr.DataArray]
    #: Power-curve function.
    power_fun: tp.Optional[xr.DataArray]
    #: Rated power.
    rated_power: tp.Optional[xr.DataArray]
    #: Rated-power speed.
    rated_power_speed: tp.Optional[xr.DataArray]
    #: Power-curve speeds.
    speed_curve: tp.Optional[xr.DataArray]

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        if parent.name != self.DEFAULT_RESULT_NAME:
            self.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    parent.result_name, self.DEFAULT_RESULT_NAME, self.name))

        super(Strategy, self).__init__(
            parent=parent, name=name, cfg=cfg,
            variable_names=VARIABLE_NAMES, **kwargs)

        # Read power curve, interplate and get thresholds
        self.get_power_curve()

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Compute wind electricity generation from climate data.

        :param stage: Modeling stage: `'fit'` or `'predict'`.

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

        # Download data if needed
        data_src.manage_download(
            variable_component_names=variable_component_names, **kwargs)

        # Functions to apply to the input climate data
        other_functions: tp.Iterable[e4tp.TransformStrictType] = [
            self.get_generation, data_src.get_regional_mean]
        transform_function = get_transform_function(
            data_src, stage, other_functions=other_functions,
            modifier=self.parent.modifier)

        # Get wind generation from climate data
        ds = data_src.parse_finalize(
            transform=transform_function,
            variable_component_names=variable_component_names)

        return ds

    def get_generation(
            self, ds: xr.Dataset = None,
            data_src: GriddedDataSourceBase = None, **kwargs) -> xr.Dataset:
        """Compute the photovoltaic electricity generation
        from the daily climate dataset.

        :param ds: Dataset containing climate variables from which to
          compute generation.
        :param data_src: Data source object from which to get features.

        :returns: A dataset containing electricity generation.

        :raises AssertionError: if

            * :py:obj:`ds` argument is `None`,
            * :py:obj:`data_src` argument is `None`.

        .. note::
          * The dataset should contain a `lat` and a `lon` coordinate
            variables.
          * The dataset should contain `zonal_wind` and `meridional_wind`
            variables for the zonal
            and meridional surface wind velocity.
          * If the `surface_temperature`, `surface_pressure`
            and `surface_specific_humidity` variables are given,
            the surface density
            is computed from the surface atmospheric temperature, pressure
            and specific humidity, respectively.
        """
        assert ds is not None, '"ds" argument required'
        assert data_src is not None, '"data_src" argument required'

        if 'wind_magnitude' in ds:
            speed = ds['wind_magnitude']
        else:
            # Get magnitude of wind speed from wind components
            speed = get_wind_magnitude(ds, **kwargs)

        self.info('Getting wind speed at 100m from 10m wind')
        z_0_wind = float(ds['zonal_wind'].attrs['height'])
        hub_speed = get_wind_at_height(
            speed, z=self.cfg['hub_height'], z_0=z_0_wind)

        # Get air density if possible
        if 'surface_density' in ds:
            # Check if surface density is given
            rho = ds['surface_density']
        else:
            # Compute density, if at least surface temperature
            # and pressure are given
            self.info('Computing density')
            rho = get_air_density_at_height(ds, self.cfg['hub_height'])

        # Get wind power
        mean_speed2mean_gen = False
        self.info('Getting wind power')
        self.generation = self.get_wind_generation(
            hub_speed, rho=rho, mean_speed2mean_gen=mean_speed2mean_gen)

        if self.med.cfg['frequency'] == 'day':
            if data_src.cfg['frequency'] == 'hour':
                # Downsample generation
                self.generation = self.generation.resample(
                    time='D').sum('time')
            else:
                # Convert from daily mean to daily integral
                self.generation *= 24
            generation_units = 'Wh/d'
        elif self.med.cfg['frequency'] == 'hour':
            generation_units = 'Wh'

        # Get capacity factors
        self.capacityfactor = self.generation / self.rated_power
        if self.med.cfg['frequency'] == 'day':
            self.capacityfactor /= 24

        # Try to add attributes (should be xarray.DataArray)
        try:
            self.capacityfactor.name = self.parent.result_name
            self.capacityfactor.attrs['long_name'] = 'Wind Capacity Factor'
            self.capacityfactor.attrs['units'] = ''
            self.generation.attrs['units'] = generation_units
        except AttributeError:
            pass

        ds = xr.Dataset({variable_name: getattr(self, variable_name)
                         for variable_name in VARIABLE_NAMES})

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get postfix corresponding to wind features.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        if self.cfg.get('use_roughness'):
            postfix += '_logheight'

        return postfix

    def get_power_curve(self):
        """Read and interpolate power curve.

        .. note::
          * Power curve should be an array with the wind speed and
            corresponding power as first and second columns, respectively.
          * For the interpolation, splines with cut-in, cut-out and rated
            output speeds are used to avoid large jumps in power distribution.
        """
        resource_name = '../data/{}'.format(self.cfg['powercurve_filename'])
        with resource_stream(__name__, resource_name) as f:
            power_data = pd.read_csv(f, index_col=0)

        # Power curve interpolation:
        self.speed_curve = power_data.index
        self.power_curve = power_data.values[:, 0]
        self.power_fun = interp1d(
            self.speed_curve, self.power_curve,
            kind='cubic', fill_value=0., bounds_error=False)

        # Cut-in speed
        id_cut_in = np.nonzero(self.power_curve > 0.1)[0][0]
        self.cut_in_speed = self.speed_curve[id_cut_in]

        # Cut-out speed
        id_cut_out = (np.nonzero(self.power_curve[id_cut_in:] > 0.1)[0][-1]
                      + id_cut_in)
        self.cut_out_speed = self.speed_curve[id_cut_out]

        # Rated power
        self.rated_power = np.max(self.power_curve)
        id_rated_power = np.nonzero(np.abs(
            self.rated_power - self.power_curve) < 0.1)[0][0]
        self.rated_power_speed = self.speed_curve[id_rated_power]

    def get_wind_generation(self, speed, rho=None, rho0=1.225,
                            mean_speed2mean_gen=False):
        """Compute wind power from a manufacturer's power curve.

        :param speed: Wind speed (m/s).
        :param rho: Air density (kg/m3). If None, air density
          is taken as the reference density for which the power curve
          was obtained.
        :param rho0: Reference air density (kg/m3) for which the
          power curve was obtained.
        :param mean_speed2mean_gen: If True, :py:obj:`speed`
          is taken as the mean of a Rayleigh distribution
          so that a factor is applied to the
          mean wind speed to get the corresponding mean wind power.
        :type speed: (sequence of) :py:class:`float`
        :type rho: (sequence of) :py:class:`float`
        :type rho0: float
        :type mean_speed2mean_gen: bool

        :returns: Wind power (W).
        :rtype: :py:class:`xarray.DataArray`
        """
        speed_eq = speed.copy(deep=True)

        # Conversion of wind speed for a different density
        if rho is not None:
            speed_eq *= (rho / rho0)**(1. / 3)

        # Factor accounting for the fact that mean wind power
        # is computed from mean wind speed
        if mean_speed2mean_gen:
            speed_eq *= (6. / np.pi)**(1. / 3)

        # Threshold. Use where function instead of method to keep as
        # original numpy.array
        try:
            generation = xr.full_like(speed_eq, None)
            generation[:] = self.power_fun(speed_eq)
        except TypeError:
            generation = self.power_fun(speed_eq)
        generation = xr.where((speed_eq > self.cut_in_speed) &
                              (speed_eq < self.cut_out_speed),
                              generation, 0.)
        generation = xr.where(speed_eq < self.rated_power_speed,
                              generation, self.rated_power)
        generation = xr.where(generation <= self.rated_power,
                              generation, self.rated_power)

        try:
            generation.name = 'generation'
            generation.attrs['long_name'] = 'Wind Generation'
            generation.attrs['units'] = 'Wh'
        except AttributeError:
            pass

        return generation


def upsample_wind_speed(speed):
    """Up-sample wind speed from daily to hourly values
    assuming that intra-day values follow a Rayleigh distribution
    with mean that of the given wind-speed time-series.

    :param speed: Daily wind-speed time-series.
    :type speed: :py:class:`xarray.DataArray`

    :returns: Hourly wind-speed.
    :rtype: :py:class:`xarray.DataArray`
    """
    # Upsample from daily to hourly values uniformly
    n_hours = 24
    delta_day = pd.Timedelta(n_hours - 1, unit='H')
    end_time = speed.indexes['time'][-1] + delta_day
    t = pd.date_range(start=speed.indexes['time'][0], end=end_time, freq='H')
    speed_up = speed.reindex(time=t)

    # Loop over days
    fact = np.sqrt(2 / np.pi)
    coords_space = [speed.coords[dim] for dim in speed.dims if dim != 'time']
    shape_space = [len(coord) for coord in coords_space]
    nspeedal = np.empty([n_hours] + shape_space)
    for date in speed.indexes['time']:
        # Get std predicted by Rayleigh distribution
        sigma = speed.loc[{'time': date}] * fact

        # Create noise array
        time_day = pd.date_range(
            start=date, end=(date + delta_day), freq='H')
        nspeedal[:] = [np.random.rayleigh(sigma) for h in range(n_hours)]
        coords = [('time', time_day)] + coords_space
        day_noise = xr.DataArray(nspeedal, coords=coords)

        # Add white noise to increase variance
        speed_up.loc[{'time': slice(time_day[0], time_day[-1])}] = day_noise

    return speed_up
