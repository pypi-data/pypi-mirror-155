"""ISTAT API."""
from pathlib import Path
import typing as tp
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefaultDownload)
import e4clim.typing as e4tp


class DataSource(GeoParsingDataSourceDefaultDownload):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'istat'

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

        :returns: URL pointing to geographical data and
          the name of shapefile.
        """
        postfix = '{}{}'.format(str(self.cfg['date']),
                                str(self.cfg['resolution']))
        dir0 = 'Limiti' + postfix
        url = '{}/{}/{}.zip'.format(self.cfg['host'], self.cfg['path'], dir0)

        return url

    def get_filename(self, *args, **kwargs) -> e4tp.PathType:
        """Get downloaded-file name.

        :returns: Filename.
        """
        postfix = '{}{}'.format(str(self.cfg['date']),
                                str(self.cfg['resolution']))
        dir0 = 'Limiti' + postfix
        dir1 = 'Reg' + postfix
        filename = Path(dir0, dir1, dir1 + '.shp')

        return filename
