"""Optimization base definitions."""
from abc import ABC, abstractmethod
from .base import ContainerBase
import e4clim
from e4clim.config import Config
import e4clim.typing as e4tp
from .optimizer_data_source import OptimizerInputBase, OptimizerSolutionBase


class OptimizerBase(ContainerBase, ABC):
    """Optimizer abstract base class. Requires :py:meth:`solve` method to be
    implemented."""

    #: Optimizer context.
    parent: 'e4clim.context.context_optimizer.ContextOptimizerBase'

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextOptimizerBase',
                 name: str, cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Build optimizer linked to mediator.

        :param parent: Optimizer context.
        :param name: Optimizer name.
        :param cfg: Optimizer configuration.
        """
        # Load optimizer configuration
        loaded_cfg = Config(cfg) or self.med.parse_configuration(self.name)

        # Initialize as container with mediator as parent
        super(OptimizerBase, self).__init__(
            name, cfg=loaded_cfg, parent=parent, **kwargs)

    @property
    def input(self) -> OptimizerInputBase:
        return self.parent.input

    @property
    def solution(self) -> OptimizerSolutionBase:
        return self.parent.solution

    @abstractmethod
    def get_new_input(self, **kwargs) -> OptimizerInputBase:
        """Get new input from optimizer."""
        ...

    @abstractmethod
    def get_new_solution(self, **kwargs) -> OptimizerSolutionBase:
        """Get new solution from optimizer."""
        ...

    @abstractmethod
    def solve(self, **kwargs) -> e4tp.DatasetType:
        """Abstract method to solve optimization problem."""
        ...
