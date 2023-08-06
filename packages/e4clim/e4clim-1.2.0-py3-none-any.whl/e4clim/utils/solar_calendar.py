"""Calculations related to calendars and astronomical parameters."""
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr

#: Variable long-names.
LONG_NAMES: tp.Final[tp.Mapping[str, str]] = {
    'julian_day': 'Julian Day',
    'ndays_since': 'Days since 2000-01-01 12:00:00',
    'mean_longitude': 'Mean Longitude',
    'elevation': 'Elevation', 'zenith': 'Zenith',
    'azimuth': 'Azimuth',
    'mean_anomaly': 'Mean Anomaly',
    'ecliptic_longitude': 'Ecliptic Longitude',
    'ecliptic_obliquity': 'Obliquity of Ecliptic',
    'right_ascension': 'Right Ascension',
    'declination': 'Declination',
    'utc_hour': 'Hour UTC',
    'greenwich_mean_sideral_time': 'Greenwich Mean Sideral Time',
    'local_mean_sideral_time': 'Local Mean Sideral Time',
    'hour_angle': 'Hour Angle',
    'sunset_hour_angle': 'Sunset Hour Angle',
    'daily_cos_zenith': 'Daily-Integrated Cosine of Zenith',
    'daily_mean_cos_zenith': 'Daily-Averaged Cosine of Zenith'
}


def compute_if_none(fun: tp.Callable[[tp.Any], xr.DataArray]) -> tp.Callable[
        [tp.Any], xr.DataArray]:
    """Compute attribute with the same name as :py:obj:`fun`
    only if `None`."""

    def comp_fun(self):
        attr_name = '_' + fun.__name__

        # Compute variable only if None
        if getattr(self, attr_name) is None:
            # Compute variable
            var = fun(self)

            # Make sure it is a data array
            try:
                var = xr.DataArray(var, coords=[('time', self.time)])
            except ValueError:
                var = xr.DataArray(var)

            # Add variable to attribute
            setattr(self, attr_name, var)

            # Add names
            self._add_attributes(attr_name)

        return getattr(self, attr_name)

    return comp_fun


def _clip_angle(angle: xr.DataArray) -> xr.DataArray:
    """Clip angle between minus pi and pi.

    :param angle: Angle in radians.

    :returns: Clipped angle.
    """
    lim = np.pi
    return np.fabs(np.fmod(angle + lim, 2 * lim)) - lim


