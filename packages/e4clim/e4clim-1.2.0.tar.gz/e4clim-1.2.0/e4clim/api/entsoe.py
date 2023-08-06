"""ENTSOE API."""
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError
from entsoe.mappings import PSRTYPE_MAPPINGS
import numpy as np
import pandas as pd
from pathlib import Path
import typing as tp
import xarray as xr
from e4clim.container.geo_data_source import get_country_code
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp

#: Timezone.
TZ: tp.Final[str] = 'UTC'

#: Variable to source variable names.
SRC_VARIABLE_NAMES: tp.Final[tp.Dict[str, str]] = {
    'generation': 'generation',
    'capacity': 'installed_generation_capacity',
    'wind_and_solar_forecast': 'wind_and_solar_forecast',
    'crossborder_flows': 'crossborder_flows',
    'imbalance_prices': 'imbalance_prices',
    'unavailability_of_generation_units': 'unavailability_of_generation_units',
    'withdrawn_unavailability_of_generation_units':
    'withdrawn_unavailability_of_generation_units',
    'price-dayahead': 'day_ahead_prices',
    'demand': 'load',
    'load_forecast': 'load_forecast',
    'generation_forecast': 'generation_forecast'
}

#: Component to source component names.
SRC_COMPONENT_NAMES: tp.Final[tp.Dict[str, str]] = {
    'pv': 'Solar',
    'wind-onshore': 'Wind Onshore',
    'wind-offshore': 'Wind Offshore',
    'demand': 'Demand',
    'price-dayahead': 'Day Ahead Prices'
}

#: Units.
UNITS: tp.Final[tp.Dict[str, str]] = {
    'demand': 'MWh',
    'price-dayahead': '€',
    'generation': 'MWh',
    'capacity': 'MW',
    'capacityfactor': ''
}

