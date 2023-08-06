"""Terna API for Italy."""
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
from e4clim.container.geo_data_source import GeoParsingSingleDataSourceBase
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.specific.capacityfactor import (
    download_to_compute_capacityfactor, compute_capacityfactor)
import e4clim.typing as e4tp


#: Host.
HOST: tp.Final[str] = 'https://www.terna.it/Portals/0/Resources/visualagency/data/evoluzione_mercato_elettrico/regioni/'

#: File format.
FILE_FORMAT: tp.Final[str] = 'xlsx'

#: Variable to source variable names.
SRC_VARIABLE_NAMES: tp.Final[tp.Dict[str, str]] = {
    'demand': 'consumi',
    'generation': 'produzione',
    'capacity': 'capacita'
}

#: Component to source component names.
SRC_COMPONENT_NAMES: tp.Final[tp.Dict[str, str]] = {
    'demand': 'totale',
    'wind-onshore': 'eolica',
    'pv': 'fotovoltaica',
    'hydro': 'idroelettrica',
    'bioenergy': 'bioenergie'
}

#: Variable to source sheet names.
SHEET_NAMES: tp.Final[tp.Dict[str, str]] = {
    'demand': 'trend',
    'generation': 'trend',
    'capacity': 'trend'
}

#: Rows to select.
SELECT_ROWS: tp.Final[tp.Dict[str, tp.Dict[str, str]]] = {
    'generation': {
        'netta_lorda': 'netta'
    }
}

#: Keyword arguments for :py:func:`pandas.read_excel`.
READ_EXCEL_KWARGS: tp.Final[tp.Dict[str, tp.Dict[
    str, tp.Union[int, tp.List[str]]]]] = {
    'demand': {
        'index_col': 0,
        'na_values': ['_']
    },
    'generation': {
        'index_col': 1,
        'na_values': ['_']
    },
        'capacity': {
            'index_col': 0,
            'na_values': ['_']
    }
}

#: Unit conversions.
UNIT_CONVERSIONS: tp.Final[tp.Dict[str, float]] = {
    'demand': 1.e6,
    'generation': 1.e6,
    'capacity': 1.,
    'capacityfactor': 1.e6
}

#: Units.
UNITS: tp.Final[tp.Dict[str, str]] = {
    'demand': 'MWh',
    'generation': 'MWh',
    'capacity': 'MW',
    'capacityfactor': ''
}


