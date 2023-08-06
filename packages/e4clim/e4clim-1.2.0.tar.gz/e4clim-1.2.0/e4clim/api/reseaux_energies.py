"""Reseaux Energies API."""
from io import BytesIO
import pandas as pd
from pathlib import Path
import requests
import typing as tp
import xarray as xr
from e4clim.container.geo_data_source import GeoParsingSingleDataSourceBase
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp


#: Host.
HOST: tp.Final[str] = 'https://opendata.reseaux-energies.fr/api/records/'

#: Version.
VERSION: tp.Final[str] = '1.0'

#: API.
API: tp.Final[str] = 'download'

#: Variable datasets.
VARIABLE_DATASETS: tp.Final[tp.Dict[str, str]] = {
    'capacityfactor': 'fc-tc-regionaux-mensuels-enr',
    'capacity': 'parc-region-annuel-production-filiere',
    'demand': 'eco2mix-regional-cons-def'
}

#: Variable component names.
VARIABLE_COMPONENT_NAMES: tp.Final[tp.Dict[str, tp.Dict[str, str]]] = {
    'capacityfactor': {
        'wind-onshore': 'fc_moyen_mensuel_eolien',
        'pv': 'fc_moyen_mensuel_solaire'
    },
    'capacity': {
        'wind-onshore': 'parc_eolien_mw',
        'pv': 'parc_solaire_mw'
    },
    'demand': {
        'demand': 'consommation'
    }
}

#: Dataset configurations.
DATASET_CFGS: tp.Final[tp.Dict[str, tp.Dict[str, tp.Union[
    str, tp.Dict[str, str]]]]] = {
    'fc-tc-regionaux-mensuels-enr': {
        'freq_label': 'mois',
        'region_label': 'region',
        'freq': 'M'
    },
    'eco2mix-regional-cons-def': {
        'freq_label': 'date_heure',
        'region_label': 'libelle_region',
        'freq': '30min',
        'resample': {
            'freq': 'H',
            'apply': 'mean'
        }
    },
    'parc-region-annuel-production-filiere': {
        'freq_label': 'annee',
        'region_label': 'region',
        'freq': 'A-DEC'
    }
}

#: Keyword arguments for :py:func:`pandas.read_csv`.
READ_CSV_KWARGS: tp.Final[tp.Dict[str, tp.Any]] = {
    'index_col': 0,
    'parse_dates': True,
}

#: Maximum number of rows.
ROWS_MAX: tp.Final[int] = 10000

#: Unit conversions.
UNIT_CONVERSIONS: tp.Final[tp.Dict[str, float]] = {
    'capacityfactor': 0.01,
    'capacity': 1.,
    'demand': 1.
}

#: Units.
UNITS: tp.Final[tp.Dict[str, str]] = {
    'capacityfactor': '',
    'capacity': 'MW',
    'demand': 'MW'
}


