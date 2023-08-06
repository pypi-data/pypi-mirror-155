"""Linear demand estimator with extraction with heating and cooling days."""
import numpy as np
import pandas as pd
import xarray as xr
from sklearn import linear_model
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.pipeline import Pipeline
import typing as tp
import e4clim
from e4clim.container.gridded_data_source import GriddedDataSourceBase
from e4clim.container.parsing_multi_data_source import (
    ParsingMultiDataSourceBase)
from e4clim.container.result_data_source import Feature
from e4clim.container.strategy import ExtractorBase, EstimatorBase
import e4clim.typing as e4tp
from e4clim.utils.learn import (
    MultiInputRegressor, select_data, get_transform_function)
from e4clim.utils import tools

#: Share of tolerated NaNs.
TOL_NANS_SHARE: tp.Final[float] = 0.01

#: Method to fill NaNs.
FILL_NANS_METHOD: tp.Final[str] = 'ffill'


class Strategy(ExtractorBase, EstimatorBase):
    #: Default result name.
    DEFAULT_RESULT_NAME: tp.Final[str] = 'demand'

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        if parent.result_name != self.DEFAULT_RESULT_NAME:
            self.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    parent.result_name, self.DEFAULT_RESULT_NAME,
                    self.name))

        #: Climate-variable name.
        self.climate_variable: str = 'surface_temperature'
        #: Calendar-variable name.
        self.calendar_variable: str = 'calendar'

        # Initialize extractor and transformer
        super(Strategy, self).__init__(
            parent=parent, name=name, cfg=cfg,
            variable_names={self.climate_variable, self.calendar_variable},
            **kwargs)

        self.coef = {
            'daily_cycle_mean': None, 'regressor': None,
            'r2': None, 't_heat': None, 't_cool': None, 'alpha': None}

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Format temperature data from climate dataset.

        :param stage: Modeling stage: `'fit'` or `'predict'`.

        :returns: Merged dataset.

        :raises AssertionError: if

            * :py:obj:`stage` argument is not given,
            * stage data source is not :py:class:`ParsingMultiDataSourceBase`,
            * climate data source is not :py:class:`GriddedDataSourceBase`,
            * climate dataset is not :py:class:`xarray.Dataset`.

        """
        assert stage is not None, '"stage" argument is not optional here'

        # Get data sources
        data_src = self.data_sources[stage]
        assert isinstance(data_src, ParsingMultiDataSourceBase), (
            'Data source for "{}" should be "ParsingMultiDataSourceBase"'
            ''.format(stage))

        clim_data_src = data_src.get_single_data_source(
            self.climate_variable)
        assert isinstance(clim_data_src, GriddedDataSourceBase), (
            'Climate data source for "{}" should be "GriddedDataSourceBase"'
            ''.format(stage))

        cal_data_src = data_src.get_single_data_source(
            self.calendar_variable)

        # Download climate data
        variable_component_names: e4tp.VCNStrictType = {
            self.climate_variable: set(self.stage_variable_component_names[
                stage][self.climate_variable])}
        clim_data_src.manage_download(
            variable_component_names=variable_component_names, **kwargs)

        # Functions to apply to the input climate data
        other_functions = [clim_data_src.get_regional_mean]
        transform_function = get_transform_function(
            clim_data_src, stage, other_functions=other_functions,
            modifier=self.parent.modifier)

        # Load climate variable
        ds_clim = clim_data_src.parse_finalize(
            transform=transform_function,
            variable_component_names=variable_component_names)

        assert isinstance(ds_clim, xr.Dataset), (
            'Climate dataset should be "xr.Dataset"')

        # Convert from Kelvin to Celsius
        ds_clim[self.climate_variable] -= 273.15

        # Re-sample the climate data, if needed
        ds_clim = self._resample_data(ds_clim, reducer='mean', **kwargs)

        # Load calendar consistent with climate dataset
        variable_component_names = {
            self.calendar_variable: set(self.stage_variable_component_names[
                stage][self.calendar_variable])}
        ds_cal = cal_data_src.parse_finalize(
            variable_component_names=variable_component_names,
            dates=ds_clim.indexes['time'], area=self.parent.parent.area)

        # Return datasets merge
        return {**ds_clim, **ds_cal}

    def fit(self, data_src_in: Feature, data_src_out: Feature,
            **kwargs) -> None:
        """Learn statistical model of temperature-dependent demand
        and predict demand.

        :param data_src_in: Temperature and calendar dataset of training set.
        :param data_src_out: Demand dataset of training set.

        .. note::
          * This function uses grid search with k-fold cross validation to
            find the best heating/cooling temperature thresholds and
            regularization parameter.
          * These hyper-parameters are the same for all regions,
            so that the model has multiple outputs (one for each region)
            and the score for the cross valideation is given by the
            sum of the individual coefficients of determination for each region
            weighted by the fraction of the total variance explained by each
            region.
          * The feature matrix of the demand model is computed by calling the
            `fit` member function of the class
            :py:class:`DemandFeatureHeatCoolDays`, which itself calls
            the function :py:func:`_get_demand_feature_heat_cool_days`.

        """
        # Select data, regional or not
        place_name = (self.parent.parent.area if self.cfg.get('over_area') else
                      None)
        da_clim = select_data(data_src_in, self.parent,
                              variable_name=self.climate_variable, **kwargs)
        da_cal = select_data(data_src_in, self.parent,
                             variable_name=self.calendar_variable, **kwargs)
        da_dem = select_data(data_src_out, self.parent,
                             place_name=place_name, **kwargs)

        tol_nans_share = tools.get_required_float_entry(
            self.cfg, 'tol_nans_share', TOL_NANS_SHARE)
        fill_nans_method = tools.get_required_str_entry(
            self.cfg, 'fill_nans_method', FILL_NANS_METHOD)
        da_dem = _handle_nans(da_dem, tol_nans_share, fill_nans_method)

        # Resample demand data, if needed
        da_dem = self._resample_data(da_dem, reducer='sum', **kwargs)

        # Average climate data over region if needed
        if self.cfg.get('over_area'):
            da_clim = da_clim.mean('region')

        # Assign variable coordinate
        da_clim = da_clim.expand_dims('variable').assign_coords(
            variable=[self.climate_variable])

        # Get common time index between demand and climate data
        da_clim, da_cal, da_dem = _select_time_slice(
            da_clim, da_cal, da_dem, **kwargs)

        # Get daily cycle mean
        if self.med.cfg['frequency'] == 'hour':
            self.coef['daily_cycle_mean'] = _get_daily_cycle(da_dem, da_cal)

        # Get raw design matrix
        des_mat_cycle = self._get_raw_design_matrix(da_clim, da_cal, **kwargs)

        # Cross-validation configuration
        if 'n_splits' in self.cfg:
            n_splits = self.cfg['n_splits']
        else:
            years = des_mat_cycle.indexes['time'].year
            n_splits = years[-1] - years[0] + 1
        # cv = TimeSeriesSplit(n_splits=self.cfg['n_splits'])
        cv = KFold(n_splits=n_splits)
        # scoring = 'neg_mean_squared_error'

        # Heating and cooling temperature grid
        cfg_t_heat: tp.Mapping[str, float] = tools.get_required_mapping_entry(
            self.cfg, 't_heat')
        t_heat_grid = np.arange(tools.get_required_float_entry(cfg_t_heat, 'start'),
                                tools.get_required_float_entry(
                                    cfg_t_heat, 'stop'),
                                tools.get_required_float_entry(cfg_t_heat, 'step'))
        cfg_t_cool: tp.Mapping[str, float] = tools.get_required_mapping_entry(
            self.cfg, 't_cool')
        t_cool_grid = np.arange(tools.get_required_float_entry(cfg_t_cool, 'start'),
                                tools.get_required_float_entry(
                                    cfg_t_cool, 'stop'),
                                tools.get_required_float_entry(cfg_t_cool, 'step'))

        # Estimator
        grid = {'extractor__t_heat':  t_heat_grid,
                'extractor__t_cool': t_cool_grid}
        params: tp.MutableMapping[str, tp.Union[bool, int]] = {
            'fit_intercept': True}
        max_iter = tools.get_int_entry(self.cfg, 'max_iter')
        if max_iter is not None:
            params['max_iter'] = max_iter
        if ((self.cfg['method'] == 'Ridge')
                | (self.cfg['method'] == 'Lasso')):
            cfg_alpha = tools.get_required_mapping_entry(self.cfg, 'alpha')
            alpha_grid = np.logspace(
                tools.get_required_float_entry(cfg_alpha, 'start'),
                tools.get_required_float_entry(cfg_alpha, 'stop'),
                tools.get_required_float_entry(cfg_alpha, 'step'))
            grid.update({'regressor__estimator__alpha': alpha_grid})
            if self.cfg['method'] == 'Ridge':
                estimator = linear_model.Ridge(**params)
            elif self.cfg['method'] == 'Lasso':
                estimator = linear_model.Lasso(**params)
        elif self.cfg['method'] == 'BayesianRidge':
            estimator = linear_model.BayesianRidge(**params)

        # Make grid estimator
        daytype_index = np.unique(da_cal)
        extractor = DemandFeatureHeatCoolDays(
            daytype_index=daytype_index, with_mean=True, with_std=True)
        regressor = MultiInputRegressor(estimator)
        steps = [('extractor', extractor), ('regressor', regressor)]
        pipe = Pipeline(steps=steps)
        grid_cv = GridSearchCV(pipe, grid, cv=cv, verbose=0)

        # Fit model
        self.info('Fitting model by {}'.format(self.cfg['method']))
        grid_cv.fit(des_mat_cycle.values, da_dem.values)
        self.coef['regressor'], self.coef['r2'] = (
            grid_cv.best_estimator_, grid_cv.best_score_)

        # Get parameters of best model
        params = self.coef['regressor'].get_params()
        self.coef['t_heat'], self.coef['t_cool'] = (
            params['extractor__t_heat'], params['extractor__t_cool'])
        if self.cfg['method'] != 'BayesianRidge':
            self.coef['alpha'] = params['regressor__estimator__alpha']

        # Print parameters and scores
        self.info('Best overall score: {:.2f}'.format(self.coef['r2']))
        self.info('Heating temperature: {:.1f}'.format(self.coef['t_heat']))
        self.info('Cooling temperature: {:.1f}'.format(self.coef['t_cool']))
        if self.cfg['method'] != 'BayesianRidge':
            self.info('Regularization coefficient: {:.1f}'.format(
                self.coef['alpha']))

    def predict(self, data_src_in: Feature, **kwargs) -> e4tp.DatasetType:
        """Get regional demand prediction from fitted model.

        :param data_src_in: Input data source for prediction.

        :returns: Prediction dataset.
        """
        if self.coef['r2'] is None:
            raise NotFittedError(
                'This demand estimator instance has not been fitted yet')

        # Select component and result and reorder regions and coordinates
        da_clim = select_data(data_src_in, self.parent,
                              variable_name=self.climate_variable, **kwargs)
        da_cal = select_data(data_src_in, self.parent,
                             variable_name=self.calendar_variable, **kwargs)

        # Average climate data over region if needed
        if self.cfg.get('over_area'):
            da_clim = da_clim.mean('region')

        # Assign variable coordinate
        da_clim = da_clim.expand_dims('variable').assign_coords(
            variable=[self.climate_variable])

        # Get raw design matrix
        des_mat_cycle = self._get_raw_design_matrix(da_clim, da_cal, **kwargs)

        # Predict
        kwargs = ({'return_std': True} if self.cfg['method'] == 'BayesianRidge'
                  else {})
        pred = self.coef['regressor'].predict(des_mat_cycle.values, **kwargs)

        # Collect regional demand prediction
        ds_pred = xr.Dataset()
        coords = dict(des_mat_cycle.coords)
        coords_new: tp.MutableSequence[tp.Tuple[str, np.ndarray]] = [
            ('time', coords['time'].values)]
        if self.cfg.get('over_area'):
            coords_new += [('region', np.array([self.parent.parent.area]))]
        else:
            coords_new += [('region', coords['region'].values)]
        if self.cfg['method'] == 'BayesianRidge':
            y_mean, y_std = pred
            # Add random perturbations to prediction drawn from
            # posterior distribution
            if self.med.cfg['frequency'] == 'hour':
                # Constant perturbations throughout the day
                y_pert_day = np.random.normal(loc=0., scale=y_std[::24])
                y_pert = np.empty(y_mean.shape)
                for ih in range(24):
                    y_pert[ih::24] = y_pert_day
            elif self.med.cfg['frequency'] == 'day':
                y_pert = np.random.normal(loc=0., scale=y_std)
            prediction = y_mean + y_pert

            # Add mean, standard deviation, alpha and lambda
            # y_mean = xr.DataArray(y_mean, coords=[coord_time, coord_reg],
            #                       name='demand_mean')
            y_std = xr.DataArray(y_std, coords=coords_new, name='demand_std')
        else:
            prediction = pred

        # Add prediction
        prediction = xr.DataArray(prediction, coords=coords_new)
        prediction.attrs['r2_total'] = self.coef['r2']
        prediction.attrs['t_heat'] = self.coef['t_heat']
        prediction.attrs['t_cool'] = self.coef['t_cool']
        if self.cfg['method'] != 'BayesianRidge':
            prediction.attrs['alpha'] = self.coef['alpha']

        # Add units
        if self.med.cfg['frequency'] == 'day':
            prediction.attrs['units'] = 'MWh/d'
        elif self.med.cfg['frequency'] == 'hour':
            prediction.attrs['units'] = 'MWh/h'
        ds_pred[self.parent.result_name] = prediction

        da_clim = des_mat_cycle.loc[{'variable': self.climate_variable}]
        time_per_year = 365.25
        if self.med.cfg['frequency'] == 'hour':
            time_per_year *= 24
        val = prediction.mean('time').values * time_per_year / 1e6
        self.info('Total fitted demand mean (TWh/y): {}'.format(val))
        if self.cfg['method'] == 'BayesianRidge':
            y_std *= time_per_year / 1e6
            val = np.sqrt((y_std**2).mean('time').values)
        self.info('Total fitted demand std (TWh/y): {}'.format(val))
        # Get number of heating and cooling days
        n_heating_days = (da_clim < self.coef['t_heat']).mean(
            'time').values * time_per_year
        n_cooling_days = (da_clim > self.coef['t_cool']).mean(
            'time').values * time_per_year
        self.info('Number of heating days per year: {}'.format(n_heating_days))
        self.info('Number of cooling days per year: {}'.format(n_cooling_days))

        return ds_pred

    def get_extractor_postfix(self, **kwargs) -> str:
        """Get postfix corresponding to wind features.

        returns: Postfix.
        """
        postfix = '{}_{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        return postfix

    def get_estimator_postfix(self, **kwargs) -> str:
        """Get estimator postfix.

        returns: Postfix.
        """
        return '{}_{}'.format(
            super(Strategy, self).get_estimator_postfix(**kwargs),
            self.cfg['method'])

    @tp.overload
    def _resample_data(self, data: xr.Dataset,
                       reducer: str = None, **kwargs) -> xr.Dataset: ...

    @tp.overload
    def _resample_data(self, data: xr.DataArray,
                       reducer: str = None, **kwargs) -> xr.DataArray: ...

    def _resample_data(self, data: e4tp.XArrayDataType,
                       reducer: str = None, **kwargs) -> e4tp.XArrayDataType:
        """Resample dataset, if needed.

        :param data: Data.
        :param reducer: Name of method used to reduce after resampling.

        :returns: Data.
        """
        t = data.indexes['time']
        freq_data = t.inferred_freq
        if freq_data is None:
            if (t[1] - t[0]).seconds // 3600 == 1:
                freq_data = 'H'
        if (('H' in freq_data) and (
                self.med.cfg['frequency'] == 'day')):
            assert reducer is not None, (
                '"reducer" argument required '
                'when reduction from hour to day needed')

            # Resample
            gp = data.resample(time='D')

            # Apply reduction
            meth = getattr(gp, reducer)
            data = meth('time', keep_attrs=True)
        elif (('D' in freq_data) and (
                str(self.med.cfg['frequency']) == 'hour')):
            end_time = data.indexes['time'][-1] + pd.Timedelta(23, unit='H')
            th = pd.date_range(
                start=data.indexes['time'][0], end=end_time, freq='H')
            data = data.reindex(time=th).ffill('time')

        return data

    def _get_raw_design_matrix(
            self, da_clim: xr.DataArray, da_cal: xr.DataArray,
            **kwargs) -> xr.DataArray:
        """Get raw design matrix.

        :param da_clim: Climate-data array.
        :param da_cal: Calendar-data array.

        :returns: Raw design matrix.
        """
        # Apply daily_cycle
        daily_cycle_series = _apply_daily_cycle(
            da_cal, self.coef.get('daily_cycle_mean'),
            str(self.med.cfg['frequency']))

        # Concatenate results and make sure dimensions in right order
        _, daily_cycle_series = xr.broadcast(
            da_clim, daily_cycle_series, exclude=['time', 'variable'])
        des_mat_cycle = xr.concat(
            [da_clim, daily_cycle_series], dim='variable')

        # Transpose available dimensions
        dims = ['time', 'variable']
        dim_reg = 'region'
        if dim_reg in des_mat_cycle.dims:
            dims.append(dim_reg)
        des_mat_cycle = des_mat_cycle.transpose(*dims)

        return des_mat_cycle


class DemandFeatureHeatCoolDays():
    """Class given to a scikit-learn pipeline to extract feature
    of the piecewise-linear_model of demand as a function of
    temperature and type of days."""

    def __init__(self, daytype_index: np.ndarray,
                 t_heat: float = 12., t_cool: float = 18.,
                 with_mean: bool = True, with_std: bool = True) -> None:
        """Constructor.

        :param daytype_index: Day-type index.
        :param t_heat: Heating-temperature threshold.
        :param t_cool: Cooling-temperature threshold.
        :param with_mean: If True, center the data.
        :param with_std: If True, scale the data to unit standard deviation.
        """
        #: Heating-temperature threshold.
        self.t_heat: float = t_heat

        #: Cooling-temperature threshold.
        self.t_cool: float = t_cool

        #: Day-type index.
        self.daytype_index: np.ndarray = daytype_index

        #: If True, center the data.
        self.with_mean = with_mean

        #: If True, scale the data to unit standard deviation.
        self.with_std = with_std

    def fit(self, des_mat: xr.DataArray,
            y=None) -> 'DemandFeatureHeatCoolDays':
        """Fit doing nothing."""
        return self

    def transform(self, des_mat: np.ndarray, **kwargs) -> np.ndarray:
        """Transform by calling :py:func:`_get_demand_feature_heat_cool_days`.

        :param des_mat: Design matrix.

        :returns: Feature matrix.
        """
        return _get_demand_feature_heat_cool_days(
            des_mat, self.daytype_index, self.t_heat, self.t_cool,
            with_mean=self.with_mean, with_std=self.with_std)

    def set_params(self, t_heat: float = None, t_cool: float = None,
                   daytype_index: np.ndarray = None,
                   with_mean: bool = None, with_std: bool = None) -> None:
        """Mimick `set_params` method from scikit-learn.

        .. todo:: Inheritance from scikit-learn was removed due to
          metaclass conflict when generating sphinx doc.
          Find a better solution.
        """
        # Set heating parameter
        if t_heat is not None:
            self.t_heat = t_heat
        # Set cooling parameter
        if t_cool is not None:
            self.t_cool = t_cool
        # Set daytype_index parameter
        if daytype_index is not None:
            self.daytype_index = daytype_index

        # Set centering parameter
        if with_mean is not None:
            self.with_mean = with_mean

        # Set scaling parameter
        if with_std is not None:
            self.with_std = with_std

    def get_params(self, **kwargs) -> dict:
        """Mimick `set_params` method from scikit-learn.

        .. todo:: Inheritance from scikit-learn was removed due to
          metaclass conflict when generating sphinx doc.
          Find a better solution.
        """
        return {'t_heat': self.t_heat, 't_cool': self.t_cool,
                'daytype_index': self.daytype_index,
                'with_mean': self.with_mean, 'with_std': self.with_std}


def _get_demand_feature_heat_cool_days(
        des_mat: np.ndarray, daytype_index: np.ndarray,
        t_heat: float, t_cool: float,
        with_mean: bool = True, with_std: bool = True) -> np.ndarray:
    """Get feature matrix of demand model with as variables heating
    and cooling temperature ramps and as factors week-days types.

    :param des_mat: Array containing climatic variables, i.e.
        mean temperature(Celsius),
        and membership of days to types 'work', 'sat' and 'off'
        (possibly including a daily cycle).
    :param daytype_index: Daytype index.
    :param t_heat: Temperature threshold below which consumers
        turn on heating.
    :param t_cool: Temperature threshold above which consumers
        turn on air conditionning.
    :param with_mean: If True, center the data.
    :param with_std: If True, scale the data to unit standard deviation.

    :returns: Feature matrix.
    """
    temp_label = 'surface_temperature'
    # Get number of variables (3 linear pieces times number of days)
    n_pieces = 2
    src_variables = daytype_index.tolist()
    src_variables.insert(0, temp_label)
    len_variables = n_pieces * len(daytype_index)

    # Build feature array
    shape = list(des_mat.shape)
    shape[1] = len_variables
    features = np.zeros(shape)

    # Select temperature
    z = des_mat[:, 0]

    for iday, day in enumerate(daytype_index):
        # Day type mask
        id_day = des_mat[:, src_variables.index(day)]

        # Heating temperature
        features[:, 0 + n_pieces * iday] = (
            t_heat - z) * np.heaviside(t_heat - z, 0.) * id_day
        # (z < t_heat).astype(float))

        # Cooling temperature
        features[:, 1 + n_pieces * iday] = (
            z - t_cool) * np.heaviside(z - t_cool, 0.) * id_day
        # (z > t_cool).astype(float)

    # Standardize
    if with_mean:
        features -= features.mean(0)
    if with_std:
        features /= features.std(0)

    return features


def _get_daily_cycle(
        da_dem: xr.DataArray, da_cal: xr.DataArray) -> xr.DataArray:
    """Build an array of complementary columns corresponding
    to each day type of the calendar.
    Non-zero values are given by a composite hourly cycle given by
    the average of demand over all samples of same day type and hour.

    :param da_dem: Demand array.
    :param da_cal: Calendar array.

    :returns: Array with each column corresponding to a day type.
    """
    # Group by day type, and hour if needed
    hours = da_cal.indexes['time'].hour
    hours.name = 'hour'
    group_index = pd.MultiIndex.from_arrays(
        [da_cal.to_index().rename('daytype'), hours])
    da_dem.coords['daytype_hour'] = ('time', group_index)
    gp_daily_cycle = da_dem.groupby('daytype_hour')

    # Get time-mean daily cycle per day type
    daily_cycle_mean = gp_daily_cycle.mean('time')

    return daily_cycle_mean


def _apply_daily_cycle(
        da_cal: xr.DataArray, daily_cycle_mean: xr.DataArray = None,
        frequency: str = 'day') -> xr.DataArray:
    """Build an array of complementary columns corresponding
    to each day type of the calendar. If frequency is `'day'`,
    non-zero values are unitary, else, if frequency is `'hour'`,
    non-zero values are given by a composite hourly cycle given by
    the average of demand over all samples of same day type and hour.

    :param da_cal: Calendar array.
    :param daily_cycle_mean: Mean daily cycle of output data.
    :param frequency: Sampling frequency as either `'day'` or `'hour'`.

    :returns: An array with each column corresponding to a day type.
    """
    # Initialize cycle
    time = da_cal.indexes['time']
    daytype_index = np.unique(da_cal)
    coords = [('time', time), ('variable', daytype_index)]
    daily_cycle_series = xr.DataArray(
        np.zeros((len(time), len(daytype_index))), coords=coords)

    # Group by day type, and hour if needed
    if frequency == 'hour':
        hours = time.hour
        hours.name = 'hour'
        grouper = 'daytype_hour'
        group_index = pd.MultiIndex.from_arrays(
            [da_cal.to_index().rename('daytype'), hours])
        daily_cycle_series.coords[grouper] = ('time', group_index)

        # Group calendar by daytype and hours
        gp_out = daily_cycle_series.groupby(grouper)

        # Fill cycle with composite
        daily_cycle_series = gp_out + daily_cycle_mean

        # Drop group variable
        daily_cycle_series = daily_cycle_series.drop_vars(grouper)
    elif frequency == 'day':
        # Group calendar by daytype
        gp_out = daily_cycle_series.groupby(da_cal)
        for gp_key, gp_idx in gp_out.groups.items():
            daily_cycle_series.loc[{'variable': gp_key}][gp_idx] = 1

    return daily_cycle_series


def _select_time_slice(
        da_clim: xr.DataArray, da_cal: xr.DataArray,
        da_dem: xr.DataArray, **kwargs) -> tp.Tuple[
            xr.DataArray, xr.DataArray, xr.DataArray]:
    """Select time slice from common index.

    :param da_clim: Climate data array.
    :param da_cal: Calendar data array.
    :param da_dem: Demand data array.

    :returns: Time-sliced data.
    """
    time = da_dem.indexes['time']
    time = time.intersection(da_clim.indexes['time'])

    # Select time slice
    da_clim = da_clim.sel(time=time)
    da_cal = da_cal.sel(time=time)
    da_dem = da_dem.sel(time=time)

    return da_clim, da_cal, da_dem


def _handle_nans(da: xr.DataArray, tol_nans_share: float,
                 method: str) -> xr.DataArray:
    """Fill NaNs in array if not too many of them.

    :param da: Array.
    :param tol_nans_share: Allowed share of NaNs in array.
    :param method: Method to fill NaNs.

    :returns: Cleaned array.

    :raises RuntimeError: if more NaNs are found than allowed by
      :py:obj:`tol_nans_share`.
    """
    nans_share = da.isnull().sum() / da.size

    if nans_share > tol_nans_share:
        raise RuntimeError('Too many NaNs in data')

    return getattr(da, method)(dim='time')
