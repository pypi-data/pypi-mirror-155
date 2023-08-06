"""Solar-radiation calculations."""
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
from e4clim.utils.solar_calendar import (
    SolarCalendarComputer, compute_if_none)
from e4clim.utils.tracking import SolarTracker


#: Long names for horizontal irradiances.
LONG_NAMES_HORIZONTAL: tp.Final[tp.Mapping[str, str]] = {
    'global_normal_et': 'Global Normal Extraterrestrial Irradiance',
    'global_horizontal_et': 'Global Horizontal Extraterrestrial Irradiance',
    'global_horizontal_surf': 'Global Horizontal Surface Irradiance',
    'direct_normal_surf': 'Direct Normal Surface Irradiance',
    'direct_horizontal_surf': 'Direct Horizontal Surface Irradiance',
    'diffused_horizontal_surf': 'Diffuse Horizontal Surface Irradiance',
    'diffused_ratio': 'Diffuse over Global Irradiance Ratio',
    'diffused_ratio_reindl': (
        "Diffuse over Global Irradiance Ratio from Reindl's Model"),
    'clearness_index': 'Clearness Index',
}

#: Long names for tilted irradiances.
LONG_NAMES_TILTED: tp.Final[tp.Mapping[str, str]] = {
    'global_tilted_surf': 'Global Tilted Surface Irradiance',
    'direct_trans_factor': 'Direct Transposition Factor',
    'direct_tilted_surf': 'Direct Tilted Surface Irradiance',
    'diffused_trans_factor': 'Diffused Transposition Factor',
    'diffused_tilted_surf': 'Diffused Tilted Surface Irradiance',
    'view_factor': 'View Factor',
    'reflected_trans_factor': 'Reflected Transposition Factor',
    'reflected_tilted_surf': 'Reflected Tilted Surface Irradiance'
}

#: Units of irradiances.
UNITS: tp.Final[tp.Mapping[str, str]] = {
    'global_normal_et': 'W/m2',
    'global_horizontal_et': 'power',
    'clearness_index': '',
    'global_horizontal_surf': 'power',
    'global_tilted_surf': 'power',
    'direct_normal_surf': 'power',
    'direct_trans_factor': '',
    'direct_tilted_surf': 'power',
    'diffused_trans_factor': '',
    'diffused_tilted_surf': 'power',
    'view_factor': '',
    'reflected_trans_factor': '',
    'reflected_tilted_surf': 'power',
}


