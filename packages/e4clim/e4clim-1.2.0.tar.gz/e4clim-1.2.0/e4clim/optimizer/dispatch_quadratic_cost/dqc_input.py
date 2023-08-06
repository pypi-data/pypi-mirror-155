from collections import OrderedDict
from orderedset import OrderedSet
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.optimizer_data_source import OptimizerInputBase
from e4clim.container.parsing_data_source import ParsingDataSourceBase
import e4clim.typing as e4tp
from e4clim.utils.logging import LoggingContext
from e4clim.utils.optimization_support import (
    OptimizerInputComponentsParserMixin)
from e4clim.utils import tools


#: Float or dataarray type.
FloatArrayType = tp.Union[float, xr.DataArray]

#: Year to hour conversion constant.
YEAR_TO_HOUR = 365.25 * 24
#: Numerical accuracy tolerance.
TOL = 1.e-8


def _x2(x: FloatArrayType, *args) -> FloatArrayType:
    """Polynomial with a second-degree term only.

    :param x: Variable.

    :returns: Term value.
    """
    return args[0] * x**2


def _diff_x2(x: FloatArrayType, *args) -> FloatArrayType:
    """Derivative of a polynomial with a second-degree term only.

    :param x: Variable.

    :returns: Derivative value.
    """
    return 2 * args[0] * x


#: Variable-cost function of dispatchable generation.
GET_DISPATCH_VARIABLE_COST = _x2

#: Marginal-cost function of dispatchable generation.
GET_DISPATCH_MARGINAL_COST = _diff_x2


