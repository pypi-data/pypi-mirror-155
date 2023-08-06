from abc import ABC, abstractmethod
import typing as tp
from e4clim.config import Config
from e4clim.container.base import ContainerBase
import e4clim.typing as e4tp


class BuilderBase(ABC):
    """Abstract builder."""

    #: Configuration.
    _cfg: tp.Optional[Config]

    #: Classe.
    _cls: tp.Type[ContainerBase]

    #: Director using this builder.
    _director: 'DirectorBase'

    #: Product being built.
    _product: ContainerBase

    def __init__(self, cls: tp.Type[ContainerBase]) -> None:
        self._cls = cls

    @property
    def cfg(self) -> tp.Optional[Config]:
        return self._cfg

    @property
    def director(self) -> 'DirectorBase':
        return self._director

    @property
    def product(self) -> ContainerBase:
        return self._product

    def reset(self, *args, **kwargs) -> None:
        self._product = self._cls(*args, **kwargs)

    def configure(
            self, cfg: tp.Optional[tp.Union[e4tp.CfgType, e4tp.PathType]],
            parent: ContainerBase = None,
            name: str = None) -> None:
        """Configure.

        :param cfg: Configuration.
        :param parent: Parent container from which the configuration
          could be taken.
        :param name: Container name.
        """
        if (cfg or ((name is None) or (parent is None))):
            self._cfg = Config(cfg)
        else:
            self._cfg = parent.med.parse_configuration(name, parent=parent)


class DirectorBase(object):
    #: Builder.
    _builder: BuilderBase

    def __init__(self, builder: BuilderBase, *args, **kwargs) -> None:
        """Initialize director.

        :param builder: Builder used to make product.
        """
        self._builder = builder

        self._hire_builder(builder)

    @property
    def builder(self) -> BuilderBase:
        return self._builder

    @builder.setter
    def builder(self, builder: BuilderBase) -> None:
        self._builder = builder

    @abstractmethod
    def make(self, **kwargs) -> ContainerBase:
        """Build product."""
        ...

    def _hire_builder(self, builder: BuilderBase) -> None:
        """Hire a builder.

        :param builder: Builder.
        """
        self._builder._director = self
