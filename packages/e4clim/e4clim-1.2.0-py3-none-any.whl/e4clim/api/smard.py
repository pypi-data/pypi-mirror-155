"""SMARD API for Germany, Luxembourg and Austria."""
from io import BytesIO
import numpy as np
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
import zipfile
from e4clim.container.geo_data_source import GeoParsingSingleDataSourceBase
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.specific.capacityfactor import (
    download_to_compute_capacityfactor, compute_capacityfactor)
import e4clim.typing as e4tp
from e4clim.utils import tools


class DataSource(ParsingSingleDataSourceBase):
    """SMARD data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'smard'

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
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`

        .. note:: The data is downloaded from
          `SMARD.de <>https://www.smard.de/en/downloadcenter/download_market_data/>`.

        :raises AssertionError:

          * if :py:obj:`variable_component_names` argument is `None`.
          * if :py:obj:`self.med.geo_src` is not
            :py:class:`e4clim.container.geo_data_source.GeoParsingSingleDataSourceBase`.
        """
        assert variable_component_names is not None, (
            '"variable_component_names" argument required')

        assert isinstance(self.med.geo_src, GeoParsingSingleDataSourceBase), (
            '"geo_src" attribute of "self.med" should be '
            '"e4clim.container.geo_data_source.GeoParsingSingleDataSourceBase"')

        # Get place names for source
        _, src_region_place = self.med.geo_src.get_place_regions_for_source(
            self.name, **kwargs)

        years = tools.get_years_range_from_cfg(self.cfg)

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
                self.info('-- {}'.format(component_name))

                # Loop over dates
                for y, year in enumerate(years):
                    self.info('--- {}'.format(year))

                    # Loop over regions
                    for region_name in src_region_place:
                        # Get URL
                        url, json = self._get_url_json(
                            variable_name, component_name, year, region_name,
                            **kwargs)
                        filepath = self._get_download_filepath(
                            variable_name, component_name, year, region_name,
                            **kwargs)
                        self.info('---- from {} to {}'.format(url, filepath))

                        # Request and raise exception if needed
                        response = requests.post(url, json=json)
                        response.raise_for_status()

                        # Unzip single file
                        zip_ref = zipfile.ZipFile(BytesIO(response.content))
                        zip_ref.filelist[0].filename = filepath.name
                        zip_ref.extract(zip_ref.filelist[0], filepath.parent)
                        zip_ref.close()

        # Return names of downloaded variables
        return variable_component_names

    @ compute_capacityfactor
    def parse(self, variable_component_names, **kwargs):
        """Parse data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get place names for source
        src_place_regions, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, **kwargs))

        # Get years
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)

        # Loop over variables
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
                self.info('-- {}'.format(component_name))

                df_comp = None
                for y, year in enumerate(years):
                    self.info('--- {}'.format(year))

                    # Loop over regions
                    df_year = pd.DataFrame(columns=src_region_place.values(),
                                           dtype=float)
                    for region_name, place_name in src_region_place.items():
                        # Get filepath
                        filepath = self._get_download_filepath(
                            variable_name, component_name, year, region_name,
                            **kwargs)
                        self.info('---- from {}'.format(filepath))

                        # Read data frame and select series
                        df_region = pd.read_csv(
                            filepath, **self.cfg['read_csv_kwargs'])
                        s = df_region.iloc[:, 0]

                        # Add region data to place
                        if df_year[place_name].any():
                            df_year[place_name] += s
                        else:
                            df_year[place_name] = s

                    # Add year
                    df_comp = (df_year if df_comp is None else
                               pd.concat([df_comp, df_year], 'index'))

                if variable_name == 'generation':
                    # Convert time zone to UTC
                    df_comp.index = df_comp.index.tz_localize(
                        self.cfg['timezone'],
                        ambiguous='infer').tz_convert(None)
                df_comp.index.name = 'time'

                # Convert to data array
                da_comp = xr.DataArray(
                    df_comp, dims=('time', 'region')).expand_dims(
                    'component').assign_coords(component=[component_name])

                # Add component to data array
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            if variable_name == 'generation':
                # Convert 15m-power to 1h-energy
                da = da.resample(time='H').sum('time')

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

            # Select requested components
            da = da.sel(component=list(component_names))

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

        # Upsample capacity to generation using capacities
        # from the 1st of January of next year
        freq = da_gen.indexes['time'].inferred_freq
        da_cap_up = da_cap.copy()
        da_cap_up['time'] = [pd.Timestamp('{}-01-01T00:00'.format(t.year - 1))
                             for t in da_cap_up.indexes['time']]
        da_cap_up = da_cap_up.resample(time=freq).ffill().reindex(
            time=da_gen.indexes['time'], method='ffill')

        # Get number of hours in generation time step
        nhours = 1.

        # Get capacity factor
        da = da_gen / (da_cap_up * nhours)

        return da

    def _get_url_json(self, variable_name, component_name, year, region_name,
                      **kwargs):
        """Get URL and JSON parameters for HTTP POST request.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :param year: Year.
        :param region_name: Region name.
        :type variable_name: str
        :type component_name: str
        :type year: int
        :type region_name: str

        :returns: URL and JSON parameters.
        :rtype: :py:class:`tuple` with a :py:class:`str` and a mapping
        """
        # Define URL
        url = self.cfg['url']

        # Get from and to timestamps (POSIX time in milliseconds)
        timestamp_from = pd.Timestamp('{}-01-01'.format(
            year)).timestamp() * 1000
        timestamp_to = pd.Timestamp('{}-01-01'.format(
            year + 1)).timestamp() * 1000 - 1.

        # Define JSON parameters
        json = {"request_form": [{
            "format": self.cfg['file_format'].upper(),
            "language": self.cfg['language'].lower(),
            "moduleIds": [
                self.cfg['component_ids'][variable_name][component_name]],
            "region": region_name,
            "timestamp_from": timestamp_from, "timestamp_to": timestamp_to,
            "type":"discrete"}]}

        return url, json

    def _get_download_filepath(
            self, variable_name, component_name, year, region_name, **kwargs):
        """Get download filepath.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :param year: Year.
        :param region_name: Region name.
        :type variable_name: str
        :type component_name: str
        :type year: int
        :type region_name: str

        :returns: Filepath.
        :rtype: str

        .. note:: Dates in filepath are in UTC.
        """
        # Define filename
        filename = '{}_{}_{}_{}_{}.csv'.format(
            self.DEFAULT_SRC_NAME, variable_name, component_name, region_name,
            year)

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
