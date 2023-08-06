from collections import MutableMapping
import logging
from pathlib import Path
import typing as tp
import e4clim
from e4clim.application import Application
from e4clim.config import Config
from e4clim.container.data_source import DataSourceBase
from e4clim.container.geo_data_source import GeoDataSourceBase
from e4clim.container.optimizer import OptimizerBase
from e4clim.context.context_optimizer import ContextOptimizerBase
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import ContextBase
from .context_component import ContextComponent


class Mediator(ContextBase, MutableMapping):
    #: Parent application.
    _app: Application

    #: Logger.
    _log: logging.Logger

    def __init__(self, cfg: tp.Optional[Config], app: Application, **kwargs):
        """Initialize mediator.

        :param cfg: Configuration.
        :param app: Application.
        """
        self._app = app

        name = 'mediator'
        super(Mediator, self).__init__(name, med=self, cfg=cfg, **kwargs)

    @property
    def app(self) -> Application:
        return self._app

    @property
    def log(self) -> logging.Logger:
        return self._log

    def build_data_source(self, *args, **kwargs) -> DataSourceBase:
        return self.app.context_data_sources.build(*args, **kwargs)

    def parse_configuration(
            self, name: str,
            parent: 'e4clim.container.base.ContainerBase'
            = None) -> tp.Optional[Config]:
        """Load container configuration from main configuration dictionary,
        from given parent, or from file.

        :param name: Container name.
        :param parent: Parent container from the configuration of which,
          the configuration of this child container could be gotten.

        :returns: Container configuration.
        """
        user_cfg_path = _get_cfg_path(self, name)
        cont_cfg_from_parent = _get_parent_cfg(parent, name)

        if name in self.cfg:
            # Get source configuration from main configuration
            cont_cfg_map = self.cfg[name]
            cont_cfg = Config(cont_cfg_map)
        elif user_cfg_path:
            cont_cfg = Config(user_cfg_path)
        elif cont_cfg_from_parent:
            # Get source configuration from container configuration
            cont_cfg = cont_cfg_from_parent
        else:
            # None worked, no configuration found
            self.warning('No {} configuration found'.format(name))
            return None

        return cont_cfg

    @property
    def data_sources(self) -> e4tp.DataSourcesType:
        return self.app.context_data_sources.data_sources

    @property
    def geo_src(self) -> tp.Optional[GeoDataSourceBase]:
        return self.app.context_geo_data_source.data_src

    @property
    def geo_cfg(self) -> Config:
        return self.app.context_geo_data_source.cfg

    @property
    def context_components(self) -> tp.MutableMapping[str, ContextComponent]:
        return self.app.context_components

    @property
    def context_optimizer(self) -> tp.Optional[ContextOptimizerBase]:
        return self.app.context_optimizer

    @property
    def optimizer(self) -> OptimizerBase:
        assert self.context_optimizer is not None, (
            '"context_optimizer" attribute is "None"')
        return self.context_optimizer.optimizer

    def __getitem__(self, context_component_name: str) -> ContextComponent:
        """Get component from :py:attr:`components`.

        :param context_component_name: Component-context name.

        :returns: Component context.
        """
        return self.app.context_components[context_component_name]

    def get(self, context_component_name: str,
            default=None) -> tp.Optional[ContextComponent]:
        """Get component from :py:attr`data`.

        :param context_component_name: Component-context name.
        :param default: Default value.

        :returns: component.
        """
        return self.app.context_components.get(
            context_component_name, default)

    def __setitem__(self, context_component_name: str,
                    context_component: ContextComponent) -> None:
        """Set component in :py:attr:`data`.

        :param context_component_name: Component-context name.
        :param context_component: Component context to set.
        """
        self.app.context_components[
            context_component_name] = context_component

    def __contains__(self, context_component_name: object) -> bool:
        """Test if component context in :py:attr:`context_components`.

        :param context_component_name: component name.
        """
        return context_component_name in self.app.context_components

    def __delitem__(self, context_component_name: str) -> None:
        """Remove component context from :py:attr:`context_components`.

        :param context_component_name: Component-context name.
        """
        del self.app.context_components[context_component_name]

    def __iter__(self):
        """Iterate :py:attr:`context_components` mapping."""
        return iter(self.app.context_components)

    def __len__(self) -> int:
        """Number of component contexts.

        :returns: Number of component contexts.
        """
        return len(self.app.context_components)


def _get_cfg_path(parent: 'e4clim.container.base.ContainerBase',
                  name: str) -> tp.Optional[e4tp.PathType]:
    """Get configuration path from parent configuration.

    :param parent: Parent.
    :param name: Name of container for which to get configuration.

    :returns: Configuration path.
    """
    try:
        # Try to get path to container configuration
        # given in mediator configuration
        cfg_cfg_path = tools.get_required_mapping_entry(parent.cfg, 'cfg_path')
        cfg_path = tools.get_required_iterable_str_entry(
            cfg_cfg_path, name, list)

        return Path(*cfg_path)
    except AssertionError:
        return None


def _get_parent_cfg(parent: tp.Optional['e4clim.container.base.ContainerBase'],
                    name: str) -> tp.Optional[Config]:
    """Get configuration from parent.

    :param parent: Parent.
    :param name: Name of container for which to get configuration.

    :returns: Configuration.
    """
    if parent is not None:
        try:
            return Config(parent.cfg[name])
        except (AttributeError, KeyError):
            return None
    else:
        return None
