"""Climate-related calculations."""
import numpy as np
import pandas as pd
from pathlib import Path
import typing as tp
import xarray as xr
import e4clim


def add_roughness_height(
        ds: xr.Dataset,
        data_src: 'e4clim.container.gridded_data_source.GriddedDataSourceBase',
        **kwargs) -> xr.Dataset:
    """Add roughness height to dataset.

    :param ds: Dataset.
    :param data_src: Data source object for which the mask is adapted.

    :returns: Dataset with same grid as roughness height array.
    """
    cfg = data_src.med.cfg

    postfix = '_{}{}_{}_{}'.format(
        'clc', str(cfg['CLC']['year']), data_src.name, data_src.cfg['domain'])
    filename = 'roughness_length{}.nc'.format(postfix)
    file_dir = data_src.med.cfg.get_project_data_directory(makedirs=False)
    filepath = Path(file_dir, 'climate', filename)
    with xr.open_dataarray(filepath) as da:
        # Indexes x and y may change in some data set resulting
        # in erros when aligning. Just set with those of dataset
        if 'y' in da.coords:
            da['y'] = ds['y']
        if 'x' in da.coords:
            da['x'] = ds['x']
        ds['roughness_height'] = da.copy(deep=True)

    return ds


def get_molar_mass_air(
        hu: xr.DataArray = 0., dry_molar_mass: float = 0.028964,
        vapor_molar_mass: float = 0.018016) -> xr.DataArray:
    """Get molar mass of wet air from specific humidity.

    :param hus: Specific humidity.
    :param dry_molar_mass: Molar mass of dry air (kg/mol).
    :param vapor_molar_mass: Molar mass of water vapor (kg/mol).

    :returns: Molar mass of wet air.
    """
    return dry_molar_mass * vapor_molar_mass / (
        (1 - hu) * vapor_molar_mass + hu * dry_molar_mass)


def get_temperature_at_height(
        temp_0: xr.DataArray, z_0: float, z: float,
        L: float = 0.0065) -> xr.DataArray:
    """Use a linear profile with constant lapse rate to compute
    the temperature at a given height (below tropopause).

    :param temp_0: Temperature at given height (K).
    :param z_0: Height at which temperature is given (m).
    :param z: Height at which to return temperature (m).
    :param L: Temperature lapse rate (K/m).

    :returns: Temperature at given level.
    """
    return temp_0 - L * (z - z_0)


def get_pressure_at_height(
        press_0: xr.DataArray, z_0: float, z: float, temp_z: float,
        air_molar_mass: float = 0.0289644, lapse_rate: float = 0.0065,
        univ_gas_cst: float = 8.3144598,
        g_0: float = 9.80665) -> xr.DataArray:
    """Use the barometric formula to compute pressure at a
    given level from pressure at another.strategy.

    :param press_0: Pressure at given height (Pa).
    :param z_0: Height at which pressure is given (m).
    :param z: Height at which to return pressure (m).
    :param temp_z: Standard temperature at output height (K).
    :param air_molar_mass: Molar mass of air(kg/mol).
      Default is dry air molar mass.
    :param lapse_rate: Temperature lapse rate (K/m).
    :param univ_gas_cst: Universal gas constant (J/K/mol).
    :param g_0: Gravitational acceleration (m/s2).

    :returns: Pressure at given level.
    """
    exp = g_0 * air_molar_mass / (univ_gas_cst * lapse_rate)
    if z >= z_0:
        press_z = press_0 * (
            temp_z / (temp_z + lapse_rate * (z - z_0)))**exp
    else:
        press_z = press_0 * (
            temp_z / (temp_z + lapse_rate * (z_0 - z)))**(-exp)

    return press_z


def get_air_density(
        temp_a: xr.DataArray, press: xr.DataArray,
        air_molar_mass: float = 0.0289644,
        univ_gas_cst: float = 8.3144598) -> xr.DataArray:
    """Get air density from other climate variables and the ideal gas law.

    :param temp_a: Atmospheric temperature (K).
    :param press: Pressure (Pa).
    :param air_molar_mass: Molar mass of air (kg/mol).
      Default is dry air molar mass.
    :param univ_gas_cst: Universal gas constemp_ant (J/K/mol).

    :returns: Air density.
    """
    # Ideal gas law
    rho = air_molar_mass * press / (univ_gas_cst * temp_a)

    return rho


def get_air_density_at_height(
        ds: xr.Dataset, height: float) -> xr.DataArray:
    """Get air density at height by computing the climate variables
    at height and using the equation of state.

    :param ds: Dataset containing all climate variables of interest.
    :param height: height.

    :returns: Air density.
    """
    # Get molar mass of air
    # If specific humidity given, use wet air
    # (assuming that humidity is constant with height)
    hus = 0.
    if 'surface_specific_humidity' in ds:
        hus = ds['surface_specific_humidity']
    molar_mass_air = get_molar_mass_air(hu=hus)

    # Get temperature at height
    temp_height = None
    if 'surface_temperature' in ds:
        temp_0 = ds['surface_temperature']
        z_0_temp = float(temp_0.attrs['height'])
        temp_height = get_temperature_at_height(temp_0, z_0_temp, height)

    # Get pressure at some surface
    # (does the pressure formula rely only on relative height?)
    get_pressure = False
    if 'surface_pressure' in ds:
        press_0 = ds['surface_pressure']
        z_0_press = float(press_0.attrs['height'])
        get_pressure = True

    # Or get pressure at sea level
    # (problem because orography larger than 0m)
    if (not ('surface_pressure' in ds)) and ('sea_level_pressure' in ds):
        press_0, z_0_press = ds['sea_level_pressure'], 0.
        get_pressure = True

    # Get pressure at height
    press_height = None
    if get_pressure:
        press_height = get_pressure_at_height(
            press_0, z_0_press, height, temp_height, molar_mass_air)

    if (temp_height is not None) & (press_height is not None):
        # Get air density from equation of state
        rho = get_air_density(temp_height, press_height, molar_mass_air)
    else:
        rho = None

    return rho


