"""GISCO API for European borders."""
import requests
import typing as tp
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefaultDownload)
import e4clim.typing as e4tp
from e4clim.utils import tools


#: Host.
HOST: tp.Final[str] = 'https://ec.europa.eu/'

#: Path.
PATH: tp.Final[str] = '/eurostat/cache/GISCO/distribution/v2/nuts/'


#: Default maximum fetch-trials.
DEFAULT_MAX_FETCH_TRIALS: tp.Final[int] = 50


class DataSource(GeoParsingDataSourceDefaultDownload):
    """GISCO data source."""
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'gisco'

    #: Flag preventing several downloads per area.
    ONE_DOWNLOAD_PER_AREA: bool = True

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize geographic data source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

    def get_url(self, *args, **kwargs) -> str:
        """ Get URL of geographical data.

        :returns: URL pointing to the geographical data.
        :rtype: str
        """
        # Get the list of files
        path = '{}/{}/'.format(HOST, PATH)
        url_files = path + 'nuts-{}-files.json'.format(self.cfg['year'])
        n_trials = 0
        max_fetch_trials = tools.get_required_int_entry(
            self.cfg, 'max_fetch_trials', DEFAULT_MAX_FETCH_TRIALS)
        while n_trials < max_fetch_trials:
            try:
                # Request and raise exception if needed
                response = requests.get(url_files)
                response.raise_for_status()
                break
            except requests.exceptions.SSLError as e:
                # Retry
                self.warning(
                    '{} trial to fetch {} file list failed: {}'.format(
                        n_trials + 1, self.name, str(e)))
                n_trials += 1
                continue
        # Verify that last trial succeeded
        if n_trials >= max_fetch_trials:
            # All trials failed
            self.critical('Fetching failed after {:d} trials'.format(n_trials))
            raise RuntimeError

        # Get the filename
        filename = self.get_filename(**kwargs)

        # Get URL
        url = '{}{}'.format(path, response.json()['geojson'][filename])

        return url

    def get_filename(self, *args, **kwargs) -> e4tp.PathType:
        """Get downloaded-file name.

        :returns: Filename.
        :rtype: str
        """
        fmt = (self.cfg['spatial_type'], self.cfg['scale'],
               self.cfg['year'], self.cfg['projection'],
               self.cfg['nuts_level'])

        return 'NUTS_{}_{}_{}_{}_LEVL_{}.geojson'.format(*fmt)
