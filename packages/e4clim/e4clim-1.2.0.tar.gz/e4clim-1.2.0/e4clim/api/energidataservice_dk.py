import pandas as pd
from pathlib import Path
from pkg_resources import resource_filename
import requests
import typing as tp
import xarray as xr
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.specific.capacityfactor import (
    download_to_compute_capacityfactor, compute_capacityfactor)
import e4clim.typing as e4tp


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'energidataservice_dk'

    #: Are.
    AREA: tp.Final[str] = 'Denmark'

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

    @download_to_compute_capacityfactor
    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> e4tp.VCNStrictType:
        """Download data.

        :param variable_component_names: Names of components to download per
          variable.

        :returns: Names of downloaded components per variable.

        .. note:: The data is downloaded from the
          `energidataservice.dk API <https://api.energidataservice.dk/>`

        :raises AssertionError: if :py:obj:`variable_component_names` argument
          is `None`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        # Get municipality codes
        code_region = self._get_code_region(**kwargs)

        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Manage wind component as onshore plus offshore
            component_name = 'wind'
            component_to_download_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are downloaded
                component_to_download_names.update(
                    ['wind-onshore', 'wind-offshore'])

                # Remove capacity factor from components to download
                component_to_download_names.discard(component_name)

            # Loop over components
            for component_name in component_to_download_names:
                # Get URL
                url = self._get_url(variable_name, component_name, **kwargs)
                filepath = self._get_download_filepath(
                    variable_name, component_name, **kwargs)
                self.info('-- {} from {} to {}'.format(
                    component_name, url, filepath))

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()
                records = response.json()['result']['records']

                # Convert to data frame with time as index
                df = pd.DataFrame(records).set_index(self.cfg['frequency'])
                df.index.name = 'time'

                # Sort data frame by index
                df = df.iloc[df.index.argsort()]

                # Remove 0 and 1 codes
                df = df.loc[(df['MunicipalityNo'].astype(int) != 0) &
                            (df['MunicipalityNo'].astype(int) != 1)]

                # Add municipality names
                df['region'] = [code_region.get(int(c))
                                for c in df['MunicipalityNo']]

                # Write data frame
                df.to_csv(filepath)

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
        :rtype: :py:class:`xarray.Dataset()`
        """
        # Get region names
        _, src_region_place = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Loop over variables
        ds = xr.Dataset()
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Manage wind component as onshore plus offshore
            component_name = 'wind'
            component_to_load_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.update(
                    ['wind-onshore', 'wind-offshore'])

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name)

            # Loop over components
            da = None
            for component_name in component_to_load_names:
                # Get filepath
                filepath = self._get_download_filepath(
                    variable_name, component_name, **kwargs)
                self.info('-- {} from {}'.format(component_name, filepath))

                # Read data frame
                df = pd.read_csv(filepath, index_col=0, header=0)

                # Aggregate in zones/regions
                df_place = self._aggregate_places(
                    df, src_region_place, component_name, variable_name,
                    **kwargs)

                # Convert to data array
                da_place = xr.DataArray(
                    df_place, dims=('time', 'region')).expand_dims(
                        'component').assign_coords(component=[component_name])

                # Add place data
                da = (da_place if da is None else
                      xr.concat([da, da_place], dim='component'))

                # Make sure that time index is datetime
                da['time'] = pd.DatetimeIndex(da.indexes['time'])

            # Add total wind component if needed
            component_name = 'wind'
            if component_name in component_names:
                da_wind = (da.sel(component='wind-onshore')
                           + da.sel(component='wind-offshore')).expand_dims(
                               'component').assign_coords(
                                   component=[component_name])
                da = xr.concat([da, da_wind], dim='component')

            # Select requested components
            da = da.sel(component=list(component_names))

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def _aggregate_places(self, df, src_region_place, component_name,
                          variable_name, **kwargs):
        """Aggregate data frame in places.

        :param df: Data frame to aggregate.
        :param src_region_place: Region-place mapping for data source.
        :param component_name: Component name.
        :param variable_name: Variable name.
        :type df: :py:class:`pandas.DataFrame`
        :type src_region_place: mapping
        :type component_name: str
        :type variable_name: str

        :returns: Aggregated data frame.
        :rtype: :py:class:`pandas.DataFrame`
        """
        df['place'] = [src_region_place[region_name]
                       for region_name in df['region']]
        src_component_name = '{}{}'.format(
            self.cfg['component_names'][component_name],
            self.cfg['variable_names_in_components'][variable_name])
        df = df[[src_component_name, 'place']]
        df_place = df.groupby(['time', 'place']).sum().unstack()[
            (src_component_name,)]
        df_place.columns.name = 'region'

        return df_place

    def _get_capacityfactor(self, ds, **kwargs):
        """Get capacity factor from generation and capacity.

        :param ds: Dataset containing generation and capacity.
        :type ds: mapping

        :returns: Capacity factor.
        :rtype: :py:class:`xarray.DataArray`
        """
        da_gen = ds['generation']

        # Get number of days in month
        time = da_gen.indexes['time']
        start = pd.Timestamp(time[0])
        end = pd.Timestamp(time[-1]) + pd.Timedelta('32 days')
        time_plus = pd.date_range(start=start, end=end, freq='MS')
        ndays = (time_plus[1:] - time_plus[:-1]).days
        da_ndays = xr.DataArray(ndays, coords=[('time', time)])
        da_nhours = da_ndays * 24

        # Get capacity factor
        da = da_gen / (ds['capacity'] * da_nhours)

        return da

    def _get_code_region(self, **kwargs):
        """Get regions corresponding to municipality codes.

        :returns: Code-to-region mapping.
        :rtype: mapping from :py:class:`str` to :py:class:`str`.
        """
        src_name = 'dst'
        filename = 'municipality_codes_regions.csv'
        resource_name = '../data/{}/{}/{}'.format(
            self.AREA, src_name, filename)

        # Read
        df = pd.read_csv(resource_filename(__name__, resource_name),
                         sep=';')

        code_regions = dict(zip(df['CODE'].astype(int), df['REGION']))

        return code_regions

    def _get_download_filepath(self, variable_name, component_name, **kwargs):
        """Write downloaded data for variable and component.

        :param variable_name: Name of data variable.
        :param component_name: Name of data component.
        :type variable_name: str
        :type component_name: str

        :returns: Filepath.
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        filename = '{}_{}_{}{}.csv'.format(
            self.name, component_name, variable_name,
            self.get_postfix(**kwargs))
        filepath = Path(src_dir, filename)

        return filepath

    def _get_url(self, variable_name, component_name, **kwargs):
        """Get URL for query.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :type variable_name: str
        :type component_name: str

        :returns: URL.
        :rtype: str
        """
        src_variable_name = self.cfg['variable_names'][variable_name]
        src_component_name = '{}{}'.format(
            self.cfg['component_names'][component_name],
            self.cfg['variable_names_in_components'][variable_name])
        res_label = 'res'

        # Component selection
        comp_query = '{}."{}"'.format(res_label, src_component_name)

        # Municipality query
        place_query = '{}."{}"'.format(res_label, 'MunicipalityNo')

        # Time query and selection
        time_query = '{}."{}"'.format(res_label, self.cfg['frequency'])
        time_selection = (
            'WHERE {}."{}" >= timestamp\'{}\' '
            'AND {}."{}" < timestamp\'{}\''.format(
                res_label, self.cfg['frequency'], self.cfg['start_date'],
                res_label, self.cfg['frequency'], self.cfg['end_date']))

        # SQL query
        sql_query = 'SELECT {}, {}, {} FROM "{}" as {} {}'.format(
            time_query, place_query, comp_query, src_variable_name, res_label,
            time_selection)

        # URL
        url = '{}/datastore_search_sql?sql={}'.format(
            self.cfg['host'], sql_query)

        return url

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['start_date'], self.cfg['end_date'])

        return postfix
