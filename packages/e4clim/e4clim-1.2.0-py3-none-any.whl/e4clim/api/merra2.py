"""MERRA-2 API."""
import netCDF4 as nc
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.gridded_data_source import GriddedDataSourceBase
import e4clim.typing as e4tp
from e4clim.utils import tools

#: Latitude-range type.
LatRangeType = tp.Tuple[float, float]


#: Height coordinate name.
HEIGHT_NAME: tp.Final[str] = 'height'

#: Variable to source variable names.
SRC_VARIABLE_NAMES: tp.Final[tp.Dict[str, str]] = {
    'surface_density': 'RHOA',
    'surface_temperature': 'TLML',
    'surface_specific_humidity': 'QLML',
    'surface_downward_radiation': 'SWGDN',
    'zonal_wind': 'U10M',
    'upper_zonal_wind': 'U50M',
    'meridional_wind': 'V10M',
    'upper_meridional_wind': 'V50M',
    'surface_temperature_max': 'T2MMAX',
    'height_500': 'H500'
}

#: Variable to source group names.
GROUP_NAMES: tp.Final[tp.Dict[str, str]] = {
    'surface_density': 'flx',
    'surface_temperature': 'flx',
    'surface_specific_humidity': 'flx',
    'surface_downward_radiation': 'rad',
    'zonal_wind': 'slv',
    'meridional_wind': 'slv',
    'upper_zonal_wind': 'slv',
    'upper_meridional_wind': 'slv',
    'surface_temperature_max': 'slv',
    'height_500': 'slv'
}

#: Streams.
STREAMS: tp.Final[tp.Dict[int, tp.Dict[str, str]]] = {
    1: {
        'start_date': '19800101',
        'end_date': '19920101'
    },
    2: {
        'start_date': '19920101',
        'end_date': '20010101'
    },
    3: {
        'start_date': '20010101',
        'end_date': '20110101'
    },
    4: {
        'start_date': '20110101',
        'end_date': '20210101'
    }
}

#: Host.
HOST: tp.Final[str] = 'https://goldsmr4.gesdisc.eosdis.nasa.gov'

#: GEOS5 version.
GEOS5_VERSION: tp.Final[str] = '5.12.4'

#: Latitude step.
DELTA_LAT: tp.Final[float] = 0.5

#: Longitude step.
DELTA_LON: tp.Final[float] = 0.625

#: File format.
FORMAT: tp.Final[str] = 'nc4'

#: Version.
VERSION: tp.Final[str] = '00'

#: Default maximum fetch-trials.
DEFAULT_MAX_FETCH_TRIALS: tp.Final[int] = 50

#: Frequency code.
FREQ_CODES: tp.Final[tp.Mapping[str, str]] = {
    'hour': '1', '3hour': '3', 'day': 'D', 'month': 'M'}

#: File sampling.
FILE_SAMPLING: tp.Final[tp.Mapping[str, str]] = {
    'hour': 'D', '3hour': 'D', 'day': 'D', 'month': 'M'}

#: Frequency-dependent directory.
DIR_FREQ: tp.Final[tp.Mapping[str, str]] = {
    'hour': '', '3hour': '', 'day': '', 'month': '_MONTHLY'}

#: Time-description code.
TIME_DESCRIPTION_CODES: tp.Final[tp.Mapping[str, str]] = {
    'cnst': 'C', 'inst': 'I', 'stat': 'S', 'tavg': 'T'}