class DataSource(ParsingSingleDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'reseaux_energies'

    #: Area: `'France'`.
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

        # Add configuration for
        # :py:func:`e4clim.container.parse_data_source.ParsingDataSourceBase.finalize_array`
        self.cfg['unit_conversions'] = UNIT_CONVERSIONS
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
          `Reseaux Energies website <https://opendata.reseaux-energies.fr/>`.

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

        # Get region names
        _, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))
            if len(component_names) == 0:
                self.warning('- No component provided: skipping')
                continue

            dates = self._get_dates(variable_name)
            for idate, date in enumerate(dates[:-1]):
                next_date = dates[idate + 1]
                self.info('-- {}'.format(date))

                for region_name in src_region_place:
                    for component_name in component_names:
                        s = self._fetch_series(
                            variable_name, component_name, region_name, date,
                            next_date)

                        filepath = self._get_download_filepath(
                            variable_name, component_name, region_name, date)

                        s.to_csv(filepath, header=True)

        return variable_component_names

    def _fetch_series(self, variable_name, component_name, region_name, date,
                      next_date):
        """Fetch records for variable, region and date.

        :param variable_name: Variable name.
        :param component_name: Component name.
        :param region_name: Region name.
        :param date: Year or date of day.
        :type variable_name: str
        :type component_name: str
        :type region_name: str
        :type date: :py:class:`int` or py:class:`pandas.Datetime`

        :returns: Time series.
        :rtype: :py:class:`pandas.Series`
        """
        url = self._get_url(
            variable_name, component_name, region_name, date, next_date)
        self.info('--- {}'.format(url))

        response = requests.get(url)
        response.raise_for_status()

        s = pd.read_csv(
            BytesIO(response.content), index_col=0, sep=';',
            parse_dates=True).squeeze('columns')
        s = s.sort_index()
        s.index.name = 'time'

        return s

    def _get_dates(self, variable_name):
        """Get dates with an additional one to compute time deltas.

        :param variable_name: Variable name.
        :type variable_name: str

        :returns: Years.
        :rtype: list
        """
        first_year = int(self.cfg['first_year'])
        last_year = int(self.cfg['last_year'] + 1)
        dates = _get_years(first_year, last_year)

        return dates

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
        src_place_regions, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))
        place_names = list(src_place_regions)

        ds = {}
        for variable_name, component_names in variable_component_names.items():
            self.info('- {}:'.format(variable_name))
            if len(component_names) == 0:
                self.warning('- No component provided: skipping')
                continue

            ds_name = VARIABLE_DATASETS[variable_name]
            cfg_ds = DATASET_CFGS[ds_name]

            da = None
            for component_name in component_names:
                self.info('-- {}'.format(component_name))

                da_comp = None
                dates = self._get_dates(variable_name)
                for date in dates[:-1]:
                    self.info('--- {}'.format(date))

                    df_date = pd.DataFrame(columns=place_names, dtype=float)
                    for region_name, place_name in src_region_place.items():
                        s = self._read_region_data(
                            variable_name, component_name, region_name, date)

                        s = _drop_duplicates(s)

                        s = _resample_series(s, cfg_ds)

                        df_date[place_name] = s

                    df_date = _average_if_capacityfactor(
                        df_date, variable_name, src_place_regions)

                    da_comp = _update_component_data(da_comp, df_date)

                da = _update_variable_data(da, da_comp, component_name)

            ds = _update_dataset(ds, da, variable_name, component_names)

        return ds

    def _read_region_data(
            self, variable_name, component_name, region_name, date):
        """Read region data."""
        filepath = self._get_download_filepath(
            variable_name, component_name, region_name, date)
        self.info('---- {}'.format(filepath))

        s = pd.read_csv(filepath, **READ_CSV_KWARGS)

        return s

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['first_year'], self.cfg['last_year'])

        return postfix

    def _get_download_filepath(self, variable_name, component_name,
                               region_name, date):
        """Get URL for region and date.

        :param variable_name: Variable name.
        :param component_name: Component_name.
        :param region_name: Region name.
        :param date: Year or date of day.
        :type variable_name: str
        :type component_name: str
        :type region_name: str
        :type date: :py:class:`int` or py:class:`pandas.Datetime`

        :returns: Filepath.
        :rtype: str
        """
        # Get data-source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get filename
        sdate = _get_date_string(date)
        filename = '{}_{}_{}_{}_{}.csv'.format(
            self.name, variable_name, component_name, region_name, sdate)

        # Return filepath
        return Path(src_dir, filename)

    def _get_url(self, variable_name, component_name, region_name,
                 date, next_date):
        """Get URL for region and date.

        :param variable_name: Variable name.
        :param component_name: Component name.
        :param region_name: Region name.
        :param date: Year or date of day.
        :type variable_name: str
        :type component_name: str
        :type region_name: str
        :type date: :py:class:`int` or py:class:`pandas.Datetime`

        :returns: URL.
        :rtype: str
        """
        ds_name = VARIABLE_DATASETS[variable_name]
        cfg_ds = DATASET_CFGS[ds_name]
        region_label = cfg_ds['region_label']
        freq_label = cfg_ds['freq_label']
        src_component_name = VARIABLE_COMPONENT_NAMES[variable_name][component_name]
        sdate = _get_date_string(date)

        ssort = '&sort=-{}'.format(freq_label)
        sfacet = '&facet={}&facet={}'.format(freq_label, region_label)
        srefine = '&refine.{}={}&refine.{}={}'.format(
            freq_label, sdate, region_label, region_name)
        sfields = '&fields={},{}'.format(freq_label, src_component_name)
        sds = '/?dataset={}'.format(ds_name)

        query = '{}{}{}{}{}'.format(sds, ssort, sfacet, srefine, sfields)

        url = '{}/{}/{}/{}'.format(HOST, VERSION, API, query)

        return url


