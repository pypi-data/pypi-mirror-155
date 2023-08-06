"""Energimyndigheten API for Sweden."""
import pandas as pd
from pkg_resources import resource_filename
import typing as tp
import xarray as xr
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.specific.capacityfactor import compute_capacityfactor


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'energimyndigheten'

    #: Area: `'Sweden'`
    AREA: tp.Final[str] = 'Sweden'

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

    def download(self, *args, **kwargs) -> tp.MutableSet[str]:
        """Convenience function to warn that Energimyndigheten data is not
        downloaded but loaded from package data.

        :returns: Downloaded variable names.
        :rtype: :py:class:`set` of :py:class:`str`

        .. note:: The data was downloaded from the
          `Energimyndigheten Statistics Database <https://pxexternal.energimyndigheten.se/pxweb/en/Vindkraftsstatistik/>`.
        """
        self.warning(
            '{} is not to be downloaded. It is instead directly loaded from '
            'the package data.'.format(self.DEFAULT_SRC_NAME))

        return {'generation', 'capacity', 'capacityfactor'}

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
        # Get places and regions
        src_place_regions, _ = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)
        src_place_names = list(src_place_regions)

        ds = {}
        ddf_allvar = {}
        for variable_name, component_names in variable_component_names.items():
            # Get column for variable
            col = self.cfg['variable_names'][variable_name]

            # Manage wind component as onshore only
            component_name = 'wind'
            component_to_load_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name)

            da = None
            for component_name in component_to_load_names:
                # Try to get previously-read component data
                df_allvar_comp = ddf_allvar.get(component_name)

                if df_allvar_comp is None:
                    # Read data
                    resource_name = self.get_download_resource_name(
                        component_name, **kwargs)
                    df_allvar_comp = pd.read_csv(
                        resource_filename(__name__, resource_name),
                        **self.cfg['read_csv_kwargs'])

                    # Save data
                    ddf_allvar[component_name] = df_allvar_comp

                # Select variable
                df_comp = df_allvar_comp[col].unstack()

                # Get time index with an additional year to count days in years
                # starting the first day of the year to count days
                idx = df_comp.index
                time = pd.DatetimeIndex((
                    '{}-01-01'.format(str(y)) for y in (
                        list(idx) + [int(idx[-1]) + 1])))

                # Aggregate in zones
                df_comp = self._aggregate_in_zones(
                    df_comp, time[:-1], src_place_names, src_place_regions,
                    **kwargs)

                # Replace time to 'A-DEC'
                df_comp.index = pd.date_range(
                    start=df_comp.index[0], end=df_comp.index[-1] +
                    pd.Timedelta('366 days'), freq='A-DEC')

                # Convert to data array
                da_comp = xr.DataArray(
                    df_comp, dims=['time', 'region'],
                    name=variable_name).expand_dims('component').assign_coords(
                        component=[component_name])

                # Add total wind component as onshore wind if needed
                component_name_add = 'wind'
                if component_name_add in component_names:
                    coord_component = da_comp.indexes['component'].tolist()
                    idx = coord_component.index('wind-onshore')
                    coord_component[idx] = component_name_add
                    da_comp['component'] = coord_component

                # Add component to variable in dataset
                da = (da_comp if da is None else
                      xr.concat([ds[variable_name], da_comp], dim='component'))

            ds[variable_name] = da

        return ds

    def get_download_resource_name(self, component_name, **kwargs):
        """Get package resource name for data.

        :returns: Resource name.
        :rtype: str
        """
        filename = '{}_production_{}{}.csv'.format(
            component_name, self.cfg['level'], self.get_postfix(**kwargs))
        resource_name = '../data/{}/{}/{}'.format(
            self.AREA, self.DEFAULT_SRC_NAME, filename)

        return resource_name

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
        end = pd.Timestamp(time[-1]) + pd.Timedelta('366 days')
        time_plus = pd.date_range(start=start, end=end, freq='Y')
        ndays = (time_plus[1:] - time_plus[:-1]).days
        da_ndays = xr.DataArray(ndays, coords=[('time', time)])
        da_nhours = da_ndays * 24

        # Get capacity factor
        da = da_gen / (ds['capacity'] * da_nhours)

        return da

    def _aggregate_in_zones(
            self, df, time, src_place_names, src_place_regions, **kwargs):
        """Aggregate data in zones.

        :param df: Data frame for variable and component.
        :param time: Time index.
        :param src_place_names: Zone/region names
        :param src_place_regions: Zone/region to regions mapping.
        :type df: :py:class:`pandas.DataFrame`
        :type time: :py:class:`pandas.DatetimeIndex`
        :type src_place_names: collection
        :type src_place_regions: mapping from :py:class:`str` to collection

        :returns: Dataset containing aggregated variables.
        :rtype: mapping from :py:class:`str` to :py:class:`pandas.DataFrame`
        """
        # Assign time index
        df.index = time

        # Aggregate into zones
        df_zones = pd.DataFrame(
            0., index=df.index, columns=src_place_names)
        for place_name, region_names in src_place_regions.items():
            df_zones[place_name] = df[region_names].sum('columns')

        return df_zones

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['first_year'], self.cfg['last_year'])

        return postfix
