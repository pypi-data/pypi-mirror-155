from orderedset import OrderedSet
import typing as tp
from e4clim.application import Application
from e4clim.context.context_component import ContextComponent
from e4clim.context.context_data_sources import ContextDataSources
from e4clim.context.context_geo_data_source import ContextGeoDataSource
from e4clim.context.context_optimizer import ContextOptimizerBase
from e4clim.context.mediator import Mediator
import e4clim.typing as e4tp
from e4clim.utils import tools
from .context_component import DirectorContextComponent
from .context_optimizer import DirectorContextOptimizer
from .base import BuilderBase, DirectorBase
from .logger import BuilderLoggerMixin


class BuilderApplication(BuilderBase, BuilderLoggerMixin):
    """Application builder."""

    _product: Application
    _director: 'DirectorApplication'

    def __init__(self, **kwargs) -> None:
        super(BuilderApplication, self).__init__(Application)

    @property
    def product(self) -> Application:
        return self._product

    @property
    def director(self) -> 'DirectorApplication':
        return self._director

    def build_mediator(self) -> None:
        """Build mediator."""
        self.product._med = Mediator(self.cfg, self.product)
        self.build_logger()

        # Share application children with mediator
        self.product._med._children = self.product._children

    def build_context_components(self) -> None:
        """Build component contexts for all areas.

        :raises AssertionError: if "cfg" attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute required'

        cfg_area_contexts = tools.get_required_mapping_entry(
            self.cfg, 'context_components_per_area')

        self.product._context_components = {}

        # Add component contexts for all areas
        for area in cfg_area_contexts:
            cfg_contexts = tools.get_mapping_entry(cfg_area_contexts, area)
            if cfg_contexts is not None:
                self.build_context_components_for_area(area, cfg_contexts)

    def build_context_components_for_area(
            self, area: str, cfg_contexts: tp.Mapping[str, tp.Any]) -> None:
        """Build component contexts for a given area.

        :param area: Area.
        :cfg_contexts: Context configurations.

        :raises AssertionError: if :py:obj:`cfg_contexts` argument
          is not a mapping.
        """
        scmp = ', '.join(cfg_contexts.keys())
        msg = ('Injecting {} component contexts for {} to '
               'application'.format(scmp, area))
        self.product.info(msg)

        # Loop over component context-configuration pairs
        for name in cfg_contexts:
            result_mng_names = tools.get_required_iterable_str_entry(
                cfg_contexts, name, OrderedSet)
            context_component = self._request_context_component(
                None, self.product, name, result_mng_names, area=area)
            self._set_context_component(name, context_component)

    def build_geography(self) -> None:
        """Build geographic context and its data source(s).

        .. note:: Only data sources associated to areas present in
          the 'context_components_per_area' entry of the mediator configuration
          are added.
        """
        # Build context
        cfg_geo = self.product.med.parse_configuration('geo')
        context = ContextGeoDataSource(self.product, cfg=cfg_geo)
        self.product._context_geo_data_source = context
        context.build()

    def build_context_data_sources(self) -> None:
        """Build context data sources."""
        self.product._context_data_sources = ContextDataSources(
            self.product, cfg=self.cfg)

    def build_optimizer(self) -> None:
        """Build optimizer context and its strategy."""
        if ((self.cfg is not None) and ('optimizer' in self.cfg)):
            # Build context
            name = str(self.cfg['optimizer'])
            cfg_opt = self.product.med.parse_configuration(name)

            context_optimizer = self.director.make_context_optimizer(
                cfg=cfg_opt, parent=self.product, name=name)

            self.product._context_optimizer = context_optimizer

            self.product.info('{} injected to application'.format(name))
        else:
            self.product._context_optimizer = None

    def _request_context_component(self, *args, **kwargs) -> ContextComponent:
        """Request component context."""
        context_component = self.director.make_context_component(
            *args, **kwargs)

        return context_component

    def _set_context_component(
            self, name: str, context_component: ContextComponent) -> None:
        """Set component context."""
        self.product._context_components[name] = context_component


class DirectorApplication(DirectorBase):
    """Application director."""

    _builder: BuilderApplication

    #: Warm-start flag.
    _warm_start: bool

    #: Component-context director.
    _deputy_context_component: DirectorContextComponent

    #: Optimizer-context director.
    _deputy_context_optimizer: DirectorContextOptimizer

    def __init__(
            self, builder: BuilderApplication,
            deputy_context_component: DirectorContextComponent,
            deputy_context_optimizer: DirectorContextOptimizer) -> None:
        """Initialize application director.

        :param builder: Application builder.
        :param deputy_context_component: Deputy component-context director.
        :param deputy_context_optimizer: Deputy optimizer-context director.
        """
        super(DirectorApplication, self).__init__(builder)

        self._warm_start = False

        #: Component-context director.
        self._deputy_context_component = deputy_context_component

        #: Optimizer-context director.
        self._deputy_context_optimizer = deputy_context_optimizer

    @property
    def builder(self) -> BuilderApplication:
        return self._builder

    @builder.setter
    def builder(self, builder: BuilderApplication) -> None:
        self._builder = builder

    @property
    def warm_start(self) -> bool:
        return self._warm_start

    @property
    def deputy_context_component(self):
        return self._deputy_context_component

    @property
    def deputy_context_optimizer(self):
        return self._deputy_context_optimizer

    def make(self, cfg_filepath: e4tp.PathType = None, **kwargs) -> Mediator:
        """Make application and return the mediator to communicate with it.

        :param cfg_filepath: Configuration filepath.

        :returns: Application mediator.

        :raises AssertionError: if configuration read from path given by
          :py:obj:`cfg_filepath` argument is `None`.
        """
        assert cfg_filepath is not None, '"cfg_filepath" argument required'
        self.builder.configure(cfg_filepath)
        cfg = self.builder.cfg

        assert cfg is not None, (
            'Configuration read from "{}" required'.format(cfg_filepath))

        self.builder.reset(cfg)

        self.builder.build_mediator()

        self.builder.product.info(
            '*** BUILDING APPLICATION FOR {} ***'.format(
                str(cfg['project_name'])))

        self.builder.build_context_data_sources()

        self.builder.build_geography()

        if not self.warm_start:
            self.builder.build_logger()

        if 'context_components_per_area' in cfg:
            self.builder.build_context_components()

        self.builder.build_optimizer()

        self._warm_start = False

        self.builder.product.info('*** APPLICATION BUILT ***')

        return self.builder.product.med

    def make_context_component(self, *args, **kwargs) -> ContextComponent:
        """Make component context.

        :returns: Component context.
        """
        context_component = self.deputy_context_component.make(*args, **kwargs)

        return context_component

    def make_context_optimizer(
            self, *args, **kwargs) -> ContextOptimizerBase:
        """Make optimizer context.

        :returns: Optimizer context.
        """
        context_optimizer = self.deputy_context_optimizer.make(*args, **kwargs)

        return context_optimizer
