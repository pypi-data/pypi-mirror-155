"""CORDEX API."""
import ftplib
import iris
import numpy as np
from orderedset import OrderedSet
import pandas as pd
from pathlib import Path
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.gridded_data_source import (
    GriddedDataSourceBase, get_geodetic_crs, get_geodetic_array)
import e4clim.typing as e4tp
from e4clim.utils import tools

#: Server.
HOST: tp.Final[str] = 'www.medcordex.eu'

#: Height coordinate name.
HEIGHT_NAME: tp.Final[str] = 'height'

#: Variable to source variable names.
SRC_VARIABLE_NAMES: tp.Final[tp.Dict[str, str]] = {
    'surface_temperature': 'tas',
    'surface_temperature_max': 'tasmax',
    'zonal_wind': 'uas',
    'meridional_wind': 'vas',
    'surface_downward_radiation': 'rsds',
    'surface_specific_humidity': 'huss',
    'surface_pressure': 'ps',
    'sea_level_pressure': 'psl'
}

#: Dimensions.
DIMS: tp.Final[tp.Dict[str, tp.Tuple[str, str]]] = {
    'CMCC-CCLM4-8-19': ('rlat', 'rlon'),
    'GUF-CCLM4-8-18': ('rlat', 'rlon'),
    'IPSL-WRF311': ('y', 'x'),
    'CNRM-ALADIN52': ('y', 'x')
}


