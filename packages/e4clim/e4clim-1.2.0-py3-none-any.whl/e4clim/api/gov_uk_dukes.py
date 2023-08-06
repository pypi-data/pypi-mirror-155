"""gov.uk DUKES API for Great Britain."""
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp


class DataSource(ParsingSingleDataSourceBase):
    """gov.uk DUKES data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'gov_uk_dukes'

    #: Area.
    AREA: tp.Final[str] = 'United Kingdom of Great Britain and Northern Ireland'

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

        .. note:: The data is downloaded from the `gov.uk DUKES's Chapter 6 <https://www.gov.uk/government/statistics/renewable-sources-of-energy-chapter-6-digest-of-united-kingdom-energy-statistics-dukes/>`

        :raises AssertionError: if :py:obj:`variable_component_names` argument
          is `None`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        # Loop over variables
        downloaded_files = []
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Loop over components
            for component_name in component_names:
                # Get URL
                url, filepath = self._get_url_filepath(
                    variable_name, component_name, **kwargs)

                # Only download once
                if filepath not in downloaded_files:
                    self.info('-- {} from {} to {}'.format(
                        component_name, url, filepath))

                    # Request and raise exception if needed
                    response = requests.get(url)
                    response.raise_for_status()

                    # Write XLS
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    # Prevent further downloads
                    downloaded_files.append(filepath)

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
        # Get place names for source
        src_place_regions, _ = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        # Loop over variables
        ds = xr.Dataset()
        loaded_files = []
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))

            # Loop over components
            da = None
            for component_name in component_names:
                # Get filepath
                _, filepath = self._get_url_filepath(
                    variable_name, component_name, **kwargs)

                # Only download once
                if filepath not in loaded_files:
                    self.info('-- {} from {}'.format(component_name, filepath))

                    # Read data frame
                    read_excel_kwargs, icols = self._get_read_excel_kwargs(
                        variable_name, component_name, **kwargs)
                    df = pd.read_excel(filepath, **read_excel_kwargs)

                    # Transpose and select columns
                    df = df.transpose().iloc[:, icols]

                    # Define time index
                    df.index = pd.DatetimeIndex(
                        ('{}-12-31'.format(y) for y in df.index), freq='A-DEC')
                    df.index.name = 'time'

                    # Select period
                    df = df.loc[self.cfg['start_date']:self.cfg['end_date']]

                    # Prevent further downloads
                    loaded_files.append(filepath)

                # Select component
                df_comp = df[self.cfg['component_names'][
                    component_name]].astype(float)

                # Convert to data array
                da_comp = xr.DataArray(df_comp, dims=('time',)).expand_dims(
                    'component').assign_coords(component=[component_name])

                # Add component to data array
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            # Add area as region coordinate
            da = da.expand_dims('region').assign_coords(
                region=list(src_place_regions))

            # Add to dataset
            ds[variable_name] = da

        return ds

    def _get_url_filepath(self, variable_name, component_name, **kwargs):
        """Get URL for query and filepath.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :type variable_name: str
        :type component_name: str

        :returns: Tuple containing URL and filepath.
        :rtype: :py:class:`tuple` with two :py:class:`str`
        """
        read_excel_kwargs, _ = self._get_read_excel_kwargs(
            variable_name, component_name, **kwargs)

        # Get URL and filename
        if component_name in ['wind', 'wind-onshore', 'wind-offshore',
                              'marine', 'pv', 'hydro', 'bio']:
            if variable_name == 'capacityfactor':
                filename = '{}_{}.xls'.format(
                    'DUKES', read_excel_kwargs['sheet_name'])
                url = '{}/{}/{}'.format(
                    self.cfg['host'], '822656', filename)

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = Path(src_dir, filename)

        return url, filepath

    def _get_read_excel_kwargs(self, variable_name, component_name, **kwargs):
        """Get keyword arguments for :py:meth:`pandas.read_excel` and columns slice.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :type variable_name: str
        :type component_name: str

        :returns: Tuple with keywoard arguments and column slice.
        :rtype: :py:class:`tuple` with :py:class:`dict` and :py:class:`slice`
        """
        if component_name in ['wind', 'wind-onshore', 'wind-offshore',
                              'marine', 'pv', 'hydro', 'bio']:
            if variable_name == 'capacityfactor':
                kwargs = {'sheet_name': '6.5', 'index_col': 0, 'header': 3,
                          'skipfooter': 7}
                icols = slice(20, None)

        return kwargs, icols

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['start_date'], self.cfg['end_date'])

        return postfix
