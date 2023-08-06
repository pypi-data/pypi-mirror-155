from e4clim.context.context_optimizer import (
    ContextOptimizerBase, ContextSingleOptimizer)
from e4clim.context.context_multi_optimizer import (
    ContextMultiOptimizerDecorator)
from e4clim.context.mediator import Mediator
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import BuilderBase, DirectorBase


class BuilderContextOptimizer(BuilderBase):
    """Optimizer context builder."""

    _product: ContextOptimizerBase

    def __init__(self, **kwargs) -> None:
        super(BuilderContextOptimizer, self).__init__(ContextOptimizerBase)

    @property
    def product(self) -> ContextOptimizerBase:
        return self._product

    def reset(self, *args, parent=None, **kwargs) -> None:
        """Build optimizer context.

        :param parent: Application.

        :raises AssertionError: if :py:attr:`cfg` attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute should not be "None"'

        # Build single-case optimizer context
        context_optimizer = ContextSingleOptimizer(
            parent, cfg=self.cfg)

        # Build optimizer context
        cases = tools.get_iterable_str_entry(
            self.cfg, 'cases', list, default=[])
        if cases:
            self._product = ContextMultiOptimizerDecorator(
                context_optimizer)
        else:
            self._product = context_optimizer

        self.product.build_optimizer(**kwargs)


class DirectorContextOptimizer(DirectorBase):
    """Optimizer context director."""

    builder: BuilderContextOptimizer

    def __init__(self, builder: BuilderContextOptimizer) -> None:
        super(DirectorContextOptimizer, self).__init__(builder)

    def make(self, cfg: e4tp.CfgType = None,
             parent: Mediator = None, name: str = None,
             **kwargs) -> ContextOptimizerBase:
        """Make result context.

        :param cfg: Optimizer-context configuration.
        :param parent: Parent component context.
        :param name: Optimizer-context name.

        :returns: Optimizer context.
        """
        assert parent is not None, '"parent" argument should not be "None"'
        assert name is not None, '"name" argument should not be "None"'

        self.builder.configure(cfg, parent=parent, name=name)

        self.builder.reset(parent=parent, **kwargs)
        self.builder.product.info('{} result injected in {} component'.format(
            name, parent.name))

        return self.builder.product