class DataSource(GriddedDataSourceBase):
    """MED-CORDEX data source.

        .. seealso::
            * `cordex variables requirements table <https://www.medcordex.eu/cordex_variables_requirement_table_110628.pdf>`
            * `cordex archive specifications <http://cordex.dmi.dk/joomla/images/cordex/cordex_archive_specifications.pdf>`
    """
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'cordex'

    #: Start dates.
    start_dates: tp.Sequence[str]

    #: End dates.
    end_dates: tp.Sequence[str]

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None, **kwargs):
        """Initialize data source.

        :param med: Mediator.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

        # Set geographic dimensions of regional model
        cfg_rcm_model_name = tools.get_required_str_entry(
            self.cfg, 'rcm_model_name')
        dims = DIMS[cfg_rcm_model_name]
        self._dims = dims[0], dims[1]

        experiment_name = tools.get_required_str_entry(
            self.cfg, 'cmip5_experiment_name')
        cfg_streams = tools.get_required_mapping_entry(self.cfg, 'streams')
        if 'rcp' in experiment_name:
            cfg_rcp = tools.get_required_mapping_entry(cfg_streams, 'rcp')
            self.start_dates = tools.get_required_iterable_str_entry(
                cfg_rcp, 'start_dates', list)
            self.end_dates = tools.get_required_iterable_str_entry(
                cfg_rcp, 'end_dates', list)
        else:
            self.start_dates = cfg_streams[experiment_name]['start_dates']
            self.end_dates = cfg_streams[experiment_name]['end_dates']

    def download(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.VCNType:
        """Download cordex data and save it locally.

        :param variable_component_names: Names of variables to download.
          If `None`, all variables in :py:attr:`variable_names` are downloaded.

        :returns: Names of downloaded variables.

        .. note:: The Med-cordex data is available on the
          `Med-cordex website <https://www.medcordex.eu/>`.
        """
        # Get variable names
        variable_names = (
            tools.ensure_collection(variable_component_names, OrderedSet)
            or self.variable_component_names)

        # Define data directories
        sim_dir = self._get_sim_dir()

        # Get credentials
        cred = self.med.cfg.get_credentials(
            self.DEFAULT_SRC_NAME, keys=['user', 'passwd'])

        # Login to the FTP server
        ftp = ftplib.FTP(HOST)
        ftp.login(**cred)
        ftp.cwd(str(sim_dir))

        svar = ', '.join(str(variable_name)
                         for variable_name in variable_names)
        self.info('{} variables for {} simulation'.format(svar, sim_dir))

        # Loop over all data-source variables
        for variable_name in variable_names:
            # Try to get variable name
            src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
            if src_variable_name is None:
                self.warning(
                    '{} variable not in "SRC_VARIABLE_NAMES": '
                    'skipping'.format(variable_name))
                continue
            else:
                src_variable_name_safe = str(src_variable_name)

            # Loop over periods
            for start_date, end_date in zip(
                    self.start_dates, self.end_dates):
                # Get paths
                var_dir, var_file = self._get_var_dir_file(
                    variable_name=variable_name, start_date=start_date,
                    end_date=end_date)

                # Make local directories
                var_dir.mkdir(parents=True, exist_ok=True)

                filepath = Path(var_dir, var_file)
                retr_string = 'RETR {}/{}'.format(
                    src_variable_name_safe, var_file)
                ftp.retrbinary(retr_string, open(filepath, 'wb').write)

        # Close
        ftp.close()

        return variable_names

    def parse(self, variable_component_names: e4tp.VCNType = None,
              transform: e4tp.TransformType = None, **kwargs) -> xr.Dataset:
        """Collect all required variables from cordex simulations.

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

        # Collect all periods
        ds = xr.Dataset()
        read_cube, coords, src_crs, dst_crs = True, None, None, None
        for start_date, end_date in zip(
                self.start_dates, self.end_dates):
            # Collect all variables
            ds_per = xr.Dataset()
            for variable_name in variable_names:
                # Get paths
                src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
                if src_variable_name is None:
                    self.warning(
                        '{} variable not in "variable_names": '
                        'skipping'.format(variable_name))
                    continue
                var_dir, var_file = self._get_var_dir_file(
                    variable_name=variable_name, start_date=start_date,
                    end_date=end_date)
                filepath = Path(var_dir, var_file)
                self.info('Reading {} from {}'.format(variable_name, filepath))

                # Read data
                with xr.open_dataset(filepath) as ds_var:
                    # Select variable of interest to get rid of other variables
                    da = ds_var[src_variable_name].squeeze(drop=True)

                    # Ensure that the temperature is in Kelvin
                    if 'temperature' in variable_name:
                        if da.mean() < 150.:
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
                    var = da.to_dataset(name=variable_name)

                    if HEIGHT_NAME not in var[variable_name].attrs:
                        # Add height as attribute
                        if HEIGHT_NAME in ds_var:
                            var[variable_name].attrs['height'] = float(
                                ds_var[HEIGHT_NAME])
                        elif HEIGHT_NAME in ds_var.coords:
                            var[variable_name].attrs['height'] = float(
                                ds_var.coords[HEIGHT_NAME])
                        else:
                            # Assume 2m height
                            var[variable_name].attrs['height'] = 2.
                    else:
                        # Rename
                        var[variable_name].attrs['height'] = var[
                            variable_name].attrs[HEIGHT_NAME]

                    # Make sure the time indexes are exactly the same
                    # (some variables use 'days since', others
                    # 'hours from',
                    # which is not processed by python netcdf)
                    if 'time' in ds_per:
                        var['time'] = ds_per['time']

                    # Create or add variable
                    ds_per = ds_per.merge(var)

                if (read_cube and
                    (('lat' not in ds_per.coords) or
                     ('lon' not in ds_per.coords))):
                    # Get cube from first file for coordinates
                    cube = iris.load(filepath)[0]

                    # Transform to geodetic coordinates
                    coords, src_crs, dst_crs = get_geodetic_crs(cube)

                    # Prevent further cube reading
                    read_cube = False

            # Transform to geodetic coordinates
            ds_per = get_geodetic_array(ds_per, coords, src_crs, dst_crs)

            # Convert time at 12:00:00 to dates
            if self.cfg['frequency'] == 'day':
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

    def get_postfix(self, start_date: str = None, end_date: str = None,
                    **kwargs) -> str:
        """Get standard postfix for cordex data.

        :param start_date: Simulation start-date.
          If `None`, the first date of :py:attr::`start_dates` is used.
        :param end_date: Simulation end-date.
          If `None`, the first date of :py:attr::`end_dates` is used.

        :returns: Postfix.
        """
        start_date = start_date or self.start_dates[0]
        end_date = end_date or self.end_dates[-1]

        # Get paths
        fmt = (self.cfg['domain'], self.cfg['gcm_model_name'],
               self.cfg['cmip5_experiment_name'],
               self.cfg['cmip5_ensemble_member'],
               self.cfg['rcm_model_name'], self.cfg['rcm_version_id'],
               self.cfg['frequency'], start_date, end_date)
        postfix = '_{}_{}_{}_{}_{}_{}_{}_{}-{}'.format(*fmt)

        return postfix

    def _get_sim_dir(self, **kwargs) -> Path:
        """Get simulation directory of cordex data.

        returns: Source directory and filename.
        """
        sim_dir = Path(
            str(self.cfg['domain']), str(self.cfg['institution']),
            str(self.cfg['gcm_model_name']),
            str(self.cfg['cmip5_experiment_name']),
            str(self.cfg['cmip5_ensemble_member']),
            str(self.cfg['rcm_model_name']),
            str(self.cfg['rcm_version_id']), str(self.cfg['frequency']))

        return sim_dir

    def get_grid_filepath(self, *args, **kwargs) -> Path:
        """Return grid filepath.

        :returns: Grid filepath.
        """
        var_dir, var_file = self._get_var_dir_file()

        return Path(var_dir, var_file)

    def get_grid_postfix(self, *args, **kwargs) -> str:
        """Get grid postfix.

        :returns: Postfix.
        """
        postfix = '_{}_{}'.format(
            self.cfg['domain'], self.cfg['rcm_model_name'])

        return postfix

    def _get_var_dir_file(
            self, variable_name: str = None, start_date: str = None,
            end_date: str = None) -> tp.Tuple[Path, Path]:
        """Get variable directory and filename for cordex data.

        :param variable_name: Package name of variable for which to get
          information.
          If `None`, the first variable in :py:attr::`variables` list is taken.
        :param start_date: Simulation start-date.
        :param end_date: Simulation end-date.

        returns: Source directory and filename.
        """
        # Take first dates if not given
        start_date = start_date or self.start_dates[0]
        end_date = end_date or self.end_dates[0]

        if variable_name is None:
            src_variable_name, it = None, 0
            while src_variable_name is None:
                variable_name = list(self.variable_component_names)[it]
                src_variable_name = SRC_VARIABLE_NAMES.get(variable_name)
                it += 1
        else:
            src_variable_name = SRC_VARIABLE_NAMES[variable_name]
        src_variable_name_safe = src_variable_name

        src_dir = self.med.cfg.get_external_data_directory(self)
        sim_dir = self._get_sim_dir()
        var_dir = Path(src_dir, sim_dir, src_variable_name_safe)
        postfix = self.get_postfix(
            start_date=start_date, end_date=end_date)
        var_file = Path('{}{}.nc'.format(src_variable_name_safe, postfix))

        return var_dir, var_file
