"""ESGF API."""
from cartopy._crs import CRS
import iris
import numpy as np
from orderedset import OrderedSet
import pandas as pd
from pathlib import Path
from pyesgf.logon import LogonManager
from pyesgf.search import context, results, SearchConnection
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.gridded_data_source import (
    GriddedDataSourceBase, get_geodetic_crs, get_geodetic_array)
import e4clim.typing as e4tp
from e4clim.utils import tools


#: Variable to source variable names.
SRC_VARIABLE_NAMES: tp.Final[tp.Mapping[str, str]] = {
    'surface_temperature': 'tas',
    'zonal_wind': 'uas',
    'meridional_wind': 'vas',
    'surface_downward_radiation': 'rsds',
    'surface_specific_humidity': 'huss',
    'surface_pressure': 'ps',
    'sea_level_pressure': 'psl'
}

#: Height name.
HEIGHT_NAME = tp.Final['height']

#: Rotated latitude/longitude names.
RLATRLON: tp.Final[tp.Tuple[str, str]] = 'rlat', 'rlon'

#: X, y coordinates names.
YX: tp.Final[tp.Tuple[str, str]] = 'y', 'x'

#: Regional Climate Model to dimensions.
DIMS: tp.Final[tp.Mapping[str, tp.Tuple[str, str]]] = {
    'CMCC-CCLM4-8-19': RLATRLON,
    'GUF-CCLM4-8-18': RLATRLON,
    'IPSL-WRF311': YX,
    'CNRM-ALADIN52': YX,
    'RCA4': RLATRLON,
    'WRF331F': RLATRLON
}

#: Default height at 2m.
DEFAULT_HEIGHT: tp.Final[float] = 2.


