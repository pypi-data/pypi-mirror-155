"""Component and result managers base definitions."""
from collections import MutableMapping, OrderedDict
import typing as tp
import e4clim
from .base import ContextBase
import e4clim.typing as e4tp
from .context_result import ContextResult

ContextResultsType = tp.MutableMapping[str, ContextResult]


class ContextComponent(ContextBase, MutableMapping):
    """Component manager."""

    #: Covered area.
    _area: str

    #: Component name (to use in data structures).
    _component_name: str

    #: Result managers of component manager.
    context_results: ContextResultsType

    #: Component-context data sources.
    #: (union of data sources from all result contexts).
    data_sources: e4tp.DataSourcesType

    # Precise types of of sub-class attributes
    _parent: 'e4clim.application.Application'

    #: Places in area.
    _place_names: e4tp.PlaceNamesType

    def __init__(self, parent: 'e4clim.application.Application',
                 name: str, cfg: e4tp.CfgType, **kwargs):
        """
        :param parent: Application.
        :param name: Name.
        :param cfg: Configuration.

        .. seealso:: Component manager builder:
          :py:class:`e4clim.build.context_component.BuilderContextComponent`
        """
        super(ContextComponent, self).__init__(name, cfg=cfg, parent=parent,
                                               **kwargs)

        component_name = self.cfg.get('component_name')
        if component_name is None:
            self._component_name = self.name
        else:
            self._component_name = str(component_name)

        self.context_results = OrderedDict()
        self.data_sources = OrderedDict()

    @property
    def area(self) -> str:
        return self._area

    @property
    def component_name(self) -> str:
        return self._component_name

    @property
    def parent(self) -> 'e4clim.application.Application':
        return self._parent

    @property
    def place_names(self) -> e4tp.PlaceNamesType:
        return self._place_names

    def __getitem__(self, context_result_name: str) -> ContextResult:
        """Get result manager from :py:attr:`context_results`.

        :param context_result_name: Result-manager name.

        :returns: Result manager.
        """
        return self.context_results[context_result_name]

    def get(self, context_result_name: str, default=None) -> tp.Optional[
            ContextResult]:
        """Get result manager from :py:attr`data`.

        :param context_result_name: Result-manager name.
        :param default: Default value.

        :returns: Result manager.
        """
        return self.context_results.get(context_result_name, default)

    def __setitem__(self, context_result_name: str,
                    context_result: ContextResult) -> None:
        """Set result manager in :py:attr:`data`.

        :param context_result_name: Result-manager name.
        :param context_result: Result manager to set.
        """
        self.context_results[context_result_name] = context_result

    def __contains__(self, context_result_name: object) -> bool:
        """Test if result manager in result managers.

        :param context_result_name: Result-manager name.
        """
        return context_result_name in self.context_results

    def __delitem__(self, context_result_name: str) -> None:
        """Remove result manager from :py:attr:`context_results`.

        :param context_result_name: Result-manager name.
        """
        del self.context_results[context_result_name]

    def __iter__(self):
        """Iterate :py:attr:`context_results` mapping."""
        return iter(self.context_results)

    def __len__(self) -> int:
        """Number of result managers.

        :returns: Number of result contexts.
        """
        return len(self.context_results)
