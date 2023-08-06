from orderedset import OrderedSet
import typing as tp
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools


class TaskManager(tp.MutableMapping):
    """Task manager."""

    #: Container for which to manage tasks.
    _container: 'e4clim.container.base.ContainerBase'

    #: Container name.
    _name: str

    #: Tasks.
    _tasks: tp.Optional[tp.MutableMapping[str, bool]]

    #: Task names.
    _task_names: tp.MutableSet[str]

    def __init__(self, container: 'e4clim.container.base.ContainerBase',
                 task_names: e4tp.StrIterableType = None,
                 default_tasks_value: bool = True, **kwargs) -> None:
        """Initialize task manager and ask to perform all tasks, or not.

        :param container: Container.
        :param task_names: Task names.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none.
        """
        # Attach container to its task manager
        self._container = container
        self._name = '{}__task_manager'.format(self.container.name)

        # Initialize tasks
        if task_names is not None:
            self._task_names = tools.ensure_collection(task_names, OrderedSet)
        else:
            self._task_names = OrderedSet()

        self._tasks = {}
        if self.task_names:
            self.set_all(default_tasks_value)

    @property
    def container(self) -> 'e4clim.container.base.ContainerBase':
        return self._container

    @property
    def name(self) -> str:
        return self._name

    @property
    def tasks(self) -> tp.Optional[tp.MutableMapping[str, bool]]:
        return self._tasks

    @property
    def task_names(self) -> tp.MutableSet[str]:
        return self._task_names

    def update(self, other=(), /, **kwargs) -> None:
        """Set given task(s) to given value(s). If a task name
        does not exist yet, it is created and its state set to value.

        :param other: Task (name, value) pairs.
        """
        if other:
            for task_name, value in other.items():
                # Add each single task
                self[task_name] = value

    def __setitem__(self, task_name: str, value: bool) -> None:
        """Set single given task.

        :param task_name: Task name to set.
        :param value: Task state value.
        """
        # Add task if needed
        if task_name not in self.task_names:
            self.task_names.add(task_name)

        # Set task to value
        if self.tasks is None:
            self._tasks = {task_name: value}
        else:
            self.tasks[task_name] = value

    def set_all(self, value: bool = True,
                task_names: e4tp.StrIterableType = None) -> None:
        """Set all tasks to given value.

        :param value: State value with which to set all tasks.
        :param task_names: Name of task(s) to set.
          in which case all tasks are set.
        :type value: bool
        :type task_names: (collection of) :py:class:`str`

        .. note:: A task is made more precise by adding `__`
          separated words, e.g. `'parse__capacity_factor'`.
          To update all `'parse'` tasks, `'parse'` can then simply be given.
        """
        # Interesect given and available task names
        if task_names is None:
            valid_task_names = self.task_names
        else:
            valid_task_names = tools.ensure_collection(task_names, OrderedSet)
        avail_task_names = OrderedSet()
        valid_task_names_list = [task.split('__') for task in valid_task_names]
        task_names_list = [task.split('__') for task in self.task_names]
        for task_name in valid_task_names_list:
            for avail_task in task_names_list:
                if avail_task[:len(task_name)] == task_name:
                    avail_task_names.add('__'.join(avail_task))

        # Update container tasks
        self.update({tn: value for tn in avail_task_names})

        # Update children tasks
        for child in self.container.children.values():
            child.task_mng.set_all(value, task_names)

    def __getitem__(self, key):
        """Get item from :py:attr:`task`."""
        return self.tasks[key]

    def __contains__(self, key):
        """:py:attr:`task` contains."""
        return key in self.tasks

    def __delitem__(self, key):
        # Remove task from dictionary
        del self.tasks[key]
        # Remove task name from set
        self.task_names.discard(key)

    def __iter__(self):
        """Iterate :py:attr:`task`."""
        return iter(self.tasks)

    def __len__(self, key, value):
        """Length of :py:attr:`task`."""
        return len(self.tasks)

    def __str__(self):
        """Get string of container and its children's tasks."""
        s = '{}: {}'.format(self.container.name, str(self.tasks))
        for child in self.container.children.values():
            s += '\n  ' + '\n  '.join(str(child.task_mng).split('\n'))

        return s

    def get(self, key, default=None):
        """Get item from :py:attr:`task`."""
        return self.tasks.get(key, default)