#: Is source variable with PSR type?
SRC_VARIABLE_WITH_PSR: tp.Final[tp.Mapping[str, bool]] = {
    'day_ahead_prices': False, 'load': False, 'load_forecast': False,
    'wind_and_solar_forecast': True, 'generation_forecast': False,
    'generation': True, 'installed_generation_capacity': True,
    'crossborder_flows': False, 'imbalance_prices': True,
    'unavailability_of_generation_units': False,
    'withdrawn_unavailability_of_generation_units': False
}
#: Lookup building zones for source variable?
SRC_VARIABLE_WITH_BZONES: tp.Final[tp.Mapping[str, bool]] = {
    'day_ahead_prices': False, 'load': False, 'load_forecast': False,
    'wind_and_solar_forecast': True, 'generation_forecast': False,
    'generation': True, 'installed_generation_capacity': False,
    'crossborder_flows': True, 'imbalance_prices': False,
    'unavailability_of_generation_units': False,
    'withdrawn_unavailability_of_generation_units': False,
    'generation_per_plant': True
}


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'entsoe'

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
        self.cfg['units'] = UNITS

    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> e4tp.VCNStrictType:
        """Download data.

        :param variable_component_names: Names of components to download per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`

        .. note:: The data is downloaded from the
          `ENTSO-E Transparency Platform <https://transparency.entsoe.eu/>`.

        :raises AssertionError: if :py:obj:`variable_component_names` argument
          is `None`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        # Define start and end dates (ISO format)
        start = pd.Timestamp(self.cfg['period_start'], tz=TZ)
        end = pd.Timestamp(self.cfg['period_end'], tz=TZ)
        svar = ', '.join(str(variable_name)
                         for variable_name in variable_component_names)
        self.info('{} variables from {} to {}:'.format(svar, start, end))

        # Get credentials and start ENTSO-E client
        cred = self.med.cfg.get_credentials(
            self.DEFAULT_SRC_NAME, ['security_token'])
        client = EntsoePandasClient(api_key=cred['security_token'])

        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Define query
            src_variable_name = SRC_VARIABLE_NAMES[variable_name]
            query = getattr(client, 'query_{}'.format(src_variable_name))

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
                # Get zone-code mapping and place-lookup mapping
                place_code, place_lookup = self._get_place_code(
                    variable_name, component_name=component_name, **kwargs)

                src_component_name = self.cfg['component_names'][
                    component_name]
                query_kwargs = {}
                vstr = '-- {} -> {}'.format(component_name, src_component_name)
                if SRC_VARIABLE_WITH_PSR[src_variable_name]:
                    psr_type = [k for k, v in PSRTYPE_MAPPINGS.items()
                                if v == src_component_name][0]
                    query_kwargs['psr_type'] = psr_type
                    vstr += '-> {}:'.format(psr_type)
                self.info(vstr)

                for place_name, code in place_code.items():
                    self.info('--- {}'.format(place_name))
                    try:
                        # Check whether to lookup building zones
                        query_bz_kwargs = query_kwargs.copy()
                        if SRC_VARIABLE_WITH_BZONES[src_variable_name]:
                            query_bz_kwargs['lookup_bzones'] = place_lookup[
                                place_name]
                            code
                        elif place_lookup[place_name]:
                            self.warning(
                                '{} dataset not zonal: downloading '
                                'for country instead'.format(variable_name))

                        # Query
                        df = pd.DataFrame(query(
                            code, start=start, end=end, **query_bz_kwargs))

                        # Write downloaded data
                        self._write_downloaded(
                            df, variable_name, component_name, place_name,
                            code, **kwargs)
                    except NoMatchingDataError:
                        self.warning(
                            'No mathcing data found for {} {} {}.'
                            ' Saving empty data frame.'.format(
                                place_name, component_name, variable_name))
                        df = pd.DataFrame(columns=[component_name])
                        self._write_downloaded(
                            df, variable_name, component_name, place_name,
                            code, **kwargs)

        # Return names of downloaded variables
        return variable_component_names

    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: :py:class:`xarray.Dataset()`
        """
        # Loop over datasets
        ds = {}
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
                self.info('-- {}:'.format(component_name))

                # Get zone-code mapping and place-lookup mapping
                place_code, place_lookup = self._get_place_code(
                    variable_name, component_name=component_name, **kwargs)

                # Loop over places
                da_comp = None
                for place_name, code in place_code.items():
                    self.info('--- {}'.format(place_name))

                    # Read downloaded data
                    filepath = self._get_download_filepath(
                        variable_name, component_name, place_name, code,
                        **kwargs)
                    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

                    # Convert index timezone to UTC
                    df.index = pd.to_datetime(
                        df.index, utc=True).tz_convert(None)

                    # Convert to DataArray
                    da_zone = xr.DataArray(
                        df, dims=('time', 'component')).expand_dims(
                            'region').assign_coords(region=[place_name])

                    # Italian exception
                    area = (self.med.geo_src.place_area.get(place_name)
                            or place_name)
                    if (area == 'Italy') and (variable_name == 'generation'):
                        # Set inconsistent values to NaN
                        da_zone.values.setflags(write=True)
                        start_na = pd.Timestamp('2016-10-26T00:00')
                        end_na = pd.Timestamp('2016-11-01T00:00')
                        da_zone.loc[{'time': slice(start_na, end_na)}] = np.nan

                    # Concatenate
                    da_comp = (da_zone if da_comp is None else
                               xr.concat([da_comp, da_zone], dim='region'))

                # Concatenate
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            # Add total wind component if needed
            component_name = 'wind'
            if component_name in component_names:
                # Treat NaNs as zero unless in both components
                da_on = da.sel(component='wind-onshore', drop=True)
                da_off = da.sel(component='wind-offshore', drop=True)
                na = da_on.isnull() & da_off.isnull()
                da_wind = (da_on.fillna(0.) + da_off.fillna(0.)).where(
                    ~na, np.nan)
                da_wind = da_wind.expand_dims('component').assign_coords(
                    component=[component_name])
                da = xr.concat([da, da_wind], dim='component')

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def _write_downloaded(self, df, variable_name, component_name,
                          place_name, code, **kwargs):
        """Write downloaded data.

        :param df: Data frame to write.
        :param variable_name: Variable name.
        :param component_name: Component name.
        :param place_name: Zone/country name.
        :param code: Zone/country code.
        :type df: :py:class:`pandas.DataFrame`
        :type variable_name: str
        :type component_name: str
        :type place_name: str
        :type code: str
        """
        # Adjust names
        df.index.name = 'time'
        df.columns = [component_name]

        # Save locally
        filepath = self._get_download_filepath(
            variable_name, component_name, place_name, code,
            **kwargs)
        df.to_csv(filepath, header=True)

    def _get_place_code(self, variable_name, component_name=None, **kwargs):
        """Get zone to zone-code mapping and zone to country-code mapping.

        :param variable_name: Variable name.
        :param component_name: Component name for which to get place names,
          based on the data sources used by component managers with the same
          component name.
          If `None`, all places are considered, independently of the component.
        :type variable_name: str
        :type component_name: str

        :returns: Zone to zone code and zone to lookup flag mappings.
        :rtype: :py:class:`tuple` of

          * mapping of :py:class:`str` to :py:class:`str`
          * mapping of :py:class:`str` to :py:class:`bool`

        .. seealso:: :py:meth:`..geo.get_country_code`.
        """
        # Get place names for source
        src_place_regions, _ = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, component_name=component_name, **kwargs))

        # Get source variable name
        src_variable_name = SRC_VARIABLE_NAMES[variable_name]

        place_code = {}
        place_lookup = {}
        for place_name, region_names in src_place_regions.items():
            # Get place (zone) area (country)
            area = self.med.geo_src.place_area[place_name]

            # Get country code
            place_country_code = get_country_code(area, code='alpha-2')

            if (area == place_name) or (
                    not SRC_VARIABLE_WITH_BZONES[src_variable_name]):
                # Assign country-code to place (country)
                place_code[area] = place_country_code

                # Do not look for building zone for this place
                place_lookup[area] = False
            else:
                # Assign code to place (zone)
                place_code[place_name] = '{}-{}'.format(
                    place_country_code, region_names[0])

                # Look for building zone for this place
                place_lookup[place_name] = True

        return place_code, place_lookup

    def _get_download_filepath(
            self, variable_name, component_name, place_name, code, **kwargs):
        """Get downloaded dataset filepath.

        :param variable_name: Variable name.
        :param component_name: Component name.
        :param place_name: Zone/country name.
        :param code: Zone/country code.
        :type variable_name: str
        :type component_name: str
        :type place_name: str
        :type code: str

        :returns: Filepath
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        src_dir = Path(src_dir, variable_name)
        src_dir.mkdir(parents=True, exist_ok=True)
        filename = '{}_{}_{}_{}{}.csv'.format(
            self.name, variable_name, component_name, code,
            self.get_postfix(**kwargs))
        filepath = Path(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['period_start'], self.cfg['period_end'])

        return postfix