class HorizontalRadiationComputer():
    """Horizontal adiation computer.

    .. seealso::
       * Duffie, J.A., Beckman, W.A., 2013.
         *Solar Energy Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.
       * Reindl, D.T., Beckman, W.A., Duffie, J.A., 1990.
         Diffuse Fraction Correlation. *Solar Energy* 45, 1-7.

    .. warning:: All computations are for an hourly frequency.
    """

    #: Clearness index.
    _clearness_index: tp.Optional[xr.DataArray]
    #: Diffused-radiation model.
    diffused_model: str
    #: Elevation threshold.
    elevation_cut: float
    #: Global horizontal extraterrestrial radiation.
    _global_horizontal_et: tp.Optional[xr.DataArray]
    #: Global horizontal surface radiation.
    _global_horizontal_surf: tp.Optional[xr.DataArray]
    #: Latitude.
    lat: float
    #: Longitude.
    lon: float
    #: Power units.
    _power_units: str
    #: Solar-calendar computer.
    sc: SolarCalendarComputer
    #: Solar constant.
    solar_constant: float
    #: Time index.
    time: pd.DatetimeIndex

    def __init__(
            self, time: pd.DatetimeIndex = None, lat: float = None,
            lon: float = None, global_horizontal_surf: xr.DataArray = None,
            global_horizontal_et: xr.DataArray = None,
            clearness_index: float = None, solar_constant: float = 1367.,
            elevation_cut: float = None, diffused_model: str = 'reindl',
            solar_computer: SolarCalendarComputer = None,
            angles_in_degrees: bool = False, **kwargs) -> None:
        """Radiation computations. All computations eventually rely on
        (i) the global horizontal surface radiation,
        :py:obj:`global_horizontal_surf`,
        and (ii) the clearness index, :py:obj:`clearness_index`.
        The clearness index may, however, be computed as the ratio of
        the global horizontal surface irradiance and the global horizontal
        extraterrestrial irradiance and the latter may be computed from
        coordinates. Thus, at least the global horizontal surface radiation
        or the clearness index should be provided.

        :param time: Time. If `None`, :py:obj:`solar_computer` should be given.
        :param lat: Latitude. If `None`,
          :py:obj:`solar_computer` should be given.
        :param lon: Longitude. If `None`,
          :py:obj:`solar_computer` should be given.
        :param global_horizontal_surf: Global horizontal surface irradiance.
        :param global_horizontal_et: Global horizontal extraterrestrial
          irradiance.
        :param clearness_index: Clearness index.
        :param solar_constant: Solar constant (yearly averaged, in W/m2).
        :param elevation_cut: Elevation threshold below which
          direct radiation is considered zero (see note).
          If `None`, use default value of 10 degrees.
        :param diffused_model: Model used to extract diffuse componant
          of global horizontal radiation. Only the model by
          Reindl *et al.* (1990) is available at the moment.
        :param solar_computer: Solar computer to initialize with, instead
          of constructing one from :py:obj:`time`, :py:obj:`lat` and
          :py:obj:`lon`, to speed-up computations.
        :param angles_in_degrees: Whether angles are given in degrees instead
          of radians and should be returned in degrees by
          :py:meth:`.solar_calendar.SolarCalendarComputer.get_angle`.

        :raises AssertionError: if both :py:obj:`global_horizontal_surf` and
          :py:obj:`clearness_index` are `None`.
        """
        # Make sure that at least the global horizontal surface radiation
        # or the clearness index are provided
        assert (global_horizontal_surf is not None) or (
            clearness_index is not None), (
                '"global_horizontal_surf" or "clearness_index" argument'
                'required')

        # Add time, latitude and longitude (in radians) as attributes
        fact = np.deg2rad(1.) if angles_in_degrees else 1.

        # Create solar angles computer (all computations in radians)
        if solar_computer is None:
            self.time = time
            self.lat = lat * fact
            self.lon = lon * fact
            self.sc = SolarCalendarComputer(
                self.time, self.lat, self.lon, angles_in_degrees=False)
        else:
            self.sc = solar_computer
            self.time = self.sc.time
            self.lat = self.sc.lat
            self.lon = self.sc.lon

        # Initialize all attribute variables to be computed
        self.clear(LONG_NAMES_HORIZONTAL)

        # Set given radiations and and clearness index
        self._global_horizontal_surf = global_horizontal_surf
        self._global_horizontal_et = global_horizontal_et
        self._clearness_index = clearness_index

        # Get power units
        self._power_units = self._get_power_units()

        # Other parameters
        self.solar_constant = solar_constant
        self.elevation_cut = (np.deg2rad(10.) if elevation_cut is None
                              else elevation_cut * fact)
        self.diffused_model = diffused_model

    def clear(self, names: tp.Iterable[str]) -> None:
        """Set all computed attribute variables to `None`.

        :param names: Names of variables to set.
        :type names: collection of :py:class:`str`
        """
        for variable_name in names:
            setattr(self, '_' + variable_name, None)

    def _get_power_units(self) -> str:
        """Try to get power units from
        :py:attr:`self._global_horizontal_surf` or
        :py:attr:`self._global_horizontal_et`, otherwise
        return `'power'`.

        :returns: Power units.
        """
        try:
            return self._global_horizontal_surf.attr['units']
        except (AttributeError, KeyError):
            try:
                return self._global_horizontal_et.attr['units']
            except (AttributeError, KeyError):
                return 'power'

    def _add_attributes(self, variable_name: str) -> None:
        """Add `long_name` and `units` attributes to data array.

        :param variable_name: Variable name.
        """
        # Get variable from variable name
        var = getattr(self, variable_name)

        # Try to add attributes
        try:
            variable_name = (variable_name[1:] if variable_name[0] == '_' else
                             variable_name)
            var.attrs['long_name'] = self.long_names[variable_name]
            var.attrs['units'] = (self.power_units
                                  if UNITS[variable_name] == 'power'
                                  else UNITS[variable_name])
        except AttributeError:
            pass

    @property
    @compute_if_none
    def clearness_index(self) -> xr.DataArray:
        """Compute the clearness index as the ratio between the
           global (surface) and extraterrestrial horizontal radiations.

        :returns: Clearness index.
        """
        # Compute the clearness index as the ratio between the surface and top
        # of the atmosphere downwelling shortwave radiation.
        var = xr.where(
            self.global_horizontal_et > 0.,
            self.global_horizontal_surf / self.global_horizontal_et,
            0.)

        # Ensure that the var index is between 0 and 1
        var = xr.where(var < 0., 0., var)
        var = xr.where(var > 1., 1., var)

        return var

    @property
    @compute_if_none
    def global_normal_et(self) -> xr.DataArray:
        """Get extraterrestrial solar radiation for a given day of the year,
           taking into account variations or the earth-sun distance.

        :returns: Extraterrestrial solar radiation (W/m2).

        .. note::
          * The Fourier series model of Spencer (1971) is used.
          * Hourly variations are very small and thus neglected.
        """
        doy_rad = (self.time.dayofyear - 1) * 2*np.pi / 365

        return self.solar_constant * (
            1.000110 + 0.034221 *
            np.cos(doy_rad) + 0.001280 * np.sin(doy_rad)
            + 0.000719 * np.cos(2*doy_rad) + 0.000077 * np.sin(2*doy_rad))

    @property
    @compute_if_none
    def global_horizontal_et(self) -> xr.DataArray:
        """ Get the extraterrestrial horizontal radiation
            from the extraterrestrial radiation and zenith.

        :returns: Extraterrestrial horizontal radiation.

        .. note::
          Negative values (between sunrise and sunset) are clipped to zero.
        """
        # Get the extraterrestrial horizontal radiation
        var = self.global_normal_et * np.cos(self.sc.zenith)

        # Keep positive values (between sunrise and sunset)
        return xr.where(var >= 0., var, 0.)

    @property
    @compute_if_none
    def global_horizontal_surf(self) -> xr.DataArray:
        """ Compute the global horizontal surface radiation as the product
            of the clearness index with the global extraterrestrial
            horizontal radiation.

        :returns: Global horizontal surface radiation.
        """
        # Get the surface horizontal radiation
        return self.clearness_index * self.global_horizontal_et

    @property
    @compute_if_none
    def direct_normal_surf(self) -> xr.DataArray:
        """Get direct normal surface radiation.

        :returns: Direct normal radiation.
        """
        return xr.where(self.direct_horizontal_surf > 1.e-10,
                        self.direct_horizontal_surf / np.cos(self.sc.zenith),
                        0.)

    @property
    @compute_if_none
    def direct_horizontal_surf(self) -> xr.DataArray:
        """ Get the direct horizontal surface radiation.

        :returns: Direct horizontal radiation.

        .. note:: The threshold :py:obj:`elevation_cut` should be larger than
          a few degrees in order to prevent numerical overflow in the direct
          transposition factor.

        .. seealso:: :py:meth:`TiltedRadiationComputer.direct_trans_factor`
        """
        var = self.global_horizontal_surf - self.diffused_horizontal_surf

        # Below the elevation_cut threshold, the direct radiation
        # is considered null.
        if self.elevation_cut is not None:
            var = xr.where(self.sc.elevation >= self.elevation_cut,
                           var, 0.)

        return var

    @property
    @compute_if_none
    def diffused_horizontal_surf(self) -> xr.DataArray:
        """ Get diffuse component of global horizontal surface radiation.

        :returns: Diffusive part of the horizontal radiation.
        """
        return self.global_horizontal_surf * self.diffused_ratio

    @property
    @compute_if_none
    def diffused_ratio(self) -> xr.DataArray:
        """Get ratio of diffuse over global horizontal surface radiation.

        :returns: Diffuse over global horizontal surface radiation ratio.
        """
        if self.diffused_model == 'reindl':
            var = self.diffused_ratio_reindl

        return var

    @property
    @compute_if_none
    def diffused_ratio_reindl(self) -> xr.DataArray:
        """Get ratio of diffuse over global horizontal surface radiation
        using the model by Reindl * et al.* (1990).

        :returns: Diffuse over global horizontal surface radiation ratio.
        """
        var = (1.4 - 1.749 * self.clearness_index
               + 0.177 * np.sin(self.sc.elevation))
        var = xr.where(
            self.clearness_index < 0.3, 1.02 - 0.254 * self.clearness_index
            + 0.0123 * np.sin(self.sc.elevation), var)
        var = xr.where(self.clearness_index > 0.78,
                       0.486 * self.clearness_index
                       - 0.182 * np.sin(self.sc.elevation), var)
        var = xr.where(var < 0.1, 0.1, var)
        var = xr.where(var > 0.97, 0.97, var)

        return var