class DataSource(ParsingSingleDataSourceBase):
    """terna.it data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'terna'

    #: Area.
    AREA: tp.Final[str] = 'Italy'

    def __init__(self, context, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(context, name, cfg=cfg, **kwargs)

        # Add configuration for
        # :py:func:`e4clim.container.parse_data_source.ParsingDataSourceBase.finalize_array`
        self.cfg['unit_conversions'] = UNIT_CONVERSIONS
        self.cfg['units'] = UNITS

    @download_to_compute_capacityfactor
    def download(self, variable_component_names: e4tp.VCNStrictType,
                 **kwargs) -> e4tp.VCNStrictType:
        """Download data.

        :param variable_component_names: Names of components to download per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`

        .. note:: The data is downloaded from
          `Terna <https://www.terna.it/Portals/0/Resources/visualagency/data/evoluzione_mercato_elettrico/regioni/>`.

        :raises AssertionError: if :py:obj:`self.med.geo_src` is not
          :py:class:`e4clim.container.geo_data_source.GeoParsingSingleDataSourceBase`.
        """
        assert isinstance(self.med.geo_src, GeoParsingSingleDataSourceBase), (
            '"geo_src" attribute of "self.med" should be '
            '"e4clim.container.geo_data_source.GeoParsingSingleDataSourceBase"')

        # Get region names
        _, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        # Loop over variables
        for variable_name in variable_component_names:
            self.info('- {}:'.format(variable_name))

            # Loop over components
            for region_name in src_region_place:
                # Get URL
                url = self._get_url(variable_name, region_name, **kwargs)
                filepath = self._get_download_filepath(
                    variable_name, region_name, **kwargs)
                self.info('-- {} from {} to {}'.format(
                    region_name, url, filepath))

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)

        # Return names of downloaded variables
        return variable_component_names

    @compute_capacityfactor
    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get region-place mapping
        src_place_region, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        # Loop over variables
        ds = {}
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Manage wind component as onshore only
            component_name_requested = 'wind'
            component_to_load_names = component_names.copy()
            if component_name_requested in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name_requested)

            # Get source-destination component names mapping
            component_names_inv = {
                SRC_COMPONENT_NAMES[component_name]: component_name
                for component_name in component_to_load_names
            }

            # Loop over regions
            da = None
            for region_name, place_name in src_region_place.items():
                # Get filepath
                filepath = self._get_download_filepath(
                    variable_name, region_name, **kwargs)
                self.info('-- {} from {}'.format(region_name, filepath))

                # Read data frame
                df_region = pd.read_excel(
                    filepath, sheet_name=SHEET_NAMES[variable_name],
                    **READ_EXCEL_KWARGS[variable_name])

                # Select rows, if needed
                sel_row_var = SELECT_ROWS.get(variable_name)
                if sel_row_var:
                    for col, value in sel_row_var.items():
                        df_region = df_region.where(
                            df_region[col] == value).dropna(
                                axis='rows', how='all')

                # Correct typo in case needed
                df_region = df_region.rename(columns={
                    'fotovotaica': 'fotovoltaica'})

                # Rename components and select them
                df_region = df_region.rename(columns=component_names_inv)[
                    component_to_load_names]

                # Define time index
                df_region.index = pd.DatetimeIndex(
                    ['{}-12-31'.format(t) for t in df_region.index],
                    freq='A-DEC')
                df_region.index.name = 'time'

                # Select period
                time_slice = slice(
                    str(self.cfg['first_year']), str(self.cfg['last_year']))
                df_region = df_region.loc[time_slice]

                # Convert to data array
                da_region = xr.DataArray(
                    df_region, dims=('time', 'component')).astype(float)

                # Initialize array
                if da is None:
                    shape = da_region.shape + (len(src_place_region),)
                    coords = [da_region['time'], da_region['component'],
                              ('region', list(src_place_region))]
                    da = xr.DataArray(np.zeros(shape), coords=coords)

                # Add region data to place
                # keeping only NaNs present in all regions
                loc = {'region': place_name}
                da.loc[loc] = da_region.where(
                    da.loc[loc].isnull(),
                    da.loc[loc] + da_region.where(~da_region.isnull(), 0.))

            # Add variable to dataset
            ds[variable_name] = da

            # Make sure that generation and capacity NaNs match
            if ('generation' in ds) and ('capacity' in ds):
                isvalid_all = (~ds['generation'].isnull() &
                               ~ds['capacity'].isnull())
                ds['generation'] = ds['generation'].where(isvalid_all)
                ds['generation'] = ds['generation'].where(isvalid_all)

        return ds

    def _get_capacityfactor(self, ds, **kwargs):
        """Get capacity factor from generation and capacity.

        :param ds: Dataset containing generation and capacity.
        :type ds: mapping

        :returns: Capacity factor.
        :rtype: :py:class:`xarray.DataArray`
        """
        da_gen = ds['generation']
        da_cap = ds['capacity']

        # Interpolate capacity
        da_cap_int = da_cap.copy()
        da_cap_int[{'time': slice(1, len(da_cap.time))}] = (
            da_cap_int[{'time': slice(1, len(da_cap.time))}].values
            + da_cap_int[{'time': slice(0, -1)}].values) / 2

        # Get number of days in month
        time = da_gen.indexes['time']
        start = pd.Timestamp(time[0])
        end = pd.Timestamp(time[-1]) + pd.Timedelta('366 days')
        time_plus = pd.date_range(start=start, end=end, freq='Y')
        ndays = (time_plus[1:] - time_plus[:-1]).days
        da_ndays = xr.DataArray(ndays, coords=[('time', time)])
        da_nhours = da_ndays * 24

        # Get capacity factor
        da = da_gen / (da_cap_int * da_nhours)

        return da

    def _get_url(self, variable_name, region_name, **kwargs):
        """Get URL for query.

        :param variable_name: Name of variable to query.
        :param region_name: Region name.
        :type variable_name: str
        :type region_name: str

        :returns: URL.
        :rtype: str
        """
        filepath = self._get_download_filepath(
            variable_name, region_name, **kwargs)
        url = '{}/{}'.format(HOST, filepath.name)

        return url

    def _get_download_filepath(self, variable_name, region_name, **kwargs):
        """Get download filepath.

        :param variable_name: Name of variable to query.
        :param region_name: Region name.
        :type variable_name: str
        :type region_name: str

        :returns: Filepath.
        :rtype: str
        """
        # Get filename
        src_variable_name = SRC_VARIABLE_NAMES[variable_name]
        filename = '{}_{}.{}'.format(
            region_name, src_variable_name, FILE_FORMAT)

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = Path(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(self.cfg['first_year'],
                                  self.cfg['last_year'])

        return postfix
