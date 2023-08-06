"""Scale correction."""
import numpy as np
import xarray as xr
from sklearn.exceptions import NotFittedError
from sklearn import linear_model
import typing as tp
import e4clim
from e4clim.container.result_data_source import Feature
from e4clim.container.strategy import EstimatorBase
import e4clim.typing as e4tp
from e4clim.utils.learn import parse_fit_data, select_data

REGRESSOR = linear_model.RidgeCV


class Strategy(EstimatorBase):
    """Scale correction."""

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
        """Get scale corrector.

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

        # Prevent fitting intercept
        regressor_kwargs['fit_intercept'] = False

        if 'alphas' not in regressor_kwargs:
            # Define regularization path from given logspace parameters
            alphas_logspace = self.cfg.get('alphas_logspace')
            if alphas_logspace is not None:
                alphas = np.logspace(**alphas_logspace)
                regressor_kwargs['alphas'] = alphas

        # Define regressor
        reg = REGRESSOR(**regressor_kwargs)

        # Ridge regression with cross validation
        reg.fit(X, y)

        # Get score
        score = reg.score(X, y)

        # Save coefficients
        try:
            coords = [da_in.region]
        except AttributeError:
            coords = []
        self.coef = xr.DataArray(reg.coef_, coords=coords, name='coef')
        self.coef.attrs['score'] = score
        self.coef.attrs['cv'] = regressor_kwargs['cv']
        try:
            self.coef.attrs['alpha'] = reg.alpha_
            self.coef.attrs['alphas'] = reg.alphas_
        except AttributeError:
            pass

        self.info('Scale regression coefficients:')
        self.info(str(self.coef))

    def predict(self, data_src_in: Feature, **kwargs) -> e4tp.DatasetType:
        """Apply scale corrector.

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
        except (KeyError, ValueError):
            pass

        # Define regressor with previously fitted coefficients
        regressor_kwargs = self.cfg['regressor_kwargs'] or {}

        # Prevent fitting intercept
        regressor_kwargs['fit_intercept'] = False

        reg = REGRESSOR(**regressor_kwargs)
        reg.intercept_ = 0.

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
        return '{}_scaled'.format(
            super(Strategy, self).get_estimator_postfix(**kwargs))


def _get_factorized_input(da_in: xr.DataArray, **kwargs) -> np.ndarray:
    """Get input matrix factorized over regions.

    :param da_in: Input matrix.

    :returns: Factorized input matrix.
    """
    shape = da_in.shape
    if len(shape) == 1:
        X = da_in.values
    else:
        nt, nreg = shape
        X = np.zeros((nt * nreg, nreg))
        for ir in range(nreg):
            # Set block of rows and column corresponding to region
            sl = slice(ir * nt, (ir + 1) * nt)

            # Linear
            X[sl, ir] = da_in.isel(region=ir).values

    return X


def _get_factorized_output(da_out: xr.DataArray, **kwargs) -> np.ndarray:
    """Get output vector factorized over regions.

    :param da_out: Output matrix.

    :returns: Factorized output vector.
    """
    if len(da_out.shape) == 1:
        # Return values
        y = da_out.values
    else:
        # Stack blocks of rows associated to each region
        y = da_out.stack(stacked_dim=['region', 'time'])

    return y
