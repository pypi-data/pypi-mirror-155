"""Base definition of contexts."""
from e4clim import context
from e4clim.container.base import ContainerBase
import e4clim.typing as e4tp


class ContextBase(ContainerBase):
    """Context base class."""

    def __init__(self, name: str, med: 'context.mediator.Mediator' = None,
                 cfg: e4tp.CfgType = None, parent: ContainerBase = None,
                 **kwargs) -> None:
        """Initialize data-source context.

        :param name: Name.
        :param med: Mediator.
        :param cfg: Configuration.
        :param parent: Parent.
        """
        super(ContextBase, self).__init__(
            name, med=med, cfg=cfg, parent=parent, **kwargs)
