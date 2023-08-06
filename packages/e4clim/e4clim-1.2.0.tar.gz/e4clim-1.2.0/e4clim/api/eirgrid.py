"""Eirgrid API for Ireland."""
import numpy as np
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.specific.capacityfactor import (
    download_to_compute_capacityfactor, compute_capacityfactor)
import e4clim.typing as e4tp


class DataSource(ParsingSingleDataSourceBase):
    """Eirgrid data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'eirgrid'

    #: Area.
    AREA: tp.Final[str] = 'Ireland'

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
          `Eirgrid <http://www.eirgridgroup.com/how-the-grid-works/renewables/>`.
        """
        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Manage wind component as onshore only
            component_name = 'wind'
            component_to_download_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_download_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_download_names.discard(component_name)

            # Loop over year groups
            dates = self._get_dates(variable_name, **kwargs)
            for date in dates:
                if (not self.cfg.get('no_verbose')) and (date is not None):
                    self.info('-- {}'.format(date))

                # Loop over components
                for component_name in component_to_download_names:
                    # Get URL
                    url, filepath = self._get_url_filepath(
                        variable_name, component_name, date, **kwargs)
                    self.info('--- {} from {} to {}'.format(
                        component_name, url, filepath))

                    # Request and raise exception if needed
                    response = requests.get(url)
                    response.raise_for_status()

                    # Write XLSX
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

        # Return names of downloaded variables
        return variable_component_names

    @compute_capacityfactor
    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get place names for source
        src_place_regions, _ = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))
        place_names = list(src_place_regions)

        # Loop over variables
        ds = {}
        start = pd.Timestamp('{}-01-01'.format(self.cfg['first_year']))
        end = pd.Timestamp('{}-01-01'.format(self.cfg['last_year'] + 1))
        time_slice = slice(start, end)
        for variable_name, component_names in variable_component_names.items():
            cfg_var = self.cfg[variable_name]
            self.info('- {}:'.format(variable_name))

            # Manage wind component as onshore only
            component_name = 'wind'
            component_to_load_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name)

            # Loop over year groups
            dates = self._get_dates(variable_name, **kwargs)
            da = None
            for date in dates:
                if (not self.cfg.get('no_verbose')) and (date is not None):
                    self.info('-- {}'.format(date.year))

                # Loop over components
                da_date = None
                for component_name in component_to_load_names:
                    # Get filepath
                    _, filepath = self._get_url_filepath(
                        variable_name, component_name, date, **kwargs)
                    self.info('-- {} from {}'.format(component_name, filepath))

                    # Read data frame
                    df_comp = pd.read_excel(
                        filepath, **cfg_var['read_excel_kwargs'])

                    if variable_name == 'generation':
                        # Convert time zone to UTC
                        df_comp.index = df_comp.index.tz_localize(
                            self.cfg['timezone'], ambiguous=df_comp[
                                'GMT Offset'].astype(bool)).tz_convert(None)
                    df_comp.index.name = 'time'

                    # Select variable
                    df_comp = df_comp[cfg_var['variable_names']
                                      [component_name]]

                    # Convert to data array
                    da_comp = xr.DataArray(
                        df_comp, dims=('time',)).expand_dims(
                        'component').assign_coords(component=[component_name])

                    # Add component to data array
                    da_date = (da_comp if da_date is None else
                               xr.concat([da_date, da_comp], dim='component'))

                # Add component to data array
                da = (da_date if da is None else
                      xr.concat([da, da_date], dim='time'))

            # Select period
            da = da.sel(time=time_slice)

            if variable_name == 'generation':
                # Convert 15m-power to 1h-energy
                da = da.resample(time='H').mean('time')

            # Add area as region coordinate
            da = da.expand_dims('region').assign_coords(
                region=place_names)

            # Add total wind component as onshore wind if needed
            component_name = 'wind'
            if component_name in component_names:
                coord_component = da.indexes['component'].tolist()
                idx = coord_component.index('wind-onshore')
                coord_component[idx] = component_name
                da['component'] = coord_component

            # Add to dataset
            ds[variable_name] = da

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

        # Upsample capacity to generation
        freq = da_gen.indexes['time'].inferred_freq
        da_cap_up = da_cap.resample(time=freq).ffill().reindex(
            time=da_gen.indexes['time'], method='ffill')

        # Get number of hours in generation time step
        nhours = 1.

        # Get capacity factor
        da = da_gen / (da_cap_up * nhours)

        return da

    def _get_dates(self, variable_name, **kwargs):
        """ Get dates from which to get year groups over which to loop.

        :param variable_name: variable_name.
        :type variable_name: str

        :returns: Dates.
        :rtype: :py:class:`pandas.DatetimeIndex`
        """
        if 'year_groups' in self.cfg[variable_name]:
            start_year = self._get_year_group(
                variable_name, self.cfg['first_year'])[0]
            start = pd.Timestamp('{}-12-31'.format(start_year))
            end_year = self._get_year_group(
                variable_name, self.cfg['last_year'])[-1]
            end = pd.Timestamp('{}-12-31'.format(end_year))
            dates = pd.date_range(
                start=start, end=end, freq='2A-DEC')
        else:
            dates = [None]

        return dates

    def _get_year_group(self, variable_name, year, **kwargs):
        """Get year group to which :py:obj:`year` belong.

        :param variable_name: Variable name.
        :param year: Year.
        :type variable_name: str
        :type year: int

        :returns: Year group.
        :rtype: list
        """
        year_groups = self.cfg[variable_name]['year_groups']
        year_group = np.array(year_groups)[
            [year in yg for yg in year_groups]][0]

        return year_group

    def _get_url_filepath(self, variable_name, component_name, date=None,
                          **kwargs):
        """Get URL for query and filepath.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :param date: Date from which to get year.
          Required for 'generation' variable.
        :type variable_name: str
        :type component_name: str
        :type date: :py:class:`pandas.Timestamp`

        :returns: Tuple containing URL and filepath.
        :rtype: :py:class:`tuple` with two :py:class:`str`
        """
        # Define URL and filename
        if component_name in ['wind', 'wind-onshore', 'wind-offshore']:
            cfg_var = self.cfg[variable_name]
            if variable_name == 'capacity':
                # Define filename for capacity
                filename = '{}.{}'.format(
                    cfg_var['filename'], cfg_var['file_format'])
            elif variable_name == 'generation':
                # Define filename for generation
                year_group = self._get_year_group(
                    variable_name, date.year, **kwargs)
                filename = '{}-{}-{}.{}'.format(
                    cfg_var['filename'], *year_group, cfg_var['file_format'])

            # URL
            url = '{}/{}'.format(self.cfg['host'], filename)

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = Path(src_dir, filename)

        return url, filepath

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(self.cfg['first_year'],
                                  self.cfg['last_year'])

        return postfix