class TiltedRadiationComputer(HorizontalRadiationComputer):
    """Tilted adiation computer.

    .. seealso::
       * Duffie, J.A., Beckman, W.A., 2013.
         *Solar Energy Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.
       * Gueymard, C.A., 2009. Direct and indirect uncertainties in the
         prediction of tilted radiation for solar engineering applications.
         *Solar Energy* 83, 432-444.
       * Maleki, S.A.M, Hizam, H., Gomes, C., 2017.
         Estimation of Hourly, Daily and Monthly Global
         Solar Radiation on Inclined Surfaces: Models Re-Visited.
         *Energies* 10, 1-28.
    """
    #: Albedo.
    albedo: float

    #: Solar tracker.
    tracker: SolarTracker

    def __init__(
            self, time: pd.DatetimeIndex = None, lat: float = None,
            lon: float = None, global_horizontal_surf: xr.DataArray = None,
            global_horizontal_et: xr.DataArray = None,
            clearness_index: xr.DataArray = None,
            solar_constant: float = 1367., elevation_cut: float = None,
            diffused_model: str = 'reindl',
            solar_computer: SolarCalendarComputer = None,
            tilt: float = None, azimuth: float = None, albedo: float = 0.2,
            angles_in_degrees: bool = False, **kwargs) -> None:
        """Radiation computations. All computations eventually rely on
        (i) the global horizontal surface radiation,
        :py:obj:`global_horizontal_surf`,
        and (ii) the clearness index, :py:obj:`clearness_index`.
        The clearness index may, however, be computed as the ratio of
        the global horizontal surface irradiance and the global horizontal
        extraterrestrial irradiance and the latter may be computed from
        coordinates. Thus, at least the global horizontal surface radiation
        or the clearness index should be provided.

        :param time: Time. If `None`, :py:obj:`solar_computer` should be given.
        :param lat: Latitude. If `None`,
          :py:obj:`solar_computer` should be given.
        :param lon: Longitude. If `None`,
          :py:obj:`solar_computer` should be given.
        :param global_horizontal_surf: Global horizontal surface irradiance.
        :param global_horizontal_et: Global horizontal extraterrestrial
          irradiance.
        :param clearness_index: Clearness index.
        :param solar_constant: Solar constant (yearly averaged, in W/m2).
        :param elevation_cut: Elevation threshold below which
          direct radiation is considered zero (see note).
          If `None`, use default value of 10 degrees.
        :param diffused_model: Model used to extract diffuse componant
          of global horizontal radiation. Only the model by
          Reindl *et al.* (1990) is available at the moment.
        :param tilt: Surface tilt. For east-west axis, north-south axis,
          vertical axis, or two axes, respectively set to `'ew_axis'`,
          `'ns_axis'`, `'vertical'`, or `'two'`.
          For a tilt equal to the latitude, set to `'lat'`. If `None`,
          computer may not be used to compute tilted irradiances.
        :param azimuth: Surface azimuth. If `None`,
          computer may not be used to compute tilted irradiances.
        :param solar_constant: Solar constant (yearly averaged, in W/m2).
        :param albedo: Composite ground albedo used to compute
          the reflected radiation.
        :param diffused_model: Model used to extract diffuse componant
          of global horizontal radiation. Only the model by
          Reindl *et al.* (1990) is available at the moment.
        :param solar_computer: Solar computer to initialize with, instead
          of constructing one from :py:obj:`time`, :py:obj:`lat` and
          :py:obj:`lon`, to speed-up computations.
        :param angles_in_degrees: Whether angles are given in degrees instead
          of radians.
        """
        # Initialize as HorizontalRadiationComputer
        super(TiltedRadiationComputer, self).__init__(
            time=time, lat=lat, lon=lon, solar_computer=solar_computer,
            global_horizontal_surf=global_horizontal_surf,
            global_horizontal_et=global_horizontal_et,
            clearness_index=clearness_index, solar_constant=solar_constant,
            elevation_cut=elevation_cut, diffused_model=diffused_model,
            angles_in_degrees=angles_in_degrees, **kwargs)

        # Tracking computer (all computations in radians)
        self.tracker = SolarTracker(
            self.sc, tilt, azimuth,
            angles_in_degrees=angles_in_degrees, **kwargs)

        # Initialize all attribute variables to be computed
        self.clear(LONG_NAMES_TILTED)

        # Other parameters
        self.albedo = albedo

    @property
    @compute_if_none
    def global_tilted_surf(self) -> xr.DataArray:
        """Compute global tilted surface radiation.

        :returns: Global tilted surface radiation.

        .. note::
          * For a general review of the various existing models to calculate
            the global tilted radiation, see Maleki *et al.* (2017)
            and Gueymard (2009).
          * For a general treatment of the available solar radiation,
            see Duffie and Beckman (2013).
        """
        # Get global radiation on tilted surface
        return (self.direct_tilted_surf + self.diffused_tilted_surf
                + self.reflected_tilted_surf)

    @property
    @compute_if_none
    def direct_trans_factor(self) -> xr.DataArray:
        """Get direct transposition factor.

        :returns: Direct transposition factor.

        .. seealso::
          :py:meth:`HorizontalRadiationComputer.direct_horizontal_surf`
        """
        # Cut at the same place as the DHI (for an elevation larger than
        # the elevation_cut, at least higher than 0)
        # and when the sun is behind is behind the surface
        test = ((self.direct_horizontal_surf > 0.)
                & (np.fabs(self.sc.azimuth - self.tracker.surface_azimuth)
                   < np.pi/2))

        return xr.where(
            test, self.tracker.cos_aoi / np.cos(self.sc.zenith), 0.)

    @property
    @compute_if_none
    def direct_tilted_surf(self) -> xr.DataArray:
        """Get direct tilted surface radiation.

        :returns: Direct tilted surface radiation.
        """
        return self.direct_horizontal_surf * self.direct_trans_factor

    @property
    @compute_if_none
    def diffused_trans_factor(self) -> xr.DataArray:
        """Get diffused transposition factor.

        :returns: Diffused transposition factor.

        .. note::
          The diffuse transposition factor is calculated using the
          HDKR model.
          See Reindl * et al.* (1990) and Maleki * et al.* (2017).
        """
        aniso_idx = xr.where(
            self.global_horizontal_surf > 0.,
            self.direct_horizontal_surf / self.global_horizontal_surf
            * self.clearness_index,
            0.)

        # Modulating function mod_fun
        mod_fun = xr.where(
            self.global_horizontal_surf > 0.,
            np.sqrt(self.direct_horizontal_surf /
                    self.global_horizontal_surf),
            0.)

        # Isotropic transposition factor
        transpo_iso = (1. + np.cos(self.tracker.surface_tilt)) / 2

        # Diffuse transposition factor. See note.
        return (
            aniso_idx * self.direct_trans_factor +
            (1. - aniso_idx) * transpo_iso
            * (1 + mod_fun * np.sin(self.tracker.surface_tilt / 2)**3))

    @property
    @compute_if_none
    def diffused_tilted_surf(self) -> xr.DataArray:
        """ Get diffuse tilted surface radiation.

        :returns: Diffuse tilted surface radiation.
        """
        return self.diffused_horizontal_surf * self.diffused_trans_factor

    @property
    @compute_if_none
    def view_factor(self) -> xr.DataArray:
        """Get view factor for reflected radiation.

        :returns: View factor.
        """
        return (1. - np.cos(self.tracker.surface_tilt)) / 2

    @property
    @compute_if_none
    def reflected_trans_factor(self) -> xr.DataArray:
        """Get reflected transposition factor.

        :returns: Reflected transposition factor.
        """
        return self.albedo * self.view_factor

    @property
    @compute_if_none
    def reflected_tilted_surf(self) -> xr.DataArray:
        """ Get reflected tilted surface radiation.

        :returns: Reflected tilted radiation.

        .. note: :
           The reflected tilted radiation is calculated for a flat array
           using the isotropic sky formula reviewed in Gueymard(2009).
        """
        return self.global_horizontal_surf * self.reflected_trans_factor