class DataSource(GriddedDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'merra2'

    # Latitude range.
    lat_range: LatRangeType

    # Longitude range.
    lon_range: LatRangeType

    # Maximum fetch trials
    max_fetch_trials: int

    # Time range.
    time_range: tp.Optional[tp.Tuple[int]]

    #: Server parent directory.
    srv_parent_dir: str

    #: Time range string.
    time_range_str: str

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None, **kwargs):
        """Initialize data source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

        # Time range
        time_range = self.cfg.get('time_range')
        if time_range is None:
            if ((self.cfg['time_description'] == 'stat')
                    or (self.cfg['frequency'] == 'month')):
                # Only one sample per day
                self.time_range_str = '[0:0]'
            elif self.cfg['time_description'] == 'tavg':
                # Default: get 24 hours of day
                self.time_range_str = '[0:23]'
        else:
            # User-defined time range
            time_range_safe = time_range
            assert isinstance(time_range_safe, tuple), (
                'Time range in configuration must be "tuple"')
            self.time_range_str = '[{}:{}]'.format(
                time_range_safe[0], time_range_safe[1])

        host_dir = (self.DEFAULT_SRC_NAME.upper()
                    + DIR_FREQ[str(self.cfg['frequency'])])
        self.srv_parent_dir = '{}/opendap/hyrax/{}/{}{}{}{}{}'.format(
            HOST, host_dir, self.cfg['data_name'],
            TIME_DESCRIPTION_CODES[str(self.cfg['time_description'])],
            FREQ_CODES[str(self.cfg['frequency'])],
            self.cfg['horizontal_resolution'],
            str(self.cfg['vertical_location']).upper())

        self.max_fetch_trials = tools.get_required_int_entry(
            self.cfg, 'max_fetch_trials', DEFAULT_MAX_FETCH_TRIALS)

    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> e4tp.VCNStrictType:
        """Download merra2 data and save it to disk.

        :param variable_component_names: Names of variables to download.
          If `None`, :py:attr:`variable_component_names` are downloaded.

        :returns: Names of downloaded variables.

        :raises AssertionError: if :py:obj:`variable_component_names`
          argument is `None`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq=FILE_SAMPLING[str(self.cfg['frequency'])], inclusive='left')
        for date in date_range:
            for variable_name in variable_component_names:
                # Download data for date and variable
                self._download_date_variable(
                    date, variable_name, download=True, **kwargs)

        return variable_component_names

    def parse(self, variable_component_names: e4tp.VCNType = None,
              transform: e4tp.TransformType = None, **kwargs) -> xr.Dataset:
        """Collect all required variables from the MERRA-2 re-analysis.

        :param transform: A function or a composee of functions
          to apply to the datasets.
          These functions should take as arguments a dataset and a
          :py:class:`e4clim.container.data_source.DataSourceBase` data source.
        :param variable_componentnames: Names of variables to download.
          If `None`, all variables in :py:attr:`variable_component_names`
          are downloaded.

        :returns: A dataset collecting all variables and periods.

        :raises AssertionError: if :py:obj:`variable_component_names`
          argument is `None`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq=FILE_SAMPLING[str(self.cfg['frequency'])], inclusive='left')
        ds = xr.Dataset()
        for date in date_range:
            ds_per = self._load_date(date, variable_component_names,
                                     transform, **kwargs)

            # Create or add period
            ds = xr.concat([ds, ds_per], dim='time') if ds else ds_per

        ds = self._set_time(ds)

        return ds

    def get_grid_filepath(self, *args, **kwargs) -> Path:
        """Return grid filepath.

        :returns: Grid filepath.
        """
        _, file_dir, filename = self._get_url_dir_file()

        return Path(file_dir, filename)

    def get_grid_postfix(self, *args, **kwargs) -> str:
        """Grid postfix.

        :returns: Postfix.
        """
        postfix = '_{}{}'.format(self.cfg['horizontal_resolution'],
                                 self.cfg['vertical_location'])

        return postfix

    def get_postfix(self, start_date: str = None,
                    end_date: str = None, **kwargs) -> str:
        """Get postfix for the MERRA-2 data.

        :param start_date: Simulation start-date. If `None`,
          the first date of `self.cfg['start_date']` is used.
        :param end_date: Simulation end-date. If `None`,
          the first date of `self.cfg['end_date']` is used.

        :returns: Postfix.
        """
        start_date = start_date or str(self.cfg['start_date'])
        end_date = end_date or str(self.cfg['end_date'])

        # Get paths
        postfix = '_{}_{}-{}'.format(self.cfg['frequency'],
                                     start_date, end_date)

        return postfix

    def _load_date(self, date: pd.Timestamp, variable_names: e4tp.VCNType,
                   transform: e4tp.TransformType = None, **kwargs) -> xr.Dataset:
        """Load data for period.

        :param date: Date for which to load data.
        :param variable_names: Variable names.
        :param transform: A function or a composee of functions
          to apply to the datasets.

        :returns: Dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        ds = xr.Dataset()
        self.info('Reading data for {}'.format(date.date()))
        for variable_name in variable_names:
            ds_var = self._load_variable(date, variable_name, **kwargs)
            if ds_var is None:
                continue

            # Merge variable
            ds = ds.merge(ds_var)
            ds_var.close()

        # Remove conflicting attributes to avoid
        # AttributeError: NetCDF: String match to name in use
        self._remove_conflicting_attributes(ds)

        # Apply functions to the dataset if given
        ds = tools.apply_transform(self, ds, transform, **kwargs)

        return ds

    def _load_variable(self, date: pd.Timestamp, variable_name: str,
                       **kwargs) -> tp.Optional[xr.Dataset]:
        """Load data for variable.

        :param date: Date for which to load data.
        :param variable_name: Variable name.

        :returns: Dataset.
        """
        src_variable_name = SRC_VARIABLE_NAMES[variable_name]

        # Read data for date and variable
        ds = self._download_date_variable(
            date, variable_name, download=False, **kwargs)
        if ds is None:
            return None

        # Add height
        self._add_height(ds)

        # Rename variable
        rename_dict = tp.cast(tp.Mapping[str, tp.Hashable],
                              {src_variable_name: variable_name})
        ds = ds.rename(**rename_dict)

        return ds

    def _remove_conflicting_attributes(self, ds: xr.Dataset) -> None:
        """Remove conflicting attributes from dataset.

        :param ds: Dataset.
        """
        try:
            del ds.time.attrs['CLASS']
            del ds.time.attrs['NAME']
        except KeyError:
            pass

    def _set_time(self, ds: xr.Dataset) -> xr.Dataset:
        """Set time index by change hour interval representation convention
        from center to left.

        :param ds: Dataset for which to set time index.

        :returns: Dataset with new time index
        """
        t = ds.indexes['time']
        index_parts = {'year': t.year, 'month': t.month, 'day': t.day}
        if self.cfg['frequency'] == 'hour':
            index_parts['hour'] = t.hour
        new_index = pd.to_datetime(index_parts)
        ds = ds.reindex(time=new_index, method='bfill')
        ds.time.encoding['units'] = "hours since 1980-01-01T00:00:00"

        return ds

    def _get_url_dir_file(self, variable_name: str = None,
                          date: pd.Timestamp = None) -> tp.Tuple[
                              str, Path, str]:
        """Get variable URL, directory and filename for MERRA-2 data.

        :param variable_name: Variable name.
        :param date: Date for which to return paths.
          If `None`, use `'start_date'` value of data-source configuration.

        returns: Source URL, directory and filename.
        """
        self._set_lat_lon_range()

        # Define grid string
        domain = '{}{}{}'.format(self.time_range_str, self.lat_range_str,
                                 self.lon_range_str)
        short_time_range_str = ('' if self.cfg['space'] == '2d'
                                else self.time_range_str)
        grid_list = 'time{},lat{},lon{}'.format(
            short_time_range_str, self.lat_range_str, self.lon_range_str)

        # Get data-source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get given date or start date
        date = pd.Timestamp(date or self.cfg['start_date'])

        # Get runid of stream containg date
        for stream, cfg_stream in STREAMS.items():
            ssd = pd.Timestamp(cfg_stream['start_date'])
            sed = pd.Timestamp(cfg_stream['end_date'])
            if (date >= ssd) & (date < sed):
                break
        runid = '{}{}'.format(stream, VERSION)
        freq = '{}{}'.format(self.cfg['time_description'],
                             FREQ_CODES[str(self.cfg['frequency'])])
        prefix0 = '{}_{}.{}_{}'.format(
            self.DEFAULT_SRC_NAME.upper(), runid, freq, self.cfg['space'])

        if variable_name is None:
            # Take first variable in a group
            group_name = None
            it = 0
            while group_name is None:
                variable_name_safe = list(self.variable_component_names)[it]
                group_name = GROUP_NAMES[variable_name_safe]
                it += 1
        else:
            # Try to get group of variable
            group_name = GROUP_NAMES[variable_name]
            variable_name_safe = variable_name
        src_variable_name = SRC_VARIABLE_NAMES[variable_name_safe]

        # Make local directories
        file_dir = Path(src_dir, group_name)
        file_dir.mkdir(parents=True, exist_ok=True)

        # Frequency dependent variables
        date_dir = '{:04d}'.format(date.year)
        if self.cfg['frequency'] in ['hour', 'day']:
            date_dir += '/{:02d}'.format(date.month)
            date_file = date.strftime('%Y%m%d')
        else:
            date_file = date.strftime('%Y%m')

        HV = '{}{}'.format(self.cfg['horizontal_resolution'],
                           self.cfg['vertical_location'])
        prefix = '{}_{}_{}.{}.{}'.format(
            prefix0, group_name, HV, date_file, FORMAT)
        postfix = '{}{},{}'.format(src_variable_name, domain, grid_list)
        filename = '{}.nc?{}'.format(prefix, postfix)

        srv_dir = '{}{}.{}'.format(
            self.srv_parent_dir, group_name.upper(), GEOS5_VERSION)
        url = '{}/{}/{}'.format(srv_dir, date_dir, filename)

        return url, file_dir, filename

    def _set_lat_lon_range(self) -> None:
        """Get latitude and longitude ranges."""
        lat_range = tools.get_iterable_float_entry(
            self.cfg, 'lat_range', tuple)
        lon_range = tools.get_iterable_float_entry(
            self.cfg, 'lon_range', tuple)

        if (not lat_range) or (not lon_range):
            self._set_lat_lon_range_from_geo_bounds()
        else:
            assert len(lat_range) == 2, '"lat_range" should be of length 2"'
            assert len(lon_range) == 2, '"lon_range" should be of length 2"'
            self.lat_range = tp.cast(LatRangeType, lat_range)
            self.lon_range = tp.cast(LatRangeType, lon_range)

        # Convert lat/lon range to indices string
        self._set_lat_lon_range_str()

    def _set_lat_lon_range_from_geo_bounds(self) -> None:
        """Get latitude and longitude ranges from bounds of geographic
        data source.

        :raises AssertionError: if :py:obj:`self.med.geo_src` is `None`.
        """
        assert self.med.geo_src is not None, (
            '"geo_src" attribute of "self.med" required')

        # Get total bounds in geoid system
        lon_min, lat_min, lon_max, lat_max = (
            self.med.geo_src.get_total_bounds(epsg=4326))

        # Set ranges
        self.lat_range = lat_min, lat_max
        self.lon_range = lon_min, lon_max

    def _set_lat_lon_range_str(self) -> None:
        """Convert lat/lon range to indices string."""
        lat_min = self.lat_range[0]
        lat_max = self.lat_range[1]
        lon_min = self.lon_range[0]
        lon_max = self.lon_range[1]

        # Convert bounds to grid indices
        ilon_min = self._get_index_lon(lon_min)
        ilon_max = self._get_index_lon(lon_max) + 1
        ilat_min = self._get_index_lat(lat_min)
        ilat_max = self._get_index_lat(lat_max) + 1

        # Get grid string
        self.lon_range_str = '[{:d}:{:d}]'.format(ilon_min, ilon_max)
        self.lat_range_str = '[{:d}:{:d}]'.format(ilat_min, ilat_max)

    def _get_index_lon(self, lon: float) -> int:
        """Get grid index corresponding to longitude.

        :param lon: Longitude.

        :returns: Longitude grid-index.
        """
        ilon = (lon + 180.) / DELTA_LON
        ilon = int(ilon + 0.1)

        return ilon

    def _get_index_lat(self, lat: float) -> int:
        """Get grid index corresponding to latitude.

        :param lat: Latitude.

        :returns: Latitude grid-index.
        :rtype: :py:class:`int`, :py:class:`numpy.array`
        """
        ilat = (lat + 90.) / DELTA_LAT
        ilat = int(ilat + 0.1)

        return ilat

    def _download_request(self, url: str) -> xr.Dataset:
        """Download data over HTTP - OPeNDAP.

        :param url: OPeNDAP URL.

        :returns: Dataset.
        """
        # Request and raise exception if needed
        response = requests.get(url)
        response.raise_for_status()

        # Convert bytes to netCDF4.Dataset
        ds_nc = nc.Dataset(filename='dum.nc', memory=response.content)

        # Convert netCDF4.Dataset to xarray.Dataset
        ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds_nc))

        return ds

    def _download_date_variable(
            self, date: pd.Timestamp, variable_name: str,
            download: bool = False, **kwargs) -> tp.Optional[xr.Dataset]:
        """Download data for given date and variable.

        :param date: Date.
        :param variable_name: Variable name.
        :param download: Whether to direclty download data, or to try to
          read it from disk first.
          If `False`, an attempt is made to read first.
        """
        # Get group name for variable
        group_name = GROUP_NAMES.get(variable_name)
        src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
        if (src_variable_name is None) or (group_name is None):
            self.warning(
                '{} variable not in "SRC_VARIABLE_NAMES": skipping'.format(
                    variable_name))
            return None

        # Get paths
        url, file_dir, filename = self._get_url_dir_file(
            variable_name=variable_name, date=date)
        filepath = Path(file_dir, filename)

        ds, n_trials = self._fetch_data(url, download, filepath, group_name)

        self._write_if_success(ds, n_trials, download, filepath, group_name)

        return ds

    def _fetch_data(self, url: str, download: bool, filepath: e4tp.PathType,
                    group_name: str) -> tp.Tuple[xr.Dataset, int]:
        """Fetch data.

        :param url: URL from which to download.
        :param download: Whether to download data.
        :param filepath: Path of file to download.
        :param group_name: Group of variables to download.

        :returns: Dataset and number of trials.
        """
        n_trials = 0
        while n_trials < self.max_fetch_trials:
            try:
                if (not download) and (n_trials == 0):
                    # Read previously downloaded data
                    ds = xr.open_dataset(filepath)
                else:
                    # Try to fetch
                    self.info('Fetching {} group from {}'.format(
                        group_name, url))
                    ds = self._download_request(url)

                # Check quality
                if self.cfg.get('check_quality'):
                    _quality_check(ds)

                # Everything went well -> leave trials loop
                break
            except (OSError, RuntimeError,
                    AttributeError, ValueError) as e:
                # Retry
                self.warning('Fetching trial {:d} failed: {}'.format(
                    n_trials + 1, str(e)))
                n_trials += 1
                continue

        return ds, n_trials

    def _write_if_success(
            self, ds: xr.Dataset, n_trials: int, download: bool,
            filepath: e4tp.PathType, group_name: str) -> None:
        """Write dataset if last fetch trial succeeded.

        :param ds: Dataset to write.
        :param n_trials: Number of fetch trials.
        :param download: Whether to download data.
        :param filepath: Path to which to write downloaded file.
        :param group_name: Group of variables to download.
        """
        if n_trials >= self.max_fetch_trials:
            # All trials failed
            self.critical('Fetching failed after {:d} trials.'.format(
                n_trials))
            raise RuntimeError
        elif download or (n_trials > 0):
            # Write data
            self.info('Writing {} group to {}'.format(group_name, filepath))
            ds.to_netcdf(filepath)

    def _add_height(self, ds: xr.Dataset) -> None:
        """Add or rename `'height'` variable to dataset attributes.

        :param ds: Dataset.
        """
        for svn in ds.data_vars:
            variable_name = str(svn)
            var = ds[variable_name]
            if HEIGHT_NAME not in var.attrs:
                # Add height as attribute
                if HEIGHT_NAME in ds:
                    var.attrs['height'] = float(
                        ds[HEIGHT_NAME])
                elif HEIGHT_NAME in ds.coords:
                    var.attrs['height'] = float(
                        ds.coords[HEIGHT_NAME])
                elif variable_name[0] in ['U', 'V']:
                    # Get height from wind name
                    var.attrs['height'] = float(
                        variable_name[1:variable_name.find('M')])
                else:
                    # Assume height of 2m
                    var.attrs['height'] = 2.
            else:
                # Rename
                var.attrs['height'] = var.attrs[HEIGHT_NAME]


def _quality_check(ds: xr.Dataset) -> None:
    """Check integrity of downloaded dataset. If dataset is invalid,
    `ValueError` is raised.

    :param ds: Dataset to check.

    :raises ValueError: if "time" index is wrong (i.e. when year is 1970),
      or if any values are null or larger than "1e10".
    """
    # Time index
    if (ds.indexes['time'].year == 1970).any():
        raise ValueError

    # NaN and Infinite values
    for da in ds.values():
        if da.isnull().any() or (da > 1e10).any():
            raise ValueError
