"""Optimizer data sources."""
from abc import ABC, abstractmethod
from pathlib import Path
import e4clim
import e4clim.typing as e4tp
from .base import ContainerBase
from .parsing_single_data_source import ParsingSingleDataSourceBase


class OptimizerDataSourceBase(ContainerBase, ABC):
    """Abstract optimizer data source."""

    #: Optimizer.
    optimizer: 'e4clim.container.optimizer.OptimizerBase'

    parent: 'e4clim.context.context_optimizer.ContextOptimizerBase'

    #: Type name.
    _type_name: str

    @abstractmethod
    def get_data_directory(self, makedirs: bool = True, **kwargs) -> Path:
        ...


class OptimizerSingleDataSourceBase(OptimizerDataSourceBase,
                                    ParsingSingleDataSourceBase, ABC):
    """Abstract optimizer data source."""

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextOptimizerBase',
                 type_name: str, name: str = None, **kwargs) -> None:
        """Initialize optimizer data source.

        :param parent: Optimizer context.
        :param type_name: Data-source type name. Either `'input'`
          or `'solution'`.
        :param name: Name.

        raises AssertionError: if `'optimizer'` attribute of
          :py:obj:`parent` argument is `None`.
        """
        assert parent.optimizer is not None, (
            '"optimizer" attribute of "parent" argument required')

        assert (type_name == 'input') or (type_name == 'solution'), (
            '"type_name" argument should either be "input" or '
            '"solution"')

        self.optimizer = parent.optimizer
        self._type_name = type_name

        name = ('{}_{}'.format(self.optimizer.name, self._type_name)
                if name is None else name)

        cfg = (parent.cfg if self._type_name == 'solution'
               else parent.cfg.get(self._type_name))

        super(OptimizerSingleDataSourceBase, self).__init__(
            parent, name, cfg=cfg, **kwargs)

    def get_data_directory(self, makedirs: bool = True, **kwargs) -> Path:
        """Get path to data directory.

        :param makedirs: Make directories if needed.

        :returns: Data directory path.
        """
        return self.med.cfg.get_project_data_directory(
            self.optimizer, subdirs=self._type_name, makedirs=makedirs)


class OptimizerInputBase(OptimizerSingleDataSourceBase, ABC):
    """Abstract optimization input class as data source with loader."""

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextSingleOptimizer',
                 **kwargs) -> None:
        """Initialize input.

        :param optimizer: Optimizer.
        """
        super(OptimizerInputBase, self).__init__(parent, 'input', **kwargs)

    def get_data_postfix(self, **kwargs) -> str:
        """Get data postfix.

        :returns: Postfix.
        """
        return ''


class OptimizerSolutionBase(OptimizerSingleDataSourceBase, ABC):
    """Optimization solution base class as data source."""

    #: Associated input.
    _input: OptimizerInputBase

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextSingleOptimizer',
                 **kwargs) -> None:
        """Initialize solution.

        :param parent: Optimizer context.
        """
        super(OptimizerSolutionBase, self).__init__(
            parent, 'solution', **kwargs)

        # Make sure there is a variable to parse
        self.update_variables({'single'})

    @property
    def input(self) -> OptimizerInputBase:
        return self._input

    def parse(self, variable_component_names: e4tp.VCNType = None,
              **kwargs) -> e4tp.DatasetType:
        """Parse returning result from
        :py:meth:`'e4clim.container.optimizer.OptimizerBase.solve`.

        :param variable_component_names: Names of components per variable.

        :returns: Solution.
        """
        self.input.get_data(**kwargs)

        return self.optimizer.solve(**kwargs)

    def get_data_postfix(self, **kwargs) -> str:
        """Default implementation of get optimization results postfix.

        :returns: Postfix.
        """
        return self.input.get_data_postfix()
