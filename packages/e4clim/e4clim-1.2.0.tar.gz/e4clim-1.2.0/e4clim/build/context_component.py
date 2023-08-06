from orderedset import OrderedSet
from e4clim.application import Application
from e4clim.context.context_component import ContextComponent
from e4clim.context.context_result import ContextResult
from e4clim.typing import CfgType, StrIterableType
from e4clim.utils import tools
from .base import BuilderBase, DirectorBase
from .context_result import DirectorContextResult


class BuilderContextComponent(BuilderBase):
    """Component context builder."""

    _product: ContextComponent
    _director: 'DirectorContextComponent'

    def __init__(self, **kwargs) -> None:
        super(BuilderContextComponent, self).__init__(ContextComponent)

    @property
    def product(self) -> ContextComponent:
        return self._product

    @property
    def director(self) -> 'DirectorContextComponent':
        return self._director

    def build_places_in_area(self, area: str) -> None:
        """Build places in area.

        :param area: Area.
        """
        self.product._area = area

        geo_src = self.product.med.geo_src
        if area and (geo_src is not None):
            if area in geo_src.area_places_sources:
                self.product._place_names = list(
                    geo_src.area_places_sources[area])

    def build_context_results(
            self, context_result_names: StrIterableType) -> None:
        """Build result contexts.

        :context_result_names: Result-contexts names.

        :raises AssertionError: if "cfg" attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute required'

        for name in tools.ensure_collection(context_result_names, OrderedSet):
            cfg = self.cfg.get(name)
            context_result = self._request_context_result(
                cfg, self.product, name)
            self._set_context_result(name, context_result)

        # Add data sources required by component context (from all of its
        # result contexts)
        for context_result in self.product.context_results.values():
            self.product.data_sources.update(context_result.data_sources)

    def _request_context_result(self, *args, **kwargs) -> ContextResult:
        """Request result context."""
        context_result = self.director.make_context_result(*args, **kwargs)

        return context_result

    def _set_context_result(
            self, name: str, context_result: ContextResult) -> None:
        """Set result context.

        :param name: Result-context name.
        :context_result: Result context.
        """
        setattr(self.product, name, context_result)
        self.product.context_results[name] = context_result


class DirectorContextComponent(DirectorBase):
    """Component context director."""

    _builder: BuilderContextComponent

    def __init__(self, builder, deputy_context_result):
        super(DirectorContextComponent, self).__init__(builder)
        self._deputy_context_result = deputy_context_result

    @property
    def builder(self) -> BuilderContextComponent:
        return self._builder

    @builder.setter
    def builder(self, builder: BuilderContextComponent) -> None:
        self._builder = builder

    @ property
    def deputy_context_result(self) -> DirectorContextResult:
        return self._deputy_context_result

    def make(self, cfg: CfgType = None, parent: Application = None,
             name: str = None,
             context_result_names: StrIterableType = None, area: str = None,
             **kwargs) -> ContextComponent:
        """Make component context.

        :param cfg: Component-context configuration.
        :param parent: Parent application.
        :param name: Component-context name.
        :param context_result_names: Result-context names.
        :param area: Area to which the component context is assigned.

        :returns: Component context.

        :raises AssertionError: if

            * "area" argument is `None`,
            * "context_result_names" argument is `None`.

        """
        assert area is not None, '"area" argument required'
        assert context_result_names is not None, (
            '"context_result_names" argument required')

        self.builder.configure(cfg, parent=parent, name=name)

        self.builder.reset(parent, name, self.builder.cfg, **kwargs)

        self.builder.build_places_in_area(area)

        self.builder.build_context_results(context_result_names)

        return self.builder.product

    def make_context_result(self, *args, **kwargs) -> ContextResult:
        """Make result context.

        :returns: Result context.
        """
        context_result = self.deputy_context_result.make(*args, **kwargs)

        return context_result
