"""Modifier offsetting variable definition."""
from copy import deepcopy
from orderedset import OrderedSet
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.strategy import ExtractorBase
import e4clim.typing as e4tp
from e4clim.utils import tools


class Strategy(ExtractorBase):
    """Modifier offsetting variable"""

    #: Required input variables to component names.
    input_variable_component_names: tp.Optional[e4tp.VCNStrictMutableType]

    #: Offset to add to the variable.
    offset: float

    #: Variable to offset.
    variable_to_offset: str

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

        self.update_input_variable_names(**kwargs)

        self.offset = tools.get_required_float_entry(self.cfg, 'offset')

    def update_input_variable_names(self,  **kwargs) -> None:
        """Add input variable names."""
        self.variable_to_offset = tools.get_required_str_entry(
            self.cfg, 'variable_name')

        # Define variable to component names
        self.input_variable_component_names = {
            self.variable_to_offset: OrderedSet(
                [self.parent.parent.component_name])}

    def transform(self, ds=None, stage: str = None,
                  **kwargs) -> e4tp.DatasetType:
        """Apply modifier to data source.

        :param ds: Dataset. If `None`, :py:obj:`data_src` should be given.
        :param stage: Modeling stage: `'fit'` or `'predict'`.

        :returns: Modified dataset.
        """
        assert stage is not None, '"stage" argument is not optional here'

        data_src = self.data_sources[stage]
        self.info('Adding {} to {}'.format(
            self.offset, self.variable_to_offset))

        # Copy source dataset (all variables)
        if ds is None:
            if isinstance(ds, xr.Dataset):
                ds = data_src.data.copy(deep=True)
            else:
                ds = deepcopy(data_src.data)

        # Modify variable in dataset
        ds[self.variable_to_offset] += self.offset

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_offset_{}_{:d}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            self.variable_to_offset, int(self.offset * 10 + 0.1))
