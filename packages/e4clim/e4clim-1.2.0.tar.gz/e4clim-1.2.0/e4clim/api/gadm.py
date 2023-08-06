"""Database of Global Administrative Areas (GADM) API."""
import typing as tp
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefaultDownload, get_country_code)
import e4clim.typing as e4tp
from e4clim.utils import tools


class DataSource(GeoParsingDataSourceDefaultDownload):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'gadm'

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

        #: Child column.
        ccp = tools.get_required_str_entry(self.cfg, 'child_column_prefix')
        level = tools.get_required_str_entry(self.cfg, 'level')
        self.cfg['child_column'] = '{}_{}'.format(ccp, level)

    def get_url(self, area: str = None, **kwargs) -> str:
        """Get URL of geographical data for given area.

        :param area: Area for which to get data.

        :returns: URL pointing to geographical data.

        :raises AssertionError: if "area" argument is `None`.
        """
        assert area is not None, '"area" argument required'

        country_code = get_country_code(area, code='alpha-3')

        # Get URL
        path = '{}/{}/{}{}/{}/'.format(
            self.cfg['host'], self.cfg['path'], self.name.lower(),
            self.cfg['version'], self.cfg['format'])
        sver = str(self.cfg['version']).replace('.', '')
        prefix = '{}{}_{}'.format(self.name.lower(), sver, country_code)
        url = '{}{}_{}.zip'.format(path, prefix, self.cfg['format'])

        return url

    def get_filename(self, area: str = None, **kwargs) -> e4tp.PathType:
        """Get downloaded-file name for given area.

        :param area: Area for which to get data.

        :returns: Filename.

        :raises AssertionError: if "area" argument is `None`.
        """
        assert area is not None, '"area" argument required'

        country_code = get_country_code(area, code='alpha-3')

        # Get filename
        sver = str(self.cfg['version']).replace('.', '')
        prefix = '{}{}_{}'.format(self.name.lower(), sver, country_code)
        filename = '{}_{}.shp'.format(prefix, str(self.cfg['level']))

        return filename
