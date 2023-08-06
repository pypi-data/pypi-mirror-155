"""RTE ECO2MIX API."""
from io import BytesIO
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
import zipfile
from e4clim.container.geo_data_source import GeoParsingSingleDataSourceBase
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp
from e4clim.utils import tools


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'eco2mix'

    #: Area.
    AREA: tp.Final[str] = 'France'

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

    def download(self, *args, **kwargs) -> e4tp.VCNStrictType:
        """Download data.

        :returns: Names of downloaded components per variable.

        .. note:: The data is downloaded from the
          `eco2mix website <https://eco2mix.rte-france.com/download/eco2mix/>`.

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

        # Get data-source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        years = tools.get_years_range_from_cfg(self.cfg)

        for year in years:
            self.info('Downloading files for {}'.format(year))
            for region_name in src_region_place:
                url = self._get_url(region_name, year, **kwargs)
                self.info('  {}'.format(url))

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                # Unzip
                zip_ref = zipfile.ZipFile(BytesIO(response.content))
                zip_ref.extractall(src_dir)
                zip_ref.close()

        return {'generation': {'wind-onshore', 'pv'},
                'capacity': {'wind-onshore', 'pv'},
                'capacityfactor': {'wind-onshore', 'pv'}}

    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: :py:class:`xarray.Dataset()`
        """
        # Manage wind component as onshore only
        component_name = 'wind'
        component_names = variable_component_names[
            list(variable_component_names)[0]]
        component_to_load_names = component_names.copy()
        if component_name in component_names:
            # Make sure that generation and capacity are loaded
            component_to_load_names.add('wind-onshore')

            # Remove capacity factor from components to load
            component_to_load_names.discard(component_name)

        # Get region-place mapping
        _, src_region_place = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Get data-source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get years
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        da = None
        for year in years:
            self.info('Reading files for {}'.format(year))
            start_date = '{}-01-01 00:00'.format(year)
            end_date = '{}-12-31 23:45'.format(year)
            da_year = None
            for region_name, place_name in src_region_place.items():
                # Read CSV file
                filename = self._get_download_filename(
                    year, region_name, self.cfg['source_file_format'])
                filepath = Path(src_dir, filename)
                self.info('  {}'.format(filepath))

                df = pd.read_csv(filepath, **self.cfg['read_csv_kwargs'])

                # Add datetime index
                df.index = pd.date_range(
                    start=start_date, end=end_date,
                    freq=self.cfg['frequency'])
                # df.index = pd.to_datetime(list(
                #     '{}\t{}'.format(d, h)
                #     for d, h in df[['Date', 'Heures']].values))
                df.index.name = 'time'

                # Drop columns
                for col in self.cfg['drop_columns']:
                    del df[col]

                # Rename components and select them
                component_names_inv = {
                    self.cfg['component_names'][component_name]:
                    component_name
                    for component_name in component_to_load_names}
                df = df.rename(columns=component_names_inv)[
                    component_to_load_names]

                # Convert 'ND' and '-' values to None
                is_null = (df == 'ND') | (df == '-')
                if is_null.any().any():
                    df[is_null] = None

                # Convert to float
                df = df.astype(float)

                # Get array with places as coordinates to groupby
                da_reg = xr.DataArray(df, dims=['time', 'component'])
                da_reg = da_reg.expand_dims(
                    'region').assign_coords(region=[place_name])

                # Concatenate regions
                da_year = da_reg if da_year is None else xr.concat(
                    [da_year, da_reg], dim='region')

            # Group by places summing energies
            da_year = da_year.groupby('region').sum('region')

            # Concatenate years
            da = da_year if da is None else xr.concat(
                [da, da_year], dim='time')

        # Sub-sample to hourly
        da = da.resample(time='H').sum('time')

        # Add total wind component as onshore wind if needed
        component_name = 'wind'
        if component_name in component_names:
            coord_component = da.indexes['component'].tolist()
            idx = coord_component.index('wind-onshore')
            coord_component[idx] = component_name
            da['component'] = coord_component

        # Create dataset of variables
        ds = xr.Dataset()
        variable_name = 'demand'
        if variable_name in variable_component_names:
            # Add demand variables with demand component only
            ds[variable_name] = da.sel(component='demand')
        variable_name = 'generation'
        if variable_name in variable_component_names:
            # Add generation variable with generation components only
            gen_comp = list(da.indexes['component'])
            try:
                gen_comp.pop(gen_comp.index('demand'))
            except ValueError:
                pass
            ds[variable_name] = da.sel(component=gen_comp)

        return ds

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['first_year'], self.cfg['last_year'])

        return postfix

    def _get_url(self, region_name, year, **kwargs):
        """Get URL for region and year.

        :param region_name: Region name.
        :param year: Year.
        :type region_name: str
        :type year: int

        :returns: URL.
        :rtype: str
        """
        filename = self._get_download_filename(year, region_name, 'zip')
        url = '{}/{}'.format(self.cfg['host'], filename)

        return url

    def _get_download_filename(self, year, region_name, file_format, **kwargs):
        """Get name of file to download/downloaded.

        :param year: Year.
        :param region_name: French administrative region.
        :param file_format: File format.
        :type year: str
        :type region_name: str
        :type file_format: str

        :returns: Filename.
        :rtype: str
        """
        region_file = self.cfg['region_files'][region_name]
        filename = 'eCO2mix_RTE_{}_Annuel-Definitif_{}.{}'.format(
            region_file, year, file_format)

        return filename
