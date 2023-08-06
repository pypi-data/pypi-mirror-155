"""EEA API."""
import typing as tp
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefaultDownload)
import e4clim.typing as e4tp


class DataSource(GeoParsingDataSourceDefaultDownload):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'eea'

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

    def get_url(self, area: str = None, sub_region: str = None,
                **kwargs) -> str:
        """Get URL of geographical data.

        :param sub_region: Secondary region to select.
          If `None`, the whole region is selected.

        :returns: URL pointing to the geographical data.

        :raises AssertionError: if "area" argument is `None`.
        """
        if sub_region is None:
            assert area is not None, (
                '"area" argument required if "sub_region" not given')
            sub_region = area

        url = '{}/{}/{}{}'.format(
            self.cfg['host'], self.cfg['path'], sub_region.lower(),
            str(self.cfg['postfix']))

        return url

    def get_filename(self, area: str = None, sub_region: str = None,
                     **kwargs) -> e4tp.PathType:
        """Get downloaded-file name.

        :param sub_region: Secondary region to select. If `None`,
          the whole region is selected.

        :returns: Filename.

        :raises AssertionError: if "area" argument is `None`.
        """
        if sub_region is None:
            assert area is not None, (
                '"area" argument required if "sub_region" not given')
            sub_region = area

        return sub_region.lower()[:2] + '_' + str(self.cfg['resolution'])