class DataSource(GriddedDataSourceBase):
    """ESGF data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'esgf'

    #: Bootstrap to log.
    bootstrap: bool

    #: Whether dimensions should be updated.
    _dims_update_required: bool

    #: Search context.
    _search_context: tp.Optional[context.DatasetSearchContext]

    #: Whether to distribute to other hosts.
    distrib: bool

    #: Hostname.
    hostname: str

    #: Postfix.
    _postfix: tp.Optional[str]

    #: Regional Climate Model name.
    _rcm_name: tp.Optional[str]

    #: Search constraints.
    search: tp.Mapping[str, str]

    #: Simulation directory.
    _sim_dir: tp.Optional[Path]

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None, **kwargs):
        """Initialize data source.

        :param med: Mediator.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

        # Configure api
        self.hostname = tools.get_required_str_entry(self.cfg, 'hostname')
        self.distrib = tools.get_required_bool_entry(self.cfg, 'distrib', True)
        self.search = tools.get_required_mapping_entry(self.cfg, 'search')
        self.bootstrap = tools.get_required_bool_entry(
            self.cfg, 'bootstrap', True)
        self._rcm_name = tools.get_str_entry(self.search, 'rcm_name')

        self._dims_update_required = True
        self._postfix = None
        self._search_context = None
        self._sim_dir = None

    @property
    def dims(self) -> tp.Tuple[str, str]:
        """Get dimensions for Regional Climate Model."""
        if self._dims_update_required:
            self._dims = DIMS.get(self.rcm_name, RLATRLON)
            self._dims_update_required = False

        return self._dims

    @property
    def search_context(self) -> context.DatasetSearchContext:
        """Get search context."""
        if self._search_context is None:
            # Connect to search
            url_search = 'https://{}/esg-search/'.format(
                self.hostname)
            conn = SearchConnection(url_search, distrib=self.distrib)
            self._search_context = conn.new_context(**self.search)

        return self._search_context

    @property
    def postfix(self) -> str:
        """Get postfix."""
        if self._postfix is None:
            self._postfix = self._get_postfix_from_search()

        return self._postfix

    @property
    def rcm_name(self) -> str:
        """Get Regional Climate Model name."""
        if self._rcm_name is None:
            facets, fmt = _get_facets(self.search_context)

            # Set RCM name for later
            self._rcm_name = facets['rcm_name']

        return self._rcm_name

    @rcm_name.setter
    def rcm_name(self, value: tp.Optional[str]) -> None:
        """Set Regional Climate Model name."""
        self._rcm_name = value

    @property
    def sim_dir(self) -> Path:
        """Get simulation directory."""
        if self._sim_dir is None:
            facets, fmt = _get_facets(self.search_context)

            # Set RCM name for later
            self.rcm_name = facets['rcm_name']
            rcm_model = '{}-{}'.format(facets['institute'], facets['rcm_name'])

            src_dir = self.med.cfg.get_external_data_directory(self)
            fmt = '/'.join(fmt.split('/')[:-2])
            sim_str = fmt.format(
                root=src_dir, project=facets['project'], domain=facets['domain'],
                institute=facets['institute'], driving_model=facets['driving_model'],
                experiment=facets['experiment'], ensemble=facets['ensemble'],
                rcm_model=rcm_model, rcm_version=facets['rcm_version'],
                time_frequency=facets['time_frequency']
            )
            self._sim_dir = Path(*sim_str.split())

        return self._sim_dir

    def download(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.VCNType:
        """Download esgf data and save it locally.

        :param variable_component_names: Names of variables to download.
          If `None`, all variables in :py:attr:`variable_names` are downloaded.

        :returns: Names of downloaded variables.
        """
        # Get variable names
        variable_names = (
            tools.ensure_collection(variable_component_names, OrderedSet)
            or self.variable_component_names)

        self._log_with_openid()

        # Loop over all data-source variables
        for variable_name in variable_names:
            # Check if variable available
            if SRC_VARIABLE_NAMES.get(variable_name) is None:
                self.warning(
                    '{} variable not in "SRC_VARIABLE_NAMES": skipping'.format(
                        variable_name))
                continue

            self._save_datasets(self.search_context,
                                self.sim_dir, variable_name)

        return variable_names

    def parse(self, variable_component_names: e4tp.VCNType = None,
              transform: e4tp.TransformType = None, **kwargs) -> xr.Dataset:
        """Collect all required variables from esgf simulations.

        :param transform: A function or a composee of functions
          to apply to the datasets.
          These functions should take as arguments a dataset
          and a :py:class:`.data_source.DataSourceBase` data source.
        :param variable_component_names: Names of variables to download.
          If `None`, all variables in :py:attr:`variable_component_names`
          are downloaded.

        :returns: A dataset collecting all variables and periods.

        .. note:: All the variables are first read, then the functions are
          applied and the different periods are finally concatenated.
        """
        # Get variable names
        variable_names = (
            tools.ensure_collection(variable_component_names, OrderedSet)
            or self.variable_component_names)

        n_files = len(self._get_files_from_search())
        # periods = self._get_periods_from_search()

        # Collect all periods
        var_files = {}
        ds = xr.Dataset()
        read_cube, coords, src_crs, dst_crs = True, None, None, None
        # for start_date, end_date in periods:
        for ip in range(n_files):
            # Collect all variables
            ds_per = xr.Dataset()
            for variable_name in variable_names:
                # Try to get variable name
                src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
                if src_variable_name is None:
                    self.warning(
                        '{} variable not in "SRC_VARIABLE_NAMES": skipping'.format(
                            variable_name))
                    continue

                # Get file for variable and period
                if variable_name not in var_files:
                    var_files[
                        variable_name] = self._get_files_from_search(variable_name)
                f = var_files[variable_name][ip]
                url = f.opendap_url
                filepath = self._get_filepath(self.sim_dir, url, variable_name)
                self.info('Reading {} from {}'.format(variable_name, filepath))

                # Read data
                with xr.open_dataset(filepath) as ds_var:
                    # Select variable of interest to get rid of other variables
                    da = ds_var[src_variable_name].squeeze(drop=True)

                    var = _format_da_var(
                        da, variable_name, ds_var, ds_per.indexes.get('time'))

                    # Create or add variable
                    ds_per = ds_per.merge(var)

                read_cube, coords, src_crs, dst_crs = _read_cube_if_needed(
                    read_cube, coords, src_crs, dst_crs, ds_per, filepath)

            # Transform to geodetic coordinates
            ds_per = get_geodetic_array(ds_per, coords, src_crs, dst_crs)

            # Convert time at 12:00:00 to dates
            if self.search['time_frequency'] == 'day':
                td = ds_per.indexes['time']
                try:
                    ds_per.coords['time'] = pd.DatetimeIndex(td.date)
                except AttributeError:
                    told = td.to_datetimeindex(unsafe=True)
                    ds_per.coords['time'] = pd.DatetimeIndex(told.date)
                    tnew = pd.DatetimeIndex(pd.date_range(
                        start=told[0], end=told[-1], freq='D').date)
                    ds_per = ds_per.reindex(time=tnew).ffill('time')

            # Squeeze in case a one-dimensional level coordinate exists
            ds_per = ds_per.squeeze()

            # Apply functions to the dataset if given
            ds_per = tools.apply_transform(self, ds_per, transform, **kwargs)

            # Create or add period
            ds = ds.merge(ds_per)

        return ds

    def get_postfix(self, **kwargs) -> str:
        """Get standard postfix for esgf data.

        :returns: Postfix.
        """
        return self.postfix

    def get_grid_filepath(self, *args, **kwargs) -> Path:
        """Return grid filepath.

        :returns: Grid filepath.
        """
        files = self._get_files_from_search()
        f = files[0]
        url = f.opendap_url

        return self._get_filepath(self.sim_dir, url)

    def get_grid_postfix(self, *args, **kwargs) -> str:
        """Get grid postfix.

        :returns: Postfix.
        """
        rcm_name = self.rcm_name or self._get_rcm_name()

        postfix = '_{}_{}'.format(self.search['domain'], rcm_name)

        return postfix

    def _get_rcm_name(self) -> str:
        """Get Reginal Climate Model (RCM) name.

        :returns: RCM name.
        """
        facets, _ = _get_facets(self.search_context)

        self.rcm_name = facets['rcm_name']

        return self.rcm_name

    def _get_postfix_from_search(self) -> str:
        """Get postfix from search.

        :returns: Postfix.
        """
        files = self._get_files_from_search()

        url = files[0].opendap_url

        filename = _get_filename_from_url(url)

        return _get_postfix_from_filename(filename)

    def _log_with_openid(self) -> None:
        """Log with OpenID."""
        cred = self.med.cfg.get_credentials(
            self.DEFAULT_SRC_NAME, keys=['openid', 'password'])

        lm = LogonManager()
        lm.logon_with_openid(**cred, bootstrap=self.bootstrap)
        assert lm.is_logged_on(), 'Could not log as {}'.format(
            cred['openid'])
        self.info('Logged as {}'.format(cred['openid']))

    def _save_datasets(self, search_context: context.DatasetSearchContext,
                       sim_dir: Path, variable_name: str) -> None:
        """Save datasets.

        :param search_context: Context.
        :param sim_dir: Simulation directory.
        :param variable_name: Variable name.
        :param variable_name: Source variable name.
        """
        files = self._get_files_from_search(variable_name)

        # Save datasets
        for f in files:
            url = f.opendap_url
            filepath = self._get_filepath(sim_dir, url, variable_name)
            self.info('Saving {} to {}'.format(url, filepath))

            # Make local directories
            filepath.parent.mkdir(parents=True, exist_ok=True)

            ds = xr.open_dataset(url)
            ds.to_netcdf(filepath)

    def _get_filepath(self, sim_dir: Path, url: str,
                      variable_name: str = None) -> Path:
        """Get filepath from simulation directory and URL.

        :param sim_dir: Simulation directory.
        :param variable_name: Variable name.
        :param url: URL from where file is downloaded.

        :returns: Filepath.
        """
        src_variable_name = self._get_src_variable_name(variable_name)
        filename = _get_filename_from_url(url)

        return Path(sim_dir, src_variable_name, filename)

    def _get_periods_from_search(self) -> tp.List[tp.Tuple[str, str]]:
        """Get periods from search.

        :returns: Periods.
        """
        files = self._get_files_from_search()

        periods = []
        for f in files:
            periods.append(_get_dates_from_file(f))

        return periods

    def _get_files_from_search(
            self, variable_name: str = None) -> results.ResultSet:
        """Get files with search context.

        :param variable_name: Variable name.
          If `None` take first available source variable.

        :returns: Files.
        """
        src_variable_name = self._get_src_variable_name(variable_name)
        ctx_variable = self.search_context.constrain(
            variable=src_variable_name)
        assert ctx_variable.hit_count == 1, (
            '{} hits instead of 1 for {}'.format(
                ctx_variable.hit_count, src_variable_name))

        # Get files
        result = ctx_variable.search()[0]
        files = result.file_context().search()

        return files

    def _get_src_variable_name(self, variable_name: str = None) -> str:
        """Get source variable name.

        :param variable_name: Variable name.

        :returns: Source variable name.
        """
        if variable_name is None:
            src_variable_name, it = None, 0
            while src_variable_name is None:
                variable_name = list(self.variable_component_names)[it]
                src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
                it += 1
        else:
            src_variable_name = SRC_VARIABLE_NAMES[variable_name]

        return src_variable_name


def _get_facets(search_context: context.DatasetSearchContext) -> tp.Tuple[
        tp.Mapping[str, str], str]:
    """Get facets from context.

    :param search_context: Context.

    :returns: Facets and directory format template.
    """
    facets = {facet_name: list(facet)[0]
              for facet_name, facet in search_context.facet_counts.items()
              if facet}
    fmt = _get_directory_format_template(facets)

    return facets, fmt


def _get_directory_format_template(facets: tp.Mapping[str, str]) -> str:
    """Get directory format template.

    :param facets: Facets.

    :returns: Directory format template.
    """
    return facets['directory_format_template_'].replace(
        '%(', '{').replace(')s', '}').replace('{product}/', '')


def _get_dates_from_file(f: results.FileResult) -> tp.Tuple[str, str]:
    """Get dates from file.

    :param f: File.

    :returns: Dates.
    """
    url = f.opendap_url
    filename = _get_filename_from_url(url)
    dates = filename.strip('.nc').split('_')[-1].split('-')

    return dates[0], dates[1]


def _get_filename_from_url(url: str) -> str:
    """Get filename from URL.

    :param url: URL.

    :returns: Filename.
    """
    return url.split('/')[-1]


def _get_postfix_from_filename(filename: str) -> str:
    """Get postfix from filename.

    :param filename: Filename.

    :returns: Postfix.
    """
    return '_' + '_'.join(filename.split('_')[1:]).split('.')[0]


def _format_da_var(
        da: xr.Dataset, variable_name, ds_origin: xr.Dataset,
        time: pd.DatetimeIndex = None) -> xr.Dataset:
    """Clean variable data-array.

    :param da: Variable data-array.
    :param variable_name: Variable name.
    :param ds_origin: Original dataset where to find height.
    :param time: Time index.

    :returns: Formatted variable data-array.
    """
    # Ensure that the temperature is in Kelvin
    if ('temperature' in variable_name) and (da.mean() < 150.):
        da += 273.15

    # Ensure that the pressure is in Pa
    if 'pressure' in variable_name:
        da *= 10**(5 - np.round(np.log10(da.mean())))

    # Indexes x and y may change in some data set resulting
    # in erros when aligning. Just set with integers.
    if 'y' in da.coords:
        da['y'] = np.arange(da['y'].shape[0])
    if 'x' in da.coords:
        da['x'] = np.arange(da['x'].shape[0])
    ds = da.to_dataset(name=variable_name)

    ds = _add_height(ds, variable_name, ds_origin)

    # Make sure the time indexes are exactly the same (some variables use
    # 'days since', others 'hours from', which is not processed by python netcdf)
    if time is not None:
        ds['time'] = time

    return ds


def _add_height(ds: xr.Dataset, variable_name,
                ds_origin: xr.Dataset) -> xr.Dataset:
    """Add height.

    :param ds: Dataset to which to add height.
    :param variable_name: Variable name.
    :param ds_origin: Original dataset from which to try to get height.

    :returns: Dataset with height.
    """
    if HEIGHT_NAME not in ds[variable_name].attrs:
        # Add height as attribute
        if HEIGHT_NAME in ds_origin:
            ds[variable_name].attrs['height'] = float(
                ds_origin[HEIGHT_NAME])
        elif HEIGHT_NAME in ds_origin.coords:
            ds[variable_name].attrs['height'] = float(
                ds_origin.coords[HEIGHT_NAME])
        else:
            ds[variable_name].attrs['height'] = DEFAULT_HEIGHT
    else:
        # Rename
        ds[variable_name].attrs['height'] = ds[
            variable_name].attrs[HEIGHT_NAME]

    return ds


def _read_cube_if_needed(
        read_cube: bool, coords: iris.coords.DimCoord, src_crs: CRS,
        dst_crs: CRS, ds: xr.Dataset, filepath: Path) -> tp.Tuple[
            bool, iris.coords.DimCoord, CRS, CRS]:
    """Read cube if needed.

    :param read_cube: Whether to read cube.
    :param ds: Cube dataset.
    :param filepath: Filepath.

    :returns: Coordinates, source CRS, destination CRS and
      :py:obj:`read_cube` flag updated to `True`.
    """
    if (read_cube and (('lat' not in ds.coords) or
                       ('lon' not in ds.coords))):
        # Get cube from first file for coordinates
        cube = iris.load(filepath)[0]

        # Transform to geodetic coordinates
        coords, src_crs, dst_crs = get_geodetic_crs(cube)

        # Prevent further cube reading
        read_cube = False

    return read_cube, coords, src_crs, dst_crs