def _resample_series(s, cfg_ds):
    """Resample series.

    :param s: Series.
    :param cfg_ds: Dataset configuration.
    :type s: :py:class:`pandas.Series`
    :type cfg_ds: mapping

    :returns: Resampled series.
    :rtype: :py:class:`pandas.Series`
    """
    cfg_resample = cfg_ds.get('resample')
    if cfg_resample:
        gp = s.resample(cfg_resample['freq'])
        s = getattr(gp, cfg_resample['apply'])()

    return s


def _average_if_capacityfactor(df_date, variable_name, src_place_regions):
    if variable_name == 'capacityfactor':
        for place_name, region_names in src_place_regions.items():
            df_date[place_name] /= len(region_names)

    return df_date


def _update_component_data(da_comp, df_date):
    # Create data array
    da_date = xr.DataArray(df_date, dims=['time', 'region'])

    # Concatenate dates
    da_comp = (da_date if da_comp is None else
               xr.concat([da_comp, da_date], dim='time'))

    return da_comp


def _update_variable_data(da, da_comp, component_name):
    # Add component dimension
    da_comp = da_comp.expand_dims(
        'component').assign_coords(component=[component_name])

    # Concatenate components
    da = da_comp if da is None else xr.concat(
        [da, da_comp], dim='component')

    return da


def _update_dataset(ds, da, variable_name, component_names):
    da = da.transpose('time', 'component', 'region')
    try:
        da['time'] = da.indexes['time'].tz_convert(None)
    except TypeError:
        pass

    ds[variable_name] = _manage_wind_components(da, component_names)

    return ds


def _manage_wind_components(da, component_names):
    """Replace `'wind'` by `'wind-onshore'` in component coordinate of array.

    :param da: Array.
    :param component_names: Component names.
    :type da: :py:class:`xarray.DataArray`
    :type component_names: collection.

    :returns: Array with proper wind component name.
    :rtype: :py:class:`xarray.DataArray`
    """
    component_name = 'wind'
    if component_name in component_names:
        coord_component = da.indexes['component'].tolist()
        idx = coord_component.index('wind-onshore')
        coord_component[idx] = component_name
        da['component'] = coord_component

    return da


def _get_years(first_year, last_year):
    """Get list of range of years.

    :param first_year: First year.
    :param last_year: Last year (included in list).

    :returns: Years.
    :rtype: list
    """
    dates = [d for d in range(first_year, last_year + 1)]

    return dates


def _round_date(d0):
    """Round date to half hours.

    :param d0: Date.
    :type d0: :py:class:`pandas.Timestamp`

    :returns: Rounded date.
    :rtype: :py:class:`pandas.Timestamp`
    """
    stime0 = str(d0.time())
    stime = '{:02d}:{:02d}:{:02d}'.format(
        d0.hour, int(d0.minute / 30) * 30, d0.second)
    d = pd.Timestamp(str(d0).replace(stime0, stime))

    return d


def _get_date_string(date):
    """Get string for date.

    :param date: Date.
    :type: :py:class:`pandas.Timestamp`

    :returns: Date string.
    :rtype: str
    """
    return str(date)


def _drop_duplicates(s):
    """Drop rows with duplicates from series.

    :param s: Series.
    :type s: :py:class:`pandas.Series`

    :returns: Series without duplicates.
    :rtype: :py:class:`pandas.Series`
    """
    return s[~s.index.duplicated()]
