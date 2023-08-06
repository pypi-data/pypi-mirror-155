"""Base container and task manager classes definitions."""
from collections import OrderedDict
from copy import deepcopy
from orderedset import OrderedSet
from pathlib import Path
import typing as tp
from e4clim import context
from e4clim.config import Config
import e4clim.typing as e4tp
from .task_manager import TaskManager


class ContainerBase(object):
    #: Configuration.
    _cfg: Config

    #: Containers depending this one.
    _children: e4tp.ChildrenMutableType

    #: Mediator.
    _med: 'context.mediator.Mediator'

    #: Name.
    _name: str

    #: Parent container.
    _parent: 'ContainerBase'

    #: Verbose flag.
    _verbose: bool

    def __init__(
            self, name: str, med: 'context.mediator.Mediator' = None,
            cfg: e4tp.CfgType = None, parent: 'ContainerBase' = None,
            children: e4tp.ChildrenType = None,
            task_names: tp.Optional[e4tp.StrIterableType] = OrderedSet(),
            default_tasks_value: bool = True, **kwargs) -> None:
        """Initialize mediator, configuration and name.

        :param name: Container name.
        :param med: Mediator. If `None`, it is inherited from parent.
        :param cfg: Container configuration.
        :param parent: Parent container.
        :param children: Set of all containers attached to this container.
        :param task_names: Names of potential tasks for container to perform.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none.
        """
        if med is not None:
            self._med = med
        elif parent is not None:
            self._med = parent.med

        if cfg is not None:
            self._cfg = Config(cfg)
        else:
            self._cfg = Config()

        try:
            self._verbose = not self.cfg['no_verbose']
        except (TypeError, KeyError):
            self._verbose = True

        self._name = name

        self._children = OrderedDict()

        self._set_genealogy(parent, children)

        #: Task manager.
        self._task_mng: TaskManager = TaskManager(
            self, task_names, default_tasks_value=default_tasks_value)

    @property
    def med(self) -> 'context.mediator.Mediator':
        return self._med

    @property
    def cfg(self) -> Config:
        return self._cfg

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def verbose(self) -> bool:
        return self._verbose

    @property
    def children(self) -> e4tp.ChildrenMutableType:
        return self._children

    @property
    def parent(self) -> 'ContainerBase':
        return self._parent

    @property
    def tasks(self) -> tp.Optional[tp.MutableMapping[str, bool]]:
        return self.task_mng.tasks

    @property
    def task_mng(self) -> TaskManager:
        return self._task_mng

    def set_tasks(self, value: bool = True,
                  task_names: e4tp.StrIterableType = None) -> None:
        """Set all tasks to given value.

        :param value: State value with which to set all tasks.
        :param task_names: Name of task(s) to set. If `None`,
          all tasks are set.

        .. note:: A task is made more precise by adding `__`
          separated words, e.g. `'parse__capacity_factor'`.
          To update all `'parse'` tasks, `'parse'` can then simply be given.
        """
        self.task_mng.set_all(value=value, task_names=task_names)

    def info(self, msg: str) -> None:
        """Log an information message.

        :param msg: Message.
        """
        if self.verbose:
            self.med.log.info(msg)

    def warning(self, msg: str) -> None:
        """Log a warning.

        :param msg: Message.
        """
        self.med.log.warning(msg)

    def critical(self, msg: str) -> None:
        """Log a critical message.

        :param msg: Message.
        """
        self.med.log.critical(msg)

    def _set_genealogy(self, parent: tp.Optional['ContainerBase'],
                       children: tp.Optional[e4tp.ChildrenType]) -> None:
        """Set parent and children containers.

        :param parent: Parent.
        :param children: Children.
        """
        # Set parent once and for all
        self._set_parent(parent)

        # Update children
        self.update_children(children)

    def _set_parent(self, parent: tp.Optional['ContainerBase']) -> None:
        """Set parent container.

        :param parent: Parent.
        """
        if parent is not None:
            # Set parent
            self._parent = parent

            # Add child to parent
            self._parent.update_children({self.name: self})

    def update_children(self, children:
                        tp.Optional[e4tp.ChildrenType]) -> None:
        """Add children to data source and set parent of each child.

        :param children: Children containers to add.
        """
        if children is not None:
            # Add children
            self._children.update(children)

            # Set parent
            for child in children.values():
                child._parent = self

    def get_data_directory(self, makedirs: bool = True, **kwargs) -> Path:
        """Get path to data directory.

        :param makedirs: Make directories if needed.

        :returns: Data directory path.
        """
        return self.med.cfg.get_project_data_directory(
            self, makedirs=makedirs, **kwargs)

    def __enter__(self) -> 'ContainerBase':
        """Context management saving tasks status."""
        self._task_enter = deepcopy(self.task_mng.tasks)

        return self

    def __exit__(self, exc_type: tp.Type, exc_val: tp.Type,
                 exc_tb: tp.Type) -> None:
        """Context management restoring tasks status."""
        self.task_mng._tasks = self._task_enter


class ContainerType(tp.Protocol):
    _med: 'context.mediator.Mediator'

    _cfg: Config

    _verbose: bool

    _name: str

    _children: e4tp.StrToContainerType

    _parent: ContainerBase

    _task_mng: TaskManager

    @property
    def med(self) -> 'context.mediator.Mediator': ...

    @property
    def cfg(self) -> Config: ...

    @property
    def name(self) -> str: ...

    @property
    def verbose(self) -> bool: ...

    @property
    def children(self) -> e4tp.StrToContainerType: ...

    @property
    def parent(self) -> ContainerBase: ...

    @property
    def task_mng(self) -> TaskManager: ...

    def set_tasks(self, value: bool = True,
                  task_names: e4tp.StrIterableType = None) -> None: ...

    def info(self, msg: str) -> None: ...

    def warning(self, msg: str) -> None: ...

    def critical(self, msg: str) -> None: ...

    def update_children(self, children:
                        tp.Optional[e4tp.ChildrenType]) -> None: ...

    def get_data_directory(self, makedirs: bool = True,
                           **kwargs) -> Path: ...

    def __enter__(self) -> 'ContainerBase': ...

    def __exit__(self, exc_type: tp.Type, exc_val: tp.Type,
                 exc_tb: tp.Type) -> None: ...
