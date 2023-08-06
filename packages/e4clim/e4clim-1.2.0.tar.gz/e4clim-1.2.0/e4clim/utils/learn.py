"""Statistical learning."""
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
from sklearn.base import clone, BaseEstimator
from sklearn.metrics import r2_score
import e4clim
from e4clim.container.data_source import DataSourceBase
import e4clim.typing as e4tp
from e4clim.utils import tools


TimeSliceType = tp.Union[slice, tp.Collection[str]]


class ShiftingBiasCorrector():
    """Bias corrector via shifting in order for the input and output
    means to coincide.
    """

    #: Intercept set when fitting.
    coef_: tp.Optional[tp.Any]

    def __init__(self):
        """Constructor."""
        self.coef_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ShiftingBiasCorrector':
        """Fit.

        :param X: Input data.
        :param y: output data.

        :returns: :py:obj:`self`.

        .. warning:: :py:obj:`X` and :py:obj:`y` should have the same
          dimensions.
        """
        self.coef_ = y.mean() - X.mean()

        return self

    def predict(self, X: np.ndarray, return_std: bool = False) -> np.ndarray:
        """Predict multi-output variable using a model
            trained for each target variable.

        :param X: Input data.

        :returns: Prediction.
        """
        return X + self.coef_

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """r2 score.

        :param X: Input data.
        :param y: output data.

        :returns: r2 score.
        """
        return r2_score(y, self.predict(X))

    def get_params(self, deep: bool = True) -> dict:
        return {}

    def set_params(self, d: tp.Any) -> 'ShiftingBiasCorrector':
        return self