class Input(OptimizerInputBase, OptimizerInputComponentsParserMixin):
    """Optimization problem input data source."""

    #: Capacity factors.
    capacityfactor: pd.core.generic.NDFrame

    #: Demand.
    demand: pd.core.generic.NDFrame

    #: Load duration curve.
    ldc: xr.DataArray

    #: Region index.
    region: pd.Index
    #: Time index (value set after load).
    _time: pd.Index
    #: VRE components index.
    vre: pd.Index

    #: Value of Lost Load
    voll: float

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextSingleOptimizer',
                 **kwargs) -> None:
        """Initialize input data source.

        :param parent: Optimizer context.
        """
        super(Input, self).__init__(parent, **kwargs)

        self.reset()

    @property
    def time(self) -> pd.DatetimeIndex:
        if self._time is None:
            # Set time index
            self._time = self.capacityfactor.index.levels[-1]

        return self._time

    @time.setter
    def time(self, value: pd.DatetimeIndex) -> None:
        self._time = value

    def reset(self) -> None:
        """Reset."""
        self._time = None

        self._init_components()

        reader_variable_names = self._init_variables()

        self._init_indices()

        self._init_reader(reader_variable_names)

    def _init_components(self) -> None:
        """Initialize components.

        :raises AssertionError: if component-context name in
          :py:attr:`cfg` attribute is not :py:class:`str`.
        """
        cfg_component = tools.get_required_mapping_entry(self.cfg, 'component')
        demand_component_name = tools.get_required_str_entry(
            cfg_component, 'demand')
        self.context_component_demand = self.med.context_components[
            demand_component_name]

        self.context_component_generation = OrderedDict()
        self.component_generation_names = set()

        # Add generation components
        cfg_cf = self.cfg['component']
        cfg_cf_safe = tools.get_required_iterable_str_entry(
            cfg_cf, 'capacityfactor', OrderedSet)

        for context_component_name in cfg_cf_safe:
            assert isinstance(context_component_name, str), (
                'Component-context name in "cfg" attribute '
                'should be "str"')
            context_component = self.med.context_components[
                context_component_name]
            self.context_component_generation[
                context_component_name] = context_component
            self.component_generation_names.add(
                context_component.component_name)

    def _init_variables(self) -> tp.Set:
        """Initialize input variables and return names of variables to read.

        :returns: Names of variables to read.
        """
        self.update_variables(
            {'capacityfactor', 'mean_capacityfactor', 'demand',
             'hourly_rental_cost', 'ldc', 'ccdf'})

        # Add variable for maximum-capacity constraint
        reader_variable_names = set()
        variable_name = 'capacity_max'
        # if self.optimizer.cfg['constraint'][variable_name]:
        self.update_variables({variable_name})
        reader_variable_names.add(variable_name)

        return reader_variable_names

    def _init_indices(self) -> None:
        """Initialize indices."""
        self.vre = pd.Index(
            [context_component.component_name for context_component in (
                self.context_component_generation.values())])

        context_component_names = list(self.context_component_generation)

        self.region = pd.Index(self.context_component_generation[
            context_component_names[0]].place_names)

    def _init_reader(self, variable_names: tp.Set) -> None:
        """Initialize CSV reader data source.

        :param variable_names: Names of variables to read.
        """
        variable_component_names = self._get_reader_variable_component_names(
            variable_names)

        self.med.build_data_source({'reader': variable_component_names},
                                   parent=self)

    def _get_reader_variable_component_names(
            self, variable_names: tp.Set) -> dict:
        """Get variable to component names mapping for variables to read.

        :param variable_names: Variable names.

        :returns: Variable to component names.
        """
        variable_component_names = {}
        for variable_name in variable_names:
            variable_component_names.update({
                variable_name:
                list(self.component_generation_names)})

        return variable_component_names

    def download(self, *args, **kwargs) -> None:
        """Not implemented."""
        self.warning('{} download not implemented'.format(self.name))

        return None

    def parse(self, *args, **kwargs) -> e4tp.DatasetType:
        """Parse optimization problem input data."""
        ds = self.parse_available_components(regional=True, **kwargs)

        self._add_noncomponent_data(ds)

        ds['mean_capacityfactor'] = ds['capacityfactor'].unstack().mean('columns')

        ds['hourly_rental_cost'] = self.get_hourly_rental_costs()

        ds['ldc'] = self.get_load_duration_curve(ds['demand'])

        ds['ccdf'] = get_complementary_cdf(ds['ldc'])

        return ds

    def get_data_callback(self, *args, **kwargs) -> None:
        """Add inputs as attributes."""
        self.capacityfactor = tools.get_frame_safe(self.data, 'capacityfactor')
        self.mean_capacityfactor = tools.get_frame_safe(
            self.data, 'mean_capacityfactor')

        self.ccdf = tools.get_array_safe(self.data, 'ccdf')
        self.demand = tools.get_frame_safe(self.data, 'demand')
        self.ldc = tools.get_array_safe(self.data, 'ldc')

        self.hourly_rental_cost = tools.get_frame_safe(
            self.data, 'hourly_rental_cost')

        self.voll = tools.get_required_float_entry(self.cfg, 'voll')

    def _add_noncomponent_data(self, ds: tp.MutableMapping[
            str, pd.DataFrame]) -> None:
        """Add noncomponent data read with reader data source to dataset.

        :param ds: Dataset to update.

        :raises AssertionError: if `'reader'` data source in
          :py:obj:`data_sources` attribute of :py:attr:`med` attribute is not
          :py:class:`e4clim.container.parsing_data_source.ParsingDataSourceBase`.
        """
        data_src = self.med.data_sources['reader']

        assert isinstance(data_src, ParsingDataSourceBase)

        ds.update(data_src.get_data())

    def _add_novre_diagnostics_for_this_param(
            self, param: float, ds: xr.Dataset) -> xr.Dataset:
        """Add diagnostics without VRE to dataset.

        :param param: Quadratic cost-function coefficient.
        :param ds: Solution dataset.

        :returns: Dataset with diagnostics without VRE.
        """
        if 'dispatch_generation_max_novre' not in ds:
            ds['dispatch_generation_max_novre'] = (
                self.get_dispatch_generation_max_novre(param))
        dgmn = float(ds['dispatch_generation_max_novre'])
        ds['dispatch_generation_novre'] = self.get_dispatch_generation_novre(
            dispatch_generation_max_novre=dgmn)
        ds['lost_load_novre'] = self.get_lost_load_novre(
            dispatch_generation_max_novre=dgmn)
        ds['system_marginal_cost_novre'] = self.get_system_marginal_cost_novre(
            param, ds['dispatch_generation_novre'], ds['lost_load_novre'])
        ds['mean_dispatch_variable_cost_novre'] = (
            _get_mean_dispatch_variable_cost(
                param, ds['dispatch_generation_novre']))
        mdvcn = float(ds['mean_dispatch_variable_cost_novre'])
        ds['dispatch_fixed_cost_novre'] = _get_dispatch_fixed_cost(
            param, ds['dispatch_generation_novre'], dgmn, self.cfg)
        ds['mean_lost_load_cost_novre'] = _get_mean_lost_load_cost(
            ds['lost_load_novre'], self.voll)
        ds['mean_dispatch_total_cost_novre'] = _get_mean_dispatch_total_cost(
            param, self.cfg, mean_dispatch_variable_cost=mdvcn,
            dispatch_fixed_cost=float(ds['dispatch_fixed_cost_novre']))
        ds['mean_system_total_cost_novre'] = _get_mean_system_total_cost_novre(
            param, self.cfg, self.voll, mean_dispatch_total_cost=float(
                ds['mean_dispatch_total_cost_novre']),
            mean_lost_load_cost=float(ds['mean_lost_load_cost_novre']))
        ds['mean_dispatch_revenue_novre'] = _get_mean_dispatch_revenue(
            ds['dispatch_generation_novre'], ds['system_marginal_cost_novre'])
        ds['lcoe_plant'] = xr.DataArray(
            self.get_lcoe_plant()).rename(vre='component')

        return ds

    def get_system_marginal_cost_novre(
            self, alpha: float,
            dispatch_generation_novre: xr.DataArray = None,
            lost_load_novre: xr.DataArray = None,
            dispatch_generation_max_novre: float = None) -> xr.DataArray:
        """Get system cost time series.

        :param alpha: Quadratic cost-function coefficient.
        :param dispatch_generation_novre: Dispatchable generation.
          If `None`, it is computed.
        :param lost_load_novre: Lost load. If `None`, it is computed.
        :param dispatch_generation_max_novre: Maximum dispatchable generation.
          If `None`, it is computed.

        :returns: System cost.
        """
        if dispatch_generation_novre is None:
            dispatch_generation_novre = self.get_dispatch_generation_novre(
                alpha=alpha,
                dispatch_generation_max_novre=dispatch_generation_max_novre)
        if lost_load_novre is None:
            lost_load_novre = self.get_lost_load_novre(
                alpha=alpha,
                dispatch_generation_max_novre=dispatch_generation_max_novre)

        system_marginal_cost_novre = _get_system_marginal_cost(
            alpha, dispatch_generation_novre, lost_load_novre, self.voll)

        return system_marginal_cost_novre

    def get_lost_load_novre(
            self, alpha: float = None,
            dispatch_generation_max_novre: float = None) -> xr.DataArray:
        """Get lost load without VRE.

        :param alpha: Quadratic cost-function coefficient.
          If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
        :param dispatch_generation_max_novre: Maximum dispatchable generation.
          If `None`, it is computed for :py:obj:`alpha`.

        :returns: Lost load without VRE.
        """
        assert ((alpha is not None) or (
            dispatch_generation_max_novre is not None)), (
            'Either "alpha" or "dispatch_generation_max_novre"'
            'should be given.')

        if dispatch_generation_max_novre is None:
            dispatch_generation_max_novre = (
                self.get_dispatch_generation_max_novre(alpha))

        coords = [('time', self.demand.index)]
        load = xr.DataArray(self.demand, coords=coords)
        lost_load_novre = _get_lost_load(load, dispatch_generation_max_novre)

        return lost_load_novre

    def get_dispatch_generation_novre(
            self, alpha: float = None,
            dispatch_generation_max_novre: float = None) -> xr.DataArray:
        """Get dispatchable generation without VRE.

        :param alpha: Quadratic cost-function coefficient.
          If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
        :param dispatch_generation_max_novre: Maximum dispatchable generation.
          If `None`, it is computed for :py:obj:`alpha`.

        :returns: Dispatchable generation without VRE.
        """
        assert ((alpha is not None) or (
            dispatch_generation_max_novre is not None)), (
            'Either "alpha" or "dispatch_generation_max_novre"'
                'should be given.')

        if dispatch_generation_max_novre is None:
            dispatch_generation_max_novre = (
                self.get_dispatch_generation_max_novre(alpha))

        # Get dispatchable generation
        coords = [('time', self.demand.index)]
        load = xr.DataArray(self.demand, coords=coords)
        dispatch_generation_novre = _get_dispatch_generation(
            load, dispatch_generation_max_novre)

        return dispatch_generation_novre

    def get_dispatch_generation_max_novre(
            self, alpha: float = None, lole_novre: float = None) -> float:
        """Get maximum dispatchable generation depending on
        `dispatch_generation_max_novre` entry in configuration:

          * `'max'`: from maximum load
          * `'lole'`: from LoLE given as argument or computed from VoLL
          * :py:class:`float`: from the given float value in MW.

        :param alpha: Quadratic cost-function coefficient.
          If `None`, :py:obj:`lole_novre` should be given.
        :param lole_novre: Loss of Load Expectation over the period
          without VRE. If `None`, it is computed.

        :returns: Maximum dispatchable generation.

        :raises ValueError: If `dispatch_generation_max_novre` not 
          `'max'`, `'lole'`, `None` or a :py:class:`float`.
        """
        try:
            dgm_type = tools.get_required_str_entry(
                self.cfg, 'dispatch_generation_max_novre', 'max')
        except AssertionError:
            dgm_type = 'value'
            dgm_value = tools.get_required_float_entry(
                self.cfg, 'dispatch_generation_max_novre')

        if dgm_type == 'max':
            # From maximum load
            dispatch_generation_max_novre = (
                self.get_dispatch_generation_max_novre_from_lole(alpha, 0))
        elif dgm_type == 'lole':
            # From LoLE
            dispatch_generation_max_novre = (
                self.get_dispatch_generation_max_novre_from_lole(
                    alpha, lole_novre))
        elif dgm_type == 'value':
            dispatch_generation_max_novre = dgm_value
        else:
            raise ValueError('"dispatch_generation_max_novre" entry in '
                             'optimizer-input configuration should be '
                             '"max", "lole", None or a float')

        return dispatch_generation_max_novre

    def get_dispatch_generation_max_novre_from_lole(
            self, alpha: float = None, lole_novre: float = None) -> float:
        """Get maximum dispatchable generation from the LoLE
        for a given quadratic cost-function coefficient.

        :param alpha: Quadratic cost-function coefficient.
          If `None`, :py:obj:`lole_novre` should be given.
        :param lole_novre: Loss of Load Expectation over the period
          without VRE. If `None`, it is computed.

        :returns: Maximum dispatchable generation.
        """
        if lole_novre is None:
            assert (alpha is not None), (
                '"alpha" argument should be given when "lole_novre" is not.')

            lole_novre = get_lole(alpha, self.ldc, self.voll, self.cfg)

        dispatch_generation_max_novre = float(self.ldc[lole_novre])

        return dispatch_generation_max_novre

    def get_lcoe_plant(self) -> pd.Series:
        """Get Levelized Cost of Electricity per plant.

        :returns: Levelized Cost of Electricity per plant.
        """
        cf_mean = self.capacityfactor.unstack().mean(
            'columns').unstack()
        hrc = pd.concat([self.hourly_rental_cost.to_frame(name=region_name)
                         for region_name in cf_mean.columns],
                        axis='columns')
        hrc.index.name = cf_mean.index.name
        hrc.columns.name = cf_mean.columns.name
        lcoe = hrc / cf_mean

        return lcoe

    def get_hourly_rental_costs(self) -> pd.Series:
        """Get hourly rental costs.

        :returns: Hourly rental costs.
        """
        index = pd.Index(self.component_generation_names)
        index.name = 'component'

        data = [_get_hourly_rental_cost_for_component(
            component_name, self.cfg) for component_name in index]

        return pd.Series(data, index=index)

    def get_load_duration_curve(self, demand: pd.Series) -> xr.DataArray:
        """Get Load Duration Curve (LDC).

        :param demand: Demand.

        :returns: Load duration curve.

        .. warning:: To fasten indexing using integers, the LDC is indexed by
          the number of hours in the time series, rather than indexing by
          probabilities or by the floating hours in a year.
          For instance, a two-year long series results in hours from 1 to
          17520.
        """
        peak_hour = np.arange(len(demand.index)) + 1
        coord_hour = ('peak_hour', peak_hour)
        peak_demand = demand.sort_values(ascending=False).values
        ldc = xr.DataArray(peak_demand, coords=[coord_hour])

        return ldc

    def get_costs_dispatch_distribution_for_alpha(
            self, alpha: float, ds: xr.Dataset,
            loadpoints: tp.Sequence) -> xr.Dataset:
        """Get marginal and rental costs for distribution of dispatchable
        producers.

        :param alpha: Quadratic cost-function coefficient.
        :param ds: Solution dataset.
        :param loadpoints: load points.

        :returns: Dispatch-distribution dataset.
        """
        lp = xr.DataArray(loadpoints, coords=[('loadpoint', loadpoints)])
        marginal_cost = tp.cast(
            xr.DataArray, GET_DISPATCH_MARGINAL_COST(lp, alpha))

        # Get utilizations
        rental_cost = xr.ones_like(marginal_cost) * np.nan
        utilization_novre = xr.ones_like(marginal_cost) * np.nan
        for iel, loadpoint in enumerate(loadpoints):
            utilization_novre[{'loadpoint': iel}], _ = (
                _get_utilization_at_loadpoint(loadpoint, self.ccdf))

        # Get rental cost for highest loadpoint
        peak_rental_cost = _get_hourly_rental_cost_for_component(
            'peak', self.cfg)
        peak_marginal_cost = GET_DISPATCH_MARGINAL_COST(
            ds['dispatch_generation_max_novre'], alpha)
        rental_cost[-1] = peak_rental_cost + (
            tp.cast(xr.DataArray, peak_marginal_cost)
            - marginal_cost[-1]) * utilization_novre[-1]

        # Get other rental costs
        for iel, loadpoint in list(enumerate(loadpoints[:-1]))[::-1]:
            rental_cost[iel] = rental_cost[iel + 1] + (
                marginal_cost[iel + 1] - marginal_cost[iel]) * (
                    utilization_novre[iel])

        ds_dis = xr.Dataset(
            {'marginal_cost': marginal_cost, 'rental_cost': rental_cost,
             'utilization_novre': utilization_novre})
        ds_dis = ds_dis.expand_dims('alpha').assign_coords(alpha=[alpha])

        return ds_dis

    def get_data_postfix(self, **kwargs) -> str:
        """Get data postfix.

        :returns: Postfix.
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get standard postfix
            postfix_list = []

            # Demand postfix
            postfix_list.append(self.context_component_demand['demand'].
                                get_data_postfix(**kwargs).split('_'))

            # Capacity factors postfix
            for context_component in (
                    self.context_component_generation.values()):
                postfix_list.append(context_component['capacityfactor'].
                                    get_data_postfix(**kwargs).split('_'))

            # Join postfixes
            postfix_list = np.concatenate(postfix)
            _, idx = np.unique(postfix_list, return_index=True)
            postfix_safe = '_'.join(postfix_list[np.sort(idx)])

            # Add period
            if self.cfg.get('select_period'):
                postfix_safe += '_{}-{}'.format(
                    self._start_date.date().strftime('%Y%m%d'),
                    self._end_date.date().strftime('%Y%m%d'))
        else:
            postfix_safe = str(postfix)

        return postfix_safe


def _get_mean_system_total_cost_novre(
        alpha: float, cfg: e4tp.CfgType, voll: float,
        dispatch_generation: xr.DataArray = None,
        lost_load: xr.DataArray = None,
        dispatch_generation_max_novre: float = None,
        mean_dispatch_variable_cost: float = None,
        dispatch_fixed_cost: float = None,
        mean_lost_load_cost: float = None,
        mean_dispatch_total_cost: float = None,
        demand: pd.Series = None, problem: str = 'variable') -> float:
    """Get mean system total cost without VRE (dispatch and lost load).

    :param alpha: Quadratic cost-function coefficient.
    :param cfg: Input configuration.
    :param voll: Value of Lost Load.
    :param dispatch_generation: Dispatchable generation.
      If `None`, :py:obj:`mean_dispatch_variable_cost`
      and :py:obj:`dispatch_fixed_cost` should be given.
    :param lost_load: Lost load.
      If `None`, :py:obj:`mean_lost_load_cost` should be given.
    :param dispatch_generation_max_novre: Maximum dispatchable generation.
      If `None`, :py:obj:`dispatch_fixed_cost` should be given.
    :param mean_dispatch_variable_cost: Dispatch variable cost.
      If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
    :param dispatch_fixed_cost: Dispatch fixed cost.
      If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
    :param mean_lost_load_cost: Lost-load cost.
      If `None`, :py:obj:`lost_load` should be given.
    :param mean_dispatch_total_cost: Dispatch total cost.
      If `None`, other arguments should be given to compute it.
    :param demand: Demand.
      Should not be `None` if :py:obj:`problem` equals `'decoupled'`.
    :param problem: Optimization-problem type.

    :returns: Mean system total cost for problem.

    :raises AssertionError: if :py:obj:`problem` not in
      `['variable', 'constant', 'decoupled']`.
    """
    assert problem in ['variable', 'constant', 'decoupled'], (
        '"problem" argument not in ["variable", "constant", "decoupled"]')

    if mean_dispatch_total_cost is None:
        mean_dispatch_total_cost = _get_mean_dispatch_total_cost(
            alpha, cfg, dispatch_generation=dispatch_generation,
            dispatch_generation_max_novre=dispatch_generation_max_novre,
            mean_dispatch_variable_cost=mean_dispatch_variable_cost,
            dispatch_fixed_cost=dispatch_fixed_cost,
            demand=demand, problem=problem)

    if problem == 'variable':
        if mean_lost_load_cost is None:
            assert (lost_load is not None), (
                '"lost_load" argument should be given when'
                '"mean_lost_load_cost" is not.')
            mean_lost_load_cost = _get_mean_lost_load_cost(lost_load, voll)
    else:
        mean_lost_load_cost = 0.

    mean_system_total_cost = mean_dispatch_total_cost + mean_lost_load_cost

    return mean_system_total_cost


def _get_mean_dispatch_total_cost(
        alpha: float, cfg: e4tp.CfgType,
        dispatch_generation: xr.DataArray = None,
        dispatch_generation_max_novre: float = None,
        mean_dispatch_variable_cost: float = None,
        dispatch_fixed_cost: float = None,
        demand: pd.Series = None,
        problem: str = 'variable') -> float:
    """Get mean dispatch total cost (rental, variable and lost-load costs).

    :param alpha: Quadratic cost-function coefficient.
    :param cfg: Input configuration.
    :param dispatch_generation: Dispatchable generation.
      If `None`, :py:obj:`mean_dispatch_variable_cost`
      and :py:obj:`dispatch_fixed_cost` should be given.
    :param dispatch_generation_max_novre: Maximum dispatchable generation.
      If `None`, :py:obj:`dispatch_fixed_cost` should be given.
    :param mean_dispatch_variable_cost: Dispatch variable cost.
      If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
    :param dispatch_fixed_cost: Dispatch fixed cost.
      If `None`, :py:obj:`dispatch_generation_max_novre` should be given.
    :param demand: Demand.
      Should not be `None` if :py:obj:`problem` equals `'decoupled'`.
    :param problem: Optimization-problem type.

    :raises AssertionError: if :py:obj:`problem` not in
      `['variable', 'constant', 'decoupled']`.
    :returns: Mean dispatch total cost.
    """
    assert problem in ['variable', 'constant', 'decoupled'], (
        '"problem" argument not in ["variable", "constant", "decoupled"]')

    if mean_dispatch_variable_cost is None:
        assert (dispatch_generation is not None), (
            '"dispatch_generation" argument should be given when '
            '"mean_dispatch_variable_cost" is not')
        mean_dispatch_variable_cost = _get_mean_dispatch_variable_cost(
            alpha, dispatch_generation, demand=demand, problem=problem)

    if dispatch_fixed_cost is None:
        assert (dispatch_generation is not None), (
            '"dispatch_generation" argument should be given when '
            '"dispatch_fixed_cost" is not')
        assert (dispatch_generation_max_novre is not None), (
            '"dispatch_generation_max_novre" argument should be given when '
            '"dispatch_fixed_cost" is not')
        dispatch_fixed_cost = _get_dispatch_fixed_cost(
            alpha, dispatch_generation, dispatch_generation_max_novre, cfg)

    mean_dispatch_total_cost = (mean_dispatch_variable_cost +
                                dispatch_fixed_cost)

    return mean_dispatch_total_cost


def _get_dispatch_fixed_cost(
        alpha: float, dispatch_generation: xr.DataArray,
        dispatch_generation_max_novre: float,
        cfg: e4tp.CfgType) -> float:
    """Get yearly dispatch fixed cost from necessary condition of optimal
    mix of dispatchable producers for quadratic dispatch variable costs.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.
    :param dispatch_generation_max_novre: Maximum dispatchable generation.

    :returns: Dispatch fixed cost.

    .. warning:: This computation is only valid for quadratic dispatch
      variable costs.
    """
    # Dispatch yearly rental cost of peak plant
    peak_rental_cost = _get_hourly_rental_cost_for_component(
        'peak', cfg) * YEAR_TO_HOUR

    # Remaining yearly rental cost
    rem_rental_cost = _get_mean_dispatch_variable_cost(
        alpha, dispatch_generation)

    return (rem_rental_cost +
            peak_rental_cost * dispatch_generation_max_novre)


def _get_mean_dispatch_variable_cost(
        alpha: float, dispatch_generation: xr.DataArray,
        demand: pd.Series = None, problem: str = 'variable') -> float:
    """Get mean yearly dispatch variable cost.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.
    :param demand: Demand.
      Should not be `None` if :py:obj:`problem` equals `'decoupled'`.
    :param problem: Optimization-problem type.

    :returns: Mean yearly dispatch variable cost.

    :raises AssertionError: if :py:obj:`problem` not in
      `['variable', 'constant', 'decoupled']`.
    """
    assert problem in ['variable', 'constant', 'decoupled'], (
        '"problem" argument not in ["variable", "constant", "decoupled"]')

    if problem == 'variable':
        mean_dispatch_variable_cost = (
            _get_variable_mean_dispatch_variable_cost(alpha, dispatch_generation))
    elif problem == 'constant':
        mean_dispatch_variable_cost = (
            _get_constant_mean_dispatch_variable_cost(alpha, dispatch_generation))
    elif problem == 'decoupled':
        assert demand is not None, ('"demand" required when "problem" '
                                    'equals "decoupled"')
        mean_dispatch_variable_cost = (
            _get_decoupled_mean_dispatch_variable_cost(
                alpha, dispatch_generation, demand))

    return mean_dispatch_variable_cost * YEAR_TO_HOUR


def _get_variable_mean_dispatch_variable_cost(
        alpha: float, dispatch_generation: xr.DataArray) -> float:
    """Get variable version of mean yearly dispatch variable cost.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.

    :returns: Mean yearly dispatch variable cost.
    """
    mean_dispatch_variable_cost = tp.cast(
        xr.DataArray, GET_DISPATCH_VARIABLE_COST(
            dispatch_generation, alpha)).mean('time')

    return mean_dispatch_variable_cost


def _get_constant_mean_dispatch_variable_cost(
        alpha: float, dispatch_generation: xr.DataArray) -> float:
    """Get constant version of mean yearly dispatch variable cost.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.

    :returns: Mean yearly dispatch variable cost.
    """
    mean_dispatch_variable_cost = GET_DISPATCH_VARIABLE_COST(
        tp.cast(xr.DataArray, dispatch_generation).mean('time'),
        alpha)

    return float(mean_dispatch_variable_cost)


def _get_decoupled_mean_dispatch_variable_cost(
        alpha: float, dispatch_generation: xr.DataArray,
        demand: pd.Series) -> float:
    """Get decoupled version of mean yearly dispatch variable cost.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.
    :param demand: Demand.

    :returns: Mean yearly dispatch variable cost.
    """
    mean_dispatch_variable_cost = tp.cast(
        xr.DataArray, GET_DISPATCH_VARIABLE_COST(
            dispatch_generation, alpha)).mean('time')
    decoupled_smc = _get_decoupled_system_marginal_cost(alpha, demand)
    mean_dispatch_variable_cost = (decoupled_smc *
                                   dispatch_generation.mean('time'))

    return mean_dispatch_variable_cost


def _get_system_marginal_cost(
        alpha: float, dispatch_generation: xr.DataArray,
        lost_load: xr.DataArray, voll: float) -> xr.DataArray:
    """Get variable-problem system marginal cost time series.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_generation: Dispatchable generation.
    :param lost_load: Lost load.
    :param voll: Value of Lost Load.

    :returns: System cost.
    """
    marginal_cost = GET_DISPATCH_MARGINAL_COST(dispatch_generation, alpha)

    system_marginal_cost = xr.where(lost_load > 0, voll, marginal_cost)

    return system_marginal_cost


def _get_constant_system_marginal_cost(
        alpha: float, dispatch_generation: xr.DataArray) -> float:
    """Get constant-problem system marginal cost.

    :param alpha: Quadratic cost-function coefficient.
    :param dispatch_geneartion: Dispatchable generation.

    :returns: System marginal cost.
    """
    system_marginal_cost = GET_DISPATCH_MARGINAL_COST(
        tp.cast(xr.DataArray, dispatch_generation).mean('time'), alpha)

    return float(system_marginal_cost)


def _get_decoupled_system_marginal_cost(
        alpha: float, demand: pd.Series) -> xr.DataArray:
    """Get decoupled-problem system-marginal cost.

    :param alpha: Quadratic cost-function coefficient.
    :param demand: Demand.

    :returns: System marginal cost.
    """
    decoupled_smc = pd.Series(GET_DISPATCH_MARGINAL_COST(
        demand, alpha)).mean()

    return decoupled_smc


def _get_curtailed_energy_fraction(
        generation: xr.DataArray, residual: xr.DataArray) -> xr.DataArray:
    """Get curtailed energy fraction.

    :param generation: Generation.
    :param residual: Residual demand.

    :returns: Curtailed energy fraction.
    """
    with LoggingContext('py.warnings', level='ERROR'):
        curt = -residual.where(residual < 0.).mean('time')
        curt /= generation.sum(['component', 'region']).mean('time')

    return curt


def _get_dispatch_generation(
        load: xr.DataArray,
        dispatch_generation_max_novre: float) -> xr.DataArray:
    """Get optimal dispatchable generation.

    :param load: (Residual) load.
    :param dispatch_generation_max_novre: Maximum dispatchable generation.

    :returns: Dispatchable generation.
    """
    dispatch_generation = load.where(load > 0., 0.).where(
        load < dispatch_generation_max_novre,
        dispatch_generation_max_novre)

    return dispatch_generation


def _get_lost_load(load: xr.DataArray,
                   dispatch_generation_max_novre: float) -> xr.DataArray:
    """Get optimal dispatchable generation.

    :param load: (Residual) load.
    :param dispatch_generation_max_novre: Maximum dispatchable generation.

    :returns: Dispatchable generation.
    """
    lost_load = load - dispatch_generation_max_novre
    lost_load = lost_load.where(lost_load > 0., 0.)

    return lost_load


def get_complementary_cdf(
        ldc: xr.DataArray, loadpoint_label: str = 'loadpoint') -> xr.DataArray:
    """Get (residual) demand complementary CDF, the inverse of the
    (residual) load duration curve.

    :param ldc: (Residual) load duration curve.
    :param loadpoint_label: Energy label.

    :returns: (Residual) demand complementary CDF.
    """
    coord_energy = loadpoint_label, ldc.values
    rccdf = xr.DataArray(ldc.indexes['peak_hour'],
                         coords=[coord_energy], attrs=ldc.attrs)

    return rccdf


def _get_value_factor_plant(
        capacityfactor: xr.DataArray,
        system_marginal_cost: xr.DataArray) -> xr.DataArray:
    """Get VRE value factor per plant.

    :param capacityfactor: Capacity factor.
    :param system_marginal_cost: System cost.

    :returns: Value factor per plant.
    """
    gen_mean = capacityfactor.mean('time')
    value_factor = (capacityfactor * system_marginal_cost).mean('time')
    value_factor /= gen_mean * system_marginal_cost.mean('time')

    return value_factor.where(gen_mean > TOL)


def _get_mean_lost_load_cost(
        lost_load: xr.DataArray, voll: float) -> float:
    """Get mean yearly lost-load cost.

    :param lost_load: Lost load.
    :param voll: Value of Lost Load.

    :returns: Mean yearly lost-load cost.
    """
    mean_lost_load_cost = (tp.cast(xr.DataArray, voll) *
                           lost_load).mean('time')

    return mean_lost_load_cost * YEAR_TO_HOUR


def get_lole(alpha: float, ldc: xr.DataArray, voll: float,
             cfg: e4tp.CfgType) -> float:
    """Get Loss of Load Expectation (over several years).

    :param alpha: Quadratic cost-function coefficient.
    :param ldc: (Residual) load duration curve.
    :param cfg: Input configuration.
    :param voll: Value of Lost Load.

    :returns: Loss of Load Expectation.
    """
    peak_rental_cost = _get_hourly_rental_cost_for_component('peak', cfg)
    marginal_costs = GET_DISPATCH_MARGINAL_COST(ldc, alpha)

    peak_hour = ldc.peak_hour

    # Get criterion
    diff = ((tp.cast(xr.DataArray, voll) - marginal_costs) * peak_hour
            - peak_hour.size * peak_rental_cost)

    lole = int(np.abs(diff).argmin())

    return lole


def _get_mean_dispatch_revenue(
        dispatch_generation: xr.DataArray,
        system_marginal_cost: xr.DataArray) -> float:
    """Get mean yearly dispatch revenue.

    :param dispatch_generation: Dispatchable generation.
    :param system_marginal_cost: System cost.

    :returns: Mean dispatch revenue.
    """
    return (system_marginal_cost * dispatch_generation).mean(
        'time') * YEAR_TO_HOUR


def _get_hourly_rental_cost_for_component(
        component_name: str, cfg: e4tp.CfgType) -> float:
    """Get hourly rental cost of component.

    :param component_name: Component name.
    :param cfg: Input configuration.

    :returns: Hourly rental cost.
    """
    cfg_annuity = tools.get_required_mapping_entry(cfg, 'annuity')
    annuity = tools.get_required_float_entry(cfg_annuity, component_name)
    cfg_fixed_om = tools.get_required_mapping_entry(cfg, 'fixed_om')
    fixed_om = tools.get_required_float_entry(cfg_fixed_om, component_name)

    return (annuity + fixed_om) / YEAR_TO_HOUR


def _get_utilization_at_loadpoint(
        loadpoint: float, ccdf: xr.DataArray,
        loadpoint_label: str = 'loadpoint') -> tp.Tuple[float, float]:
    """Get dispatch plant utilization at load point.

    :param loadpoint: load point above which plant is active.
    :param ccdf: (Residual) complementary CDF.
    :param loadpoint_label: Loadpoint label.

    :returns: Utilization and peak hour at load point.
    """
    peak_hour_at_loadpoint = float(_get_peak_hour_at_loadpoint(
        ccdf, {loadpoint_label: loadpoint}))
    utilization = peak_hour_at_loadpoint / len(ccdf)

    return utilization, peak_hour_at_loadpoint


def _get_peak_hour_at_loadpoint(
        ccdf: xr.DataArray, loadpoint_dim: tp.Mapping[str, float]) -> int:
    """Get complementary quantile corresponding to load point.

    :param ccdf: Complementary CDF.
    :param loadpoint_dim: Load-point dimension key-value pair.

    :returns: Complementary quantile corresponding to load point.
    """
    try:
        peak_hour_safe = int(ccdf.sel(**loadpoint_dim))
    except (TypeError, IndexError, KeyError):
        try:
            peak_hour = ccdf[::-1].interp(
                assume_sorted=True, **loadpoint_dim)
            if bool(peak_hour.isnull()):
                peak_hour = ccdf.sel(method='ffill', **loadpoint_dim)
            peak_hour_safe = int(peak_hour)
        except KeyError:
            peak_hour_safe = 0

    return peak_hour_safe


def get_dispatch_distribution_for_alpha(
        func: tp.Callable[[
            float, float, xr.Dataset, xr.DataArray], xr.Dataset],
        alpha: float, ds: xr.Dataset, ldc: xr.DataArray,
        loadpoints: tp.Sequence, **kwargs) -> xr.Dataset:
    """Get some properties over all dispatch plants
    for a given value of alpha.

    :param func: Function to compute a property of the dispatchable
      producers.
    :param alpha: Quadratic cost-function coefficient.
    :param ds: Solution dataset.
    :param loadpoints: load points.

    :returns: Updated dispatch-distribution dataset.
    """
    rccdf = get_complementary_cdf(
        ldc, loadpoint_label='residual_loadpoint')

    # Get effects for each load point
    data = [func(alpha, loadpoint, ds, rccdf)
            for loadpoint in loadpoints]

    # Concatenate along load points
    ds_dis = xr.concat(data, dim='loadpoint')

    return ds_dis.expand_dims('alpha').assign_coords(alpha=[alpha])
