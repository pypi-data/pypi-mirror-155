from abc import ABC, abstractmethod
import typing as tp
import e4clim
from e4clim.config import import_class_from_cfg
from e4clim.container.optimizer import OptimizerBase
from e4clim.container.optimizer_data_source import (
    OptimizerDataSourceBase, OptimizerInputBase, OptimizerSolutionBase)
import e4clim.typing as e4tp
from .base import ContextBase


class ContextOptimizerBase(ContextBase):

    #: Optimizer.
    _optimizer: tp.Optional[OptimizerBase]

    #: Input data source.
    _input: tp.Optional[OptimizerDataSourceBase]

    #: Solution data source.
    _solution: tp.Optional[OptimizerDataSourceBase]

    def __init__(self, app: 'e4clim.application.Application',
                 name: str = 'context_optimizer',
                 cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Build optimizer context.

        :param app: Context application.
        :param name: Optimizer context name.
        :param cfg: Optimizer configuration.
        """
        super(ContextOptimizerBase, self).__init__(
            name, cfg=cfg, parent=app, **kwargs)

        self._input = None
        self._optimizer = None
        self._solution = None

    @property
    def optimizer(self) -> OptimizerBase:
        """Optimizer property.

        :returns: Optimizer.

        :raises AssertionError: if :py:attr:`_optimizer` is `None`.
        """
        assert self._optimizer is not None, '"_optimizer" attribute not set'

        return self._optimizer

    @optimizer.setter
    def optimizer(self, optimizer: OptimizerBase) -> None:
        """Optimizer property setter also setting new input and solution.

        :param optimizer: Optimizer to set.
        """
        self._optimizer = optimizer

        self._input = self.get_new_input()
        self._solution = self.get_new_solution()

        children: e4tp.ChildrenType = {
            self.optimizer.name: self.optimizer,
            self.input.name: self.input, self.solution.name: self.solution}
        self.update_children(children)

    @property
    def input(self) -> OptimizerDataSourceBase:
        """Input property.

        :returns: Input.

        :raises AssertionError: if :py:attr:`_input` is `None`.
        """
        assert self._input is not None, '"_input" attribute not set'

        return self._input

    @property
    def solution(self) -> OptimizerDataSourceBase:
        """Solution property.

        :returns: Solution.

        :raises AssertionError: if :py:attr:`_solution` is `None`.
        """
        assert self._solution is not None, '"_solution" attribute not set'

        return self._solution

    @abstractmethod
    def get_new_input(self, **kwargs) -> OptimizerDataSourceBase:
        """Get new input from optimizer."""
        ...

    @abstractmethod
    def get_new_solution(self, **kwargs) -> OptimizerDataSourceBase:
        """Get new solution from optimizer."""
        ...

    @abstractmethod
    def solve(self, **kwargs) -> tp.Union[
            e4tp.DatasetType, e4tp.MultiDatasetType]:
        """Solve optimization problem for all cases.

        :returns: Solution dataset.
        """
        ...

    def build_optimizer(self, **kwargs) -> None:
        """Build optimizer."""
        # Import optimizer class
        theclass = import_class_from_cfg(self.cfg)

        # Build optimizer
        self.optimizer = theclass(self, cfg=self.cfg)


class ContextSingleOptimizer(ContextOptimizerBase):

    _input: tp.Optional[OptimizerInputBase]
    _solution: tp.Optional[OptimizerSolutionBase]

    def __init__(self, app: 'e4clim.application.Application',
                 name: str = 'context_optimizer',
                 cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize optimizer context.

        :param app: Context application.
        :param name: Optimizer name.
        :param cfg: Optimizer configuration.
        """
        super(ContextSingleOptimizer, self).__init__(
            app, name=name, cfg=cfg, **kwargs)

    @property
    def input(self) -> OptimizerInputBase:
        """Input property.

        :returns: Input.

        :raises AssertionError: if :py:attr:`_input` is `None`.
        """
        assert self._input is not None, '"_input" attribute not set'

        return self._input

    @property
    def solution(self) -> OptimizerSolutionBase:
        """Solution property.

        :returns: Solution.

        :raises AssertionError: if :py:attr:`_solution` is `None`.
        """
        assert self._solution is not None, '"_solution" attribute not set'

        return self._solution

    def get_new_input(self, **kwargs) -> OptimizerInputBase:
        """Get new input from optimizer."""
        return self.optimizer.get_new_input(**kwargs)

    def get_new_solution(self, **kwargs) -> OptimizerSolutionBase:
        """Get new solution from optimizer.

        :raises AssertionError: if :py:attr:`_input` is `None`.
        """
        assert self._input is not None, '"_input" attribute not set'

        # Get new solution
        data_src = self.optimizer.get_new_solution(**kwargs)

        # Associate input to solution
        data_src._input = self._input

        return data_src

    def solve(self, **kwargs) -> e4tp.DatasetType:
        """Solve optimization problem for all cases.

        :returns: Solution dataset.
        """
        return self.optimizer.solve(**kwargs)


class ContextOptimizerDecoratorBase(ContextOptimizerBase, ABC):
    """Base optimizer context decorator."""

    _context_optimizer: ContextOptimizerBase

    def __init__(self, context_optimizer: ContextOptimizerBase,
                 name: str = 'context_optimizer_decorated',
                 **kwargs) -> None:
        """Initialize optimizer context decorator.

        :param context_optimizer: Optimizer context.
        :param name: Optimizer context name.
        """
        self._context_optimizer = context_optimizer

        super(ContextOptimizerDecoratorBase, self).__init__(
            self._context_optimizer.med._app, name=name,
            cfg=self._context_optimizer.cfg,
            children={self._context_optimizer.name: self._context_optimizer},
            **kwargs)

    @property
    def optimizer(self) -> OptimizerBase:
        """Optimizer property.

        :returns: Optimizer.

        :raises AssertionError: if :py:attr:`_optimizer` is `None`.
        """
        assert self._optimizer is not None, '"_optimizer" attribute not set'

        return self._optimizer

    @optimizer.setter
    def optimizer(self, optimizer: OptimizerBase) -> None:
        """Optimizer property setter also setting child optimizer
        new input and solution.

        :param optimizer: Optimizer to set.
        """
        self._optimizer = optimizer
        self._context_optimizer._optimizer = optimizer

        self._input = self.get_new_input()
        self._solution = self.get_new_solution()

        children: e4tp.ChildrenType = {
            self._context_optimizer.name: self._context_optimizer,
            self.input.name: self.input, self.solution.name: self.solution}
        self.update_children(children)

    def build_optimizer(self, **kwargs) -> None:
        """Build optimizer via child optimizer context.."""
        # Make child optimizer context build optimizer
        self._context_optimizer.build_optimizer(**kwargs)

        # Link optimizer to optimizer from child optimizer context
        self.optimizer = self._context_optimizer.optimizer
