"""GME API."""
from io import BytesIO
from orderedset import OrderedSet
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
import zipfile
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp
from e4clim.utils import tools


#: Component name.
COMPONENT_NAME: tp.Final[str] = 'demand'

#: Variable name.
VARIABLE_NAME: tp.Final[str] = 'demand'

#: Host.
HOST: tp.Final[str] = 'http://www.gestoremercatienergetici.org/En/MenuBiblioteca/Documenti/'

#: Source sheet name.
SHEET_NAME: tp.Final[str] = 'Vendite-Sales'

#: Units.
UNITS: tp.Final[tp.Dict[str, str]] = {
    'demand': 'MWh'
}


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'gme'

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

        .. note:: The GME data is downloaded from the
          `GME website <http://www.gestoremercatienergetici.org>`_.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(context, name, cfg=cfg, **kwargs)

        # Add configuration for
        # :py:func:`e4clim.container.parse_data_source.ParsingDataSourceBase.finalize_array`
        self.cfg['units'] = UNITS

    def download(self, *args, **kwargs) -> e4tp.VCNStrictType:
        """Download GME data source.

        :param variable_component_names: Names of components to download per
          variable.

        :returns: Names of downloaded components per variable.
        """
        years = tools.get_years_range_from_cfg(self.cfg)

        for year in years:
            # Download file
            url = self._get_url(year, **kwargs)
            self.info('- Year {} from {}'.format(year, url))

            # Request and raise exception if needed
            response = requests.get(url)
            response.raise_for_status()

            # Get zip
            zip_ref = zipfile.ZipFile(BytesIO(response.content))

            # Get filepath with extension
            filepath = self._get_download_filepath(year, **kwargs)
            extension = Path(zip_ref.filelist[0].filename).suffix
            filepath = Path('{}{}'.format(filepath, extension))

            # Unzip single file
            zip_ref.filelist[0].filename = filepath.name
            zip_ref.extract(zip_ref.filelist[0], filepath.parent)
            zip_ref.close()

        # Return names of downloaded variables
        return {VARIABLE_NAME: {COMPONENT_NAME}}

    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: :py:class:`xarray.Dataset()`

        :raises AssertionError: if variable name or component names in
          :py:obj:`variable_component_names` argument are not equal to
          :py:obj:`VARIABLE_NAME` and :py:obj:`COMPONENT_NAME`.
        """
        # Check if demand in variable and component names
        assert set(variable_component_names) == tools.ensure_collection(
            VARIABLE_NAME, OrderedSet), (
                'Variable names different from "{}"'.format(VARIABLE_NAME))

        assert variable_component_names[VARIABLE_NAME] == tools.ensure_collection(
            COMPONENT_NAME, OrderedSet), (
                'Component names different from "{}"'.format(COMPONENT_NAME))

        # Get places and regions
        src_place_regions, _ = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Read demand from file
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        da = None
        for year in years:
            # Read downloaded file
            df = self._read_downloaded_file(year, **kwargs)

            # Set UTC datetime index from 'Europe/Rome' time with DST
            start = pd.to_datetime(
                str(df.iloc[0, 0]) + '{:02d}'.format(df.iloc[0, 1] - 1),
                format='%Y%d%m%H')
            df.index = pd.date_range(
                start=start, freq='H', periods=df.shape[0],
                tz='Europe/Rome').tz_convert(None)

            # Groupby zones, summing energy
            df_zones = pd.DataFrame(
                0., index=df.index, columns=list(src_place_regions))
            for place_name, region_names in src_place_regions.items():
                df_zones[place_name] = df[region_names].sum('columns')

            # Select zones and convert to DataArray
            da_year = xr.DataArray(df_zones, dims=('time', 'region'))

            # Add array to record
            da = (da_year if da is None else
                  xr.concat([da, da_year], dim='time'))

        # Remove the years appearing from conversion to UTC
        first_date = '{}-01-01'.format(years[0])
        last_date = '{}-12-31'.format(years[-1])
        da = da.sel(time=slice(first_date, last_date))
        da['time'].attrs['timezone'] = 'UTC'

        # Add component dimension
        da = da.expand_dims('component').assign_coords(
            component=[COMPONENT_NAME])

        # Add demand to dataset
        ds = {VARIABLE_NAME: da}

        return ds

    def _read_downloaded_file(self, year, **kwargs):
        """Read downloaded file.

        :param year: Year for which to read file.
        :type year: int

        :returns: Data frame read from file.
        :rtype: :py:class:`pandas.DataFrame`
        """
        # Get filepath
        filepath = self._get_download_filepath(year, **kwargs)

        # Read file as xls or xlsx
        self.info('- Year {} from {}'.format(year, filepath))
        try:
            filepath_ext = Path('{}.xls'.format(filepath))
            df = pd.read_excel(filepath_ext, sheet_name=SHEET_NAME)
        except FileNotFoundError:
            filepath_ext = Path('{}.xlsx'.format(filepath))
            df = pd.read_excel(filepath_ext, sheet_name=SHEET_NAME)

        return df

    def _get_url(self, year, **kwargs):
        """Get url.

        :param year: Year.
        :type year: int

        :returns: Filepath.
        :rtype: str
        """
        filename = 'Anno{}.zip'.format(year)
        url = '{}/{}'.format(HOST, filename)

        return url

    def _get_download_filepath(self, year, **kwargs):
        """Get download filepath without extension.

        :param year: Year.
        :type year: int

        :returns: Filepath.
        :rtype: str
        """
        # Define filename
        filename = '{}_{}_{}'.format(
            self.DEFAULT_SRC_NAME, VARIABLE_NAME, year)

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = Path(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get postfix for GSE data source.

        returns: Postfix.
        rtype: str
        """
        postfix = '_{}-{}'.format(self.cfg['first_year'],
                                  self.cfg['last_year'])

        return postfix
