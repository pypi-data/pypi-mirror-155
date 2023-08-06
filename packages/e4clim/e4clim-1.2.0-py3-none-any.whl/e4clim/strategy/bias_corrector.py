"""Bias corrector and predictor."""
from sklearn.exceptions import NotFittedError
import typing as tp
import e4clim
from e4clim.container.result_data_source import Feature
from e4clim.container.strategy import EstimatorBase
import e4clim.typing as e4tp
import e4clim.utils.learn as learn
from e4clim.utils import tools


class Strategy(EstimatorBase):
    """Bias corrector and predictor."""

    #: Operator choice.
    _operator_choice: str

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

        self._operator_choice = tools.get_required_str_entry(
            self.cfg, 'operator', 'scale')

        assert self._operator_choice in ['scale', 'shift'], (
            '"operator" entry in configuration should either be "scale" '
            'or "shift"')

    def fit(self, data_src_in: Feature, data_src_out: Feature,
            **kwargs) -> None:
        """Get bias corrector for component as a factor to multiply the
        input data with and such that the training input data
        multiplied by the bias corrector has the same mean
        as the training output data over the same period.

        :param data_src_in: Training set input data source.
        :param data_src_out: Training set output data source.

        .. warning:: If the `intersection_only_if_possible` entry of the
          container configuration is `True`, an attempt is made to
          compute the bias on a common time-slice. The time indices of
          the two data sources should, however, be compatible.

        .. seealso:: :py:func:`_intersection_time_slice`
        """
        # Get input and output data arrays
        subsample_freq = tools.get_str_entry(self.cfg, 'subsample_freq')
        time_slice = tools.get_iterable_str_entry(
            self.cfg, 'time_slice', tuple)
        da_in, da_out = learn.parse_fit_data(
            data_src_in, data_src_out, self.parent,
            subsample_freq=subsample_freq, select_period=True,
            time_slice=time_slice, **kwargs)

        # Check if selected period intersects that of input period
        time_slice_in = slice(*da_in.indexes['time'][[0, -1]])
        time_slice_out = slice(*da_out.indexes['time'][[0, -1]])
        ioip = tools.get_bool_entry(self.cfg, 'intersection_only_if_possible')
        if ioip:
            inter_slice = learn.intersection_time_slice(da_in, da_out)
            if inter_slice is not None:
                time_slice_in = time_slice_out = inter_slice

        # Get bias corrector
        self.info(
            'Computing {} {} bias corrector from {} to {} (input) '
            'and from {} to {} (output)'.format(
                self.parent.name, self.parent.parent.name,
                time_slice_in.start, time_slice_in.stop,
                time_slice_out.start, time_slice_out.stop))
        mean_in = da_in.sel(time=time_slice_in).mean('time')
        mean_out = da_out.sel(time=time_slice_out).mean('time')
        bc = self._operator_inv(mean_out, mean_in)

        # Convert coordinates datatypes from object to str if needed
        for dim in bc.dims:
            if bc[dim].dtype == object:
                bc[dim] = bc[dim].astype(str)
        self.coef = bc

        self.info('Computed average ({} / {}):'.format(
            time_slice_in.start, time_slice_in.stop))
        self.info(mean_in.values)
        self.info('Observed average ({} / {}):'.format(
            time_slice_out.start, time_slice_out.stop))
        self.info(mean_out.values)

    def predict(self, data_src_in: Feature, **kwargs) -> e4tp.DatasetType:
        """Apply bias corrector for component by multipling input data.

        :param data_src_in: Input data source.

        :returns: Bias corrected dataset.
        """
        ds = {}
        # Verify that bias corrector has been fitted
        if self.coef is None:
            raise NotFittedError('This bias corrector instance '
                                 'must be fitted before prediction.')

        # Select result, copy and ensure dimensions order
        da_in = learn.select_data(data_src_in, self.parent, **kwargs)

        # Copy input dataset
        da_pred = da_in.copy(deep=True)

        # Reorder regions to comply
        coef_comp = (self.coef.loc[{'region': da_in.indexes['region']}]
                     if 'region' in self.coef.coords else self.coef.copy())

        # Select component if needed
        try:
            coef_comp = coef_comp.sel(
                component=self.parent.parent.component_name)
        except ValueError:
            pass

        # Apply bias corrector, with input data
        da_pred = self._operator(da_pred, coef_comp)

        # Add bias-corrected output variable to dataset
        ds[self.parent.result_name] = da_pred

        return ds

    def _operator(self, a: tp.Any, b: tp.Any) -> tp.Any:
        """Bias-correction operator.
        Multiplication (resp. addition) if :py:attr:`_operator_choice`
        is `'scale'` (resp. `'shift'`).
        """
        if self._operator_choice == 'scale':
            return a * b
        elif self._operator_choice == 'shift':
            return a + b

    def _operator_inv(self, a: tp.Any, b: tp.Any) -> tp.Any:
        """Inverse bias-correction operator.
        Division (resp. substraction) if :py:attr:`_operator_choice`
        is `'scale'` (resp. `'shift'`).
        """
        if self._operator_choice == 'scale':
            return a / b
        elif self._operator_choice == 'shift':
            return a - b

    def get_estimator_postfix(self, **kwargs) -> str:
        """Get bias-corrector postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_nobias'.format(
            super(Strategy, self).get_estimator_postfix(**kwargs))
