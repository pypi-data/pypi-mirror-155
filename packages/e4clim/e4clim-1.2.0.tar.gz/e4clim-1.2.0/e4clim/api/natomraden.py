"""natomraden.se API for Sweden's bidding zones."""
import geopandas as gpd
from pkg_resources import resource_filename
import typing as tp
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefault, GEO_VARIABLE_NAME)
import e4clim.typing as e4tp


class DataSource(GeoParsingDataSourceDefault):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'natomraden'

    #: Area: `'Sweden'`.
    AREA: tp.Final[str] = 'Sweden'

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

    def download(self, *args, **kwargs) -> tp.Set[str]:
        """Convenience function to warn that natomraden.se data is not downloaded
        but loaded from package data.

        :returns: Names of downloaded variables.

        .. note:: The JSON geometries were downloaded from the `natomraden.se <https://www.natomraden.se/>` source code.
        """
        self.warning(
            '{} is not to be downloaded. It is instead directly loaded from '
            'the package data.'.format(self.DEFAULT_SRC_NAME))

        return {GEO_VARIABLE_NAME}

    def read_file(self, *args, **kwargs) -> gpd.GeoDataFrame:
        """Read geographical data for area from package resources.

        :param area: Geographical area for which to read the data.

        :returns: Geographic data frame.
        """
        # Get resource name
        resource_name = self.get_filename(**kwargs)

        # Read geographical file for area
        gdf = gpd.read_file(resource_filename(__name__, resource_name))

        return gdf

    def get_filename(self, *args, **kwargs) -> str:
        """Get package resource name for data scratched from `"natomraden.se"`.

        :returns: Resource name.
        """
        filename = 'sweden_bidding_zones_geometry.json'
        resource_name = '../data/{}/{}/{}'.format(
            self.AREA, self.DEFAULT_SRC_NAME, filename)

        return resource_name
