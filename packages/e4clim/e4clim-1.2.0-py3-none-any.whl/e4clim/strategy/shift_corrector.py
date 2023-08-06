"""Shift correction."""
import xarray as xr
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import cross_val_score
import e4clim
from e4clim.container.result_data_source import Feature
from e4clim.container.strategy import EstimatorBase
import e4clim.typing as e4tp
from e4clim.utils.learn import (
    parse_fit_data, select_data, ShiftingBiasCorrector)
from .scale_corrector import _get_factorized_input, _get_factorized_output

REGRESSOR = ShiftingBiasCorrector


class Strategy(EstimatorBase):
    """Shift correction."""

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

    def fit(self, data_src_in: Feature, data_src_out: Feature,
            **kwargs) -> None:
        """Get shift corrector.

        :param data_src_in: Training set input data source.
        :param data_src_out: Training set output data source.
        """
        # Get input and output data arrays
        da_in, da_out = parse_fit_data(
            data_src_in, data_src_out, self.parent,
            subsample_freq=self.cfg.get('subsample_freq'),
            select_period=True, time_slice=self.cfg.get('time_slice'),
            **kwargs)

        # Select intersection
        t_in = da_in.indexes['time']
        t_intersect = t_in.intersection(da_out.indexes['time'])
        da_in = da_in.sel(time=t_intersect)
        da_out = da_out.sel(time=t_intersect)

        # Select valid
        valid = ~da_in.isnull() & ~da_out.isnull()
        da_in = da_in.where(valid, drop=True)
        da_out = da_out.where(valid, drop=True)

        self.info('Computing {} {} bias corrector from {} to {} '.format(
            self.parent.name, self.parent.parent.name,
            *da_in.indexes['time'][[0, -1]]))

        # Make multiple regional models into one model
        X = _get_factorized_input(da_in, **kwargs)
        y = _get_factorized_output(da_out, **kwargs)

        # Configure regression
        regressor_kwargs = self.cfg.get('regressor_kwargs') or {}

        if 'cv' not in regressor_kwargs:
            # Split by year for cross validation
            years = da_in.indexes['time'].year
            regressor_kwargs['cv'] = years.max() - years.min() + 1

        # Define regressor
        reg = REGRESSOR()

        # Get score
        score = cross_val_score(
            reg, X, y, cv=regressor_kwargs['cv']).mean()

        # Fit
        reg.fit(X, y)

        # Save coefficients
        try:
            coords = [da_in.region]
        except AttributeError:
            coords = []
        self.coef = xr.DataArray(reg.coef_, coords=coords, name='coef')
        self.coef.attrs['score'] = score
        self.coef.attrs['cv'] = regressor_kwargs['cv']

        self.info('Shift coefficients:')
        self.info(str(self.coef))

    def predict(self, data_src_in: Feature, **kwargs) -> e4tp.DatasetType:
        """Apply shift corrector.

        :param data_src_in: Input feature.

        :returns: Corrected dataset.
        """
        # Verify that bias corrector has been fitted
        if self.coef is None:
            raise NotFittedError('This bias corrector instance '
                                 'must be fitted before prediction.')

        # Select result, copy and ensure dimensions order
        da_in = select_data(data_src_in, self.parent, **kwargs)

        # Reorder regions to comply
        coef_comp = (self.coef.loc[{'region': da_in.indexes['region']}]
                     if 'region' in self.coef.coords else self.coef.copy())

        # Select component if needed
        try:
            coef_comp = coef_comp.sel(
                component=self.parent.parent.component_name)
        except ValueError:
            pass

        # Define regressor with previously fitted coefficients
        reg = REGRESSOR()

        # Set fitted coefficients
        reg.coef_ = coef_comp.values

        # Initialize prediction depending on input dimensions
        if len(da_in.shape) > 1:
            da_pred = xr.full_like(
                da_in.stack(stacked_dim=['region', 'time']), None)
        else:
            da_pred = xr.full_like(da_in, None)

        # Get factorized input
        X = _get_factorized_input(da_in, **kwargs)

        # Predict
        da_pred[:] = reg.predict(X)

        # Unstack, if needed
        if len(da_in.shape) > 1:
            da_pred = da_pred.unstack('stacked_dim').transpose(
                'time', 'region')

        return {self.parent.result_name: da_pred}

    def get_estimator_postfix(self, **kwargs) -> str:
        """Get bias-corrector postfix.

        returns: Postfix.
        """
        return '{}_shifted'.format(
            super(Strategy, self).get_estimator_postfix(**kwargs))