class SolarCalendarComputer(object):
    """Class to compute solar calendar variables.
    When getting an attribute, the variable
    corresponding to it is automatically computed. New computations are
    only performed if the needed attribute value is `None`, i.e. if it
    has not previously been computed.
    To perform new computations, start from a new object,
    or call :py:meth:`clear`.

    .. note::
      * The Almanac approximation is used with ecliptic coordinates,
        as in Michalsky (1988).
      * The *solar elevation* is the angle between the horizontal and the
        line to the sun, that is, the complement of the *zenith angle*.
      * The *solar azimuth* is the angular displacement from south of the
        projection of beam radiation on the horizontal plane. Displacements
        east of south are negative and west of south are positive.
      * The *right ascension* is the angular distance measured eastward
        along the celestial equator from the Sun at the March equinox
        to the hour circle of the point above the earth in question.
      * The *declination* is the angular position of the sun at solar noon
        (i.e., when the sun is on the local meridian)
        with respect to the plane of the equator, north positive.
      * The *hour angle* is the angular displacement of the sun east or west
        of the local meridian due to rotation of the earth on its axis at
        15 degrees per hour; morning negative, afternoon positive.
      * The *sunset hour angle* is the hour angle when elevation is zero.
        See Duffie and Beckman(2013).

    .. warning::
      The Almanac's approximation covers the (1950-2050) period
      and may need to be modified for longer periods.

    .. seealso::
      * Michalsky, J.J., 1988. The Astronomical Almanac's Algorithm format
        Approximate Solar Position (1950, 2050). *Solar Energy* 40, 227-235.
      * Duffie, J.A., Beckman, W.A., 2013.
      * *Solar Energy and Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.

    """

    #: Whether angles are in degrees.
    angle_in_degrees: bool
    #: Angle units.
    angle_units: str
    #: Degree to radians conversion factor.
    fact: float
    #: Inverse conversion factor.
    inv_fact: float
    #: Latitude.
    lat: float
    #: Longitude.
    lon: float
    #: Time index.
    time: pd.DatetimeIndex

    def __init__(
            self, time: pd.DatetimeIndex, lat: float, lon: float,
            angles_in_degrees: bool = False):
        """Initialize solar angles computer.

        :param time: Time.
        :param lat: Latitude.
        :param lon: Longitude.
        :param angles_in_degrees: Whether angles are given in degrees instead
          of radians and should be returned in degrees by :py:meth:`get_angle`.

        .. warning:: All attribute variables (e.g. :py:attr:`hour_angle`)
            are given in radians and all computations are performed
            in radians. To get angles in the same units as those
            provided to constructor, call :py:meth:`get_angle`.
        """

        # Manage degrees-radians conversion
        self.angles_in_degrees = angles_in_degrees
        self.fact = np.deg2rad(1.) if self.angles_in_degrees else 1.
        self.inv_fact = 1. if self.angles_in_degrees else np.deg2rad(1.)
        self.angle_units = 'degrees' if self.angles_in_degrees else 'radians'

        # Convert to radians if needed
        self.time = time
        self.lat = lat * self.fact
        self.lon = lon * self.fact

        # Initialize all variables to be computed to None
        self.clear()

    def clear(self) -> None:
        """Set all computed attribute variables to `None`."""
        for variable_name in LONG_NAMES:
            setattr(self, '_' + variable_name, None)

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
            var.attrs['long_name'] = LONG_NAMES[variable_name]
            var.attrs['units'] = self.angle_units
        except AttributeError:
            pass

    def get_angle(self, angle_name: str) -> float:
        """Get angle, converted in degrees if needed.

        :param angle_name: Angle name.

        .. warning:: No exception is raised if a non-angle variable name,
          e.g. :py:attr:`julian_day` is given, leading to return this variable
          after a potential spurious angle conversion. Instead, such variables
          should directly be accessed as attribute.
        """
        return _clip_angle(getattr(self, angle_name)) / self.fact

    @property
    @compute_if_none
    def julian_day(self) -> pd.Index:
        """Get Julian day as data array."""
        return self.time.to_julian_date()

    @property
    @compute_if_none
    def ndays_since(self) -> float:
        """Get number of days since 2000-01-01 12:00:00."""
        return self.julian_day - 2451545.0

    @property
    @compute_if_none
    def mean_longitude(self) -> float:
        """Get mean longitude."""
        return 4.89495 + 0.01720279 * self.ndays_since

    @property
    @compute_if_none
    def elevation(self) -> xr.DataArray:
        """Compute solar elevation from Julian day, East longitude and
        latitude. Angular extent of sun neglected.
        """
        # Elevation (radians)
        return np.arcsin(
            np.sin(self.declination) * np.sin(self.lat) +
            np.cos(self.declination) * np.cos(self.lat) *
            np.cos(self.hour_angle))

    @property
    @compute_if_none
    def zenith(self) -> xr.DataArray:
        """Get zenith from elevation angle."""
        return np.pi/2 - self.elevation

    @property
    @compute_if_none
    def azimuth(self) -> xr.DataArray:
        """Compute solar azimuth from Julian day, East longitude and latitude.
        Angular extent of sun neglected.
        """
        # Azimuth (radians)
        # Numerical errors may lead to absolute sine values slighly larger
        # than 1. In this case, angle is set to -pi/2, as should be.
        var = -np.pi/2 * xr.ones_like(self.elevation)
        val = (-np.cos(self.declination) * np.sin(self.hour_angle)
               / np.cos(self.elevation))
        np.arcsin(val, out=var.values, where=(np.fabs(val) < 1.))

        # Assign correct quadrant to azimuth (check discontinuity)
        elc = np.arcsin(np.sin(self.declination) / np.sin(self.lat))
        var = xr.where(self.elevation >= elc, np.pi - var, var)

        return var

    @property
    @compute_if_none
    def mean_anomaly(self) -> xr.DataArray:
        """Get mean anomaly."""
        return 6.24004 + 0.01720197 * self.ndays_since

    @property
    @compute_if_none
    def ecliptic_longitude(self) -> xr.DataArray:
        """Get ecliptic longitude."""
        return self.mean_longitude + 0.03342 * np.sin(
            self.mean_anomaly) + 0.00035 * np.sin(2 * self.mean_anomaly)

    @property
    @compute_if_none
    def ecliptic_obliquity(self) -> xr.DataArray:
        """Get ecliptic obliquity."""
        return 0.40908 - 7.e-9 * self.ndays_since

    @property
    @compute_if_none
    def right_ascension(self) -> xr.DataArray:
        """Get right ascension."""
        return np.arctan2(
            np.cos(self.ecliptic_obliquity) *
            np.sin(self.ecliptic_longitude),
            np.cos(self.ecliptic_longitude))

    @property
    @compute_if_none
    def declination(self) -> xr.DataArray:
        """Get declination."""
        return np.arcsin(
            np.sin(self.ecliptic_obliquity) *
            np.sin(self.ecliptic_longitude))

    @property
    @compute_if_none
    def utc_hour(self) -> xr.DataArray:
        """Get UTC hour in radians."""
        # A decimal part of the Julian date equal to zero
        # corresponds to noon (12h)
        djd = self.julian_day.astype(int)
        return (self.julian_day - djd) * 2*np.pi + np.pi

    @property
    @compute_if_none
    def greenwich_mean_sideral_time(self) -> xr.DataArray:
        """Get Greenwich mean sideral time."""
        return 1.753369 + 0.0172027917 * self.ndays_since + self.utc_hour

    @property
    @compute_if_none
    def local_mean_sideral_time(self) -> xr.DataArray:
        """Get local mean sideral time."""
        return self.greenwich_mean_sideral_time + self.lon

    @property
    @compute_if_none
    def hour_angle(self) -> xr.DataArray:
        """Get hour angle in radians."""
        return self.local_mean_sideral_time - self.right_ascension

    @property
    @compute_if_none
    def sunset_hour_angle(self) -> xr.DataArray:
        """Compute sunset hour angle from latitude and declination."""
        # Compute sunset hour angle
        return np.arccos(
            -np.tan(self.lat) * np.tan(self.declination))

    @property
    @compute_if_none
    def daily_cos_zenith(self) -> xr.DataArray:
        """Get daily-integrated cosine of zenith angle."""
        return ((
            self.sunset_hour_angle * np.sin(self.declination)
            * np.sin(self.lat) + np.cos(self.declination) * np.cos(self.lat)
            * np.sin(self.sunset_hour_angle))
            * 2 * (12. / np.pi))

    @property
    @compute_if_none
    def daily_mean_cos_zenith(self) -> xr.DataArray:
        """Get daily-averaged cosine of zenith angle."""
        return xr.where(
            np.fabs(self.sunset_hour_angle) > 1.e-8,
            self.daily_cos_zenith / (2 * (12. / np.pi))
            / self.sunset_hour_angle, 0.)