class MultiInputRegressor():
    """Multi input estimator.

    :param estimator: An estimator implementing `fit` and `predict`.
    :type estimator: estimator object
    """

    #: Base estimator.
    estimator: BaseEstimator
    #: Multiple estimators.
    estimators: tp.List[BaseEstimator]
    #: Number of estimators.
    n_estimators: int
    #: Scores for each estimator.
    scores: np.ndarray

    def __init__(self, estimator):
        """Constructor.

        :param estimator: Estimator.
        :type estimator: :py:class:`sklearn.base.BaseEstimator`
        """
        self.estimator = estimator

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MultiInputRegressor':
        """Fit model to data.
        Fit a separate model for each input and output variables.

        :param X: Input array,
            shape(n_samples, n_feature, n_outputs).
        :param y: Output array, shape(n_samples, n_outputs)

        :returns: :py:obj:`self`
        """
        # Loop over inputs and outputs
        self.estimators = []
        Xy_rng = zip(X.T, y.T) if len(X.shape) > 2 else [(X.T, y.T)]
        for ie, (X_l_T, y_l_T) in enumerate(Xy_rng):
            # Clone estimator
            e = clone(self.estimator)

            # Fit data
            e.fit(X_l_T.T, y_l_T.T)

            # Save estimator
            self.estimators.append(e)

        # Save number of estimators
        self.n_estimators = len(self.estimators)

        return self

    def predict(self, X: np.ndarray, return_std: bool = False) -> tp.Union[
            np.ndarray, tp.Tuple[np.ndarray, np.ndarray]]:
        """Predict multi-output variable using a model
            trained for each target variable.

        :param X: Input data, shape(n_samples, n_feature, n_outputs).
        :param return_std: If `True`, return standard deviation
           of posterior prediction(in the Bayesian case).

        :returns: Prediction.
        """
        shape = [X.shape[0]]
        if len(X.shape) > 2:
            shape.append(X.shape[-1])
            # First dimension as list for type compatibility
            X_rng = [x0 for x0 in X.T]
        else:
            shape.append(1)
            X_rng = [X.T]
        y_pred = np.empty(shape)
        if return_std:
            y_std = np.empty(shape)

        for ie, X_l_T in enumerate(X_rng):
            # Manage return std for Bayesian case only
            kwargs = {'return_std': True} if return_std else {}

            # Predict
            pred = self.estimators[ie].predict(X_l_T.T, **kwargs)

            # Manage prediction result
            if return_std:
                y_pred[:, ie] = pred[0]
                y_std[:, ie] = pred[1]
            else:
                y_pred[:, ie] = pred
        if return_std:
            return (y_pred, y_std)
        else:
            return y_pred

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute individual scores and variance-weighted score
        of multiple-output prediction.

        :param X: Input data, shape(n_samples, n_feature, n_outputs).
        :param y: True target data, shape(n_samples, n_outputs).

        :returns: Variance-weighted score.

        .. note:: Individual scores are saved in :py:attr:`scores`.
        """
        # Predict
        y_pred = self.predict(X)

        # Save raw scores
        self.scores = r2_score(y, y_pred, multioutput='raw_values')

        # Return variance weighted score
        score = (self.scores * y.var(0)).sum() / y.var(0).sum()

        return score


def intersection_time_slice(da_in: xr.DataArray,
                            da_out: xr.DataArray) -> tp.Optional[slice]:
    """Get full years intersection between two arrays, if possible.

    :param da_in: First array.
    :param da_out: Second array.

    :returns: Intersection time slice if not empty.

    .. warning:: The time index of the input and output arrays
      must be compatible. For instance, daily-sampled indices
      but with different hours won't intersect.
    """
    # Match frequencies
    t_out = da_out.indexes['time']
    freq_out = t_out.inferred_freq
    t_in = da_in.indexes['time']
    freq_in = t_in.inferred_freq
    if freq_out in ['A-DEC', 'Y']:
        # Make index of yearly mean start 1st of January
        da_out['time'] = pd.DatetimeIndex(
            ['{}-01-01'.format(t.year) for t in t_out])
        if freq_in == 'H':
            start = '{}-01-01 00:00:00'.format(t_out[0].year)
            end = '{}-12-31 23:00:00'.format(t_out[-1].year)
            t_out_hour = pd.date_range(start, end, freq=freq_in)
            da_out = da_out.reindex(time=t_out_hour, method='ffill')

    t_inter = da_out.indexes['time'].intersection(
        da_in.indexes['time'])
    if len(t_inter) > 0:
        first_date_inter = t_inter[0]
        last_date_inter = last_full_years_date(
            t_inter, first_date_inter)
        if ((last_date_inter - first_date_inter)
                >= pd.Timedelta('365 days')):
            # If there are at least a year of common data,
            # use common data only
            time_slice = slice(first_date_inter, last_date_inter)

            return time_slice
    return None


def parse_fit_data(
        data_src_in: DataSourceBase, data_src_out: DataSourceBase,
        parent: 'e4clim.context.context_result.ContextResult',
        subsample_freq: str = None, select_period: bool = False,
        time_slice: TimeSliceType = None,
        **kwargs) -> tp.Tuple[xr.DataArray, xr.DataArray]:
    """Get input and output data arrays.

    :param data_src_in: Training set input data source.
    :param data_src_out: Training set output data source.
    :param parent: Result manager.
    :param subsample_freq: Sub-sampling frequency.
      If `None`, no sub-sampling is performed.
    :param time_slice: Time slice to select period.
      If `None`, the full period is kept.
    :param select_period: Whether to select period.

    :returns: Input and output data arrays.
    """
    # Select result, copy and ensure dimensions order
    da_in = select_data(data_src_in, parent, **kwargs)
    da_out = select_data(data_src_out, parent, **kwargs)

    # Subsample if requested
    if subsample_freq:
        da_in = da_in.resample(time=subsample_freq).mean('time')
        da_out = da_out.resample(time=subsample_freq).mean('time')

    if select_period:
        # Select input and output periods
        # as given by configuration or first full years
        da_in, time_slice = select_period_from_array(
            da_in, time_slice=time_slice, **kwargs)
        da_out, _ = select_period_from_array(
            da_out, time_slice=time_slice, **kwargs)

    return da_in, da_out


def select_period_from_array(
        da: xr.DataArray, time_slice: TimeSliceType = None,
        **kwargs) -> tp.Tuple[xr.DataArray, slice]:
    """Select full years period from an array.
    Try to get first and last dates from configuration.
    Otherwise, select the first full years.

    :param da: Array.
    :param time_slice: Time slice to select period.
      If `None`, the full period is kept.

    :returns: Tuple containing the selected array and time slice.
    """
    if time_slice is None:
        # Get time index
        time = da.indexes['time']

        # First date is given or first available date
        first_date = pd.Timestamp(time[0])

        # Last date is given or last date which is a multiple of one
        # year past first date
        last_date = pd.Timestamp(
            last_full_years_date(time, first_date, **kwargs))
    else:
        if isinstance(time_slice, slice):
            first_date, last_date = time_slice.start, time_slice.stop
        else:
            first_date, last_date = time_slice

    # Slice
    time_slice = slice(first_date, last_date)
    da = da.sel(time=time_slice)

    return da, time_slice


def last_full_years_date(time: pd.DatetimeIndex,
                         first_date: pd.Timestamp, **kwargs) -> pd.Timestamp:
    """Get last date in date-time index which is a multiple of a year
    away from start date.

    :param time: Date-time index.
    :param first_date: First date.

    :returns: Last date.
    """
    last_date = pd.date_range(time[0], time[-1], freq='A-DEC')[-1]

    # Make sure last samples are present
    freq = time.inferred_freq
    if freq is None:
        if (time[1] - time[0]).seconds == 3600:
            freq = 'H'
    if freq == 'H':
        last_date += pd.Timedelta('23H')

    return last_date


def select_data(
        data_src: DataSourceBase,
        parent: 'e4clim.context.context_result.ContextResult',
        variable_name: str = None, place_name: str = None,
        **kwargs) -> xr.DataArray:
    """Select variable from data source, copy it, reorder regions,
    drop components and transpose, if possible.

    :param data_src: Training set input data source.
    :param parent: Result manager.
    :param variable_name: Variable to select from data source.
      If `None`, `parent.result_name` is used instead.
    :param place_name: Name of place to select.
      If `None`, no place is selected.
    :type data_src: :py:class:`..data_source.DataSourceBase`
    :type parent: :py:class:`..component.ContextResult`
    :type variable_name: str
    :type place_name: str

    :returns: Input and output data arrays.
    :rtype: :py:class:`tuple` containing two
      :py:class:`xarray.DataArray`'s
    """
    # Select variable or result
    variable_name = variable_name or parent.result_name
    da = data_src[variable_name].copy(deep=True)

    if place_name is not None:
        da = da.sel(region=place_name, drop=True)
    else:
        # Try to reorder regions from component-manager place names
        try:
            da = da.sel(region=parent.parent.place_names)
        except (ValueError, KeyError):
            pass

    # Try to select component in case needed
    try:
        da = da.sel(component=parent.parent.component_name, drop=True)
    except (KeyError, ValueError):
        pass
    try:
        msg = 'Requested component does not match component in data'
        assert da.component == parent.parent.component_name, msg
        da = da.drop('component')
    except AttributeError:
        pass

    # Try to transpose
    try:
        da = da.transpose('time', 'region')
    except ValueError:
        pass

    return da


def get_transform_function(
        data_src, stage: str,
        other_functions: tp.Iterable[e4tp.TransformStrictType] = [],
        modifier: 'e4clim.container.strategy.ExtractorBase' = None,
        crop_area: bool = True) -> (
            e4tp.TransformStrictType):
    """Get transform functions.

    :param data_src: Data source for which to get transform functions.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
    :param other_functions: Additional transform functions.
    :param modifier: Modifier.
    :param crop_area: Whether to crop area or not.

    :returns: Composed transform function.
    """
    functions = []

    if crop_area:
        # Add regions domain cropping
        functions = [data_src.crop_area]

    if (modifier is not None) and (not (
            ('stage' in modifier.cfg) and
            (modifier.cfg['stage'] != stage))):
        # Add modifier transformation
        functions.append(modifier.transform)

    # Add other functions
    functions.extend(other_functions)

    return tools.Composer(*functions)
