import typing as tp
from .container.base import ContainerBase
from .context.context_data_sources import ContextDataSources
from .context.context_geo_data_source import ContextGeoDataSource
from .context.context_component import ContextComponent
from .context.context_optimizer import ContextOptimizerBase
from .typing import CfgType


class Application(ContainerBase):
    """Main application."""
    #: Components context.
    _context_components: tp.MutableMapping[str, ContextComponent]

    #: Data-sources context.
    _context_data_sources: ContextDataSources

    #: Geographic data-source context.
    _context_geo_data_source: ContextGeoDataSource

    #: Optimizer context.
    _context_optimizer: tp.Optional[ContextOptimizerBase]

    def __init__(self, cfg: CfgType):
        """Initialize application.

        :param cfg: Configuration.

        .. seealso:: Application builder:
          :py:class:`e4clim.build.application.BuilderApplication`
        """
        super(Application, self).__init__('application', cfg=cfg)

    @property
    def context_components(self) -> tp.MutableMapping[str, ContextComponent]:
        return self._context_components

    @property
    def context_data_sources(self) -> ContextDataSources:
        return self._context_data_sources

    @property
    def context_geo_data_source(self) -> ContextGeoDataSource:
        return self._context_geo_data_source

    @property
    def context_optimizer(self) -> tp.Optional[ContextOptimizerBase]:
        return self._context_optimizer