def get_wind_magnitude(
        ds: xr.Dataset = None,
        data_src: 'e4clim.container.data_source.DataSourceBase' = None,
        **kwargs) -> xr.DataArray:
    """Add wind magnitude computed from wind components to dataset,
    only if `'wind_magnitude'` not already in dataset.

    :param ds: Dataset containing `zonal_wind` and `meridional_wind`
      components. If `None`, wind data is read from the data source.
    :param data_src: Input data source. Only used if :py:obj:`ds` is `None`.

    :returns: Wind magnitude.
    """
    if ds is None:
        # Get data from data source
        if 'wind_magnitude' in data_src.variable_component_names:
            data_src.get_data(
                variable_component_names='wind_magnitude', **kwargs)
        else:
            data_src.get_data(
                variable_component_names=['zonal_wind', 'meridional_wind'],
                **kwargs)
        ds = data_src.data

    if 'wind_magnitude' in ds:
        da = ds['wind_magnitude']
    else:
        da = np.sqrt(ds['zonal_wind']**2 + ds['meridional_wind']**2)

        # Add units
        if hasattr(ds['zonal_wind'], 'attrs'):
            if 'units' in ds['zonal_wind'].attrs:
                da.attrs['units'] = ds['zonal_wind'].attrs['units']

    return da


def get_wind_at_height(
        speed_0: xr.DataArray, z: float, z_0: float = 10.,
        roughness_height: xr.DataArray = None,
        alpha: float = 1./7) -> xr.DataArray:
    """Compute wind speed at height :py:obj:`z` from wind speed at
    reference height :py:obj:`z_0` using either a power law with exponent
    :py:obj:`alpha` (Justus and Mikhail, 1976), or a neutral stability
    logarithmic profile with roughness height :py:obj:`zr` (Lysen, 1983).

    :param speed_0: Wind magnitude.
    :param z: Height at which to compute wind speed (m).
    :param z_0: Height at which wind speed is given (m).
    :param roughness_height: Roughness height (m). If given,
      the logarithmic law is used. Otherwise, the power law is used.
    :param alpha: Wind shear exponent.

    :returns: Wind speed at given height.

    .. seealso::
      * Justus, C. G., and Amir Mikhail, 1976, Height Variation of Wind Speed
        and Wind Distributions Statistics. *GRL* 3, 261-64.
      * Lysen, E. H., 1983, *Introduction to Wind Energy*, CWD, Amersfoort.
    """
    # Transform to magnitude of wind speed at hubHeight
    speed_z = xr.DataArray(speed_0)
    if roughness_height is None:
        speed_z *= (z / z_0)**alpha
    else:
        speed_z *= np.log(z / roughness_height) / np.log(
            z_0 / roughness_height)

    speed_z.name = 'wind_magnitude'
    speed_z.attrs['long_name'] = 'Wind Speed at {:.2f}m'.format(z)
    if 'units' in speed_0.attrs:
        speed_z.attrs['units'] = speed_0.attrs['units']
    else:
        speed_z.attrs['units'] = 'Unknown, speed_0 provided without units'

    return speed_z


def get_climatology(da: xr.DataArray) -> tp.Tuple[
        xr.DataArray, xr.DataArray]:
    """Get climatology and anomalies from time series.

    :param data: Time series.

    :returns: A tuple containing the climatology and the anomalies.
    """
    # Get climatology
    gp = da.groupby('time.dayofyear')
    da_clim = gp.mean(keep_attrs=True)

    # Get anomalies
    da_ano = gp - da_clim

    return da_clim, da_ano


def get_seasonal_cycle(
        da: xr.DataArray, time_name: str = 'time',
        filter_leap_years: bool = True, **kwargs) -> xr.DataArray:
    """Get seasonal cycle from data.

    :param da: Data array from which to get cycle.
    :param time_name: Time-dimension name.
    :param filter_leap_years: Filter leap years.

    :returns: Seasonal cycle.
    """
    # Get time of year
    t = da.indexes[time_name]
    if len(np.unique(t.hour)) > 1:
        time_of_year = pd.MultiIndex.from_arrays(
            [t.dayofyear, t.hour], names=['dayofyear', 'hour'])
    else:
        time_of_year = t.dayofyear

    # Group by time of year
    da.coords['time_of_year'] = ('time', time_of_year)
    gp_seasonal_cycle = da.groupby('time_of_year')

    # Get seasonal cycle
    seasonal_cycle = gp_seasonal_cycle.mean(time_name)

    if filter_leap_years:
        # Remove day from leap years
        seasonal_cycle = seasonal_cycle[
            seasonal_cycle['time_of_year_level_0'] != 366]

    # Drop time_of_year from reference array
    del da['time_of_year']

    return seasonal_cycle
