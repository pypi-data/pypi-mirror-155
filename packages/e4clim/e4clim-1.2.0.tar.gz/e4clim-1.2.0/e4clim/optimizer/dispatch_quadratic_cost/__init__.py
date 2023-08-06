from collections import OrderedDict
from datetime import datetime
from orderedset import OrderedSet
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt.results import SolverResults
import typing as tp
import xarray as xr
import e4clim
import e4clim.typing as e4tp
import e4clim.utils.optimization_support as support
from e4clim.utils import tools
from . import dqc_input
from . import dqc_solution


CoordsType = tp.MutableMapping[str, tp.Tuple[str, tp.Sequence]]
CstrType = tp.Tuple[tp.Sequence[str], tp.Callable[..., pyo.Expression]]
CstrDefType = tp.MutableMapping[str, CstrType]
VariableDimsType = tp.MutableMapping[str, tp.MutableSet[str]]

#: Dispatch variable-cost function.
GET_DISPATCH_VARIABLE_COST = dqc_input.GET_DISPATCH_VARIABLE_COST
#: Dispatch marginal-cost function.
GET_DISPATCH_MARGINAL_COST = dqc_input.GET_DISPATCH_MARGINAL_COST

#: Default optimization-problem type.
DEFAULT_PROBLEM: tp.Final[str] = 'variable'
#: Available optimization-problem types.
AVAILABLE_PROBLEMS: tp.Final[tp.List[str]] = [
    DEFAULT_PROBLEM, 'constant', 'decoupled']


class Optimizer(support.OptimizerWithPyomo):
    """Total cost minimization with quadratic dispatch variable costs."""

    #: Constraint definitions as dictionnary from constraint name
    #: to a tuple with a list of sets and a rule function.
    _constraint_definitions: CstrDefType

    #: Coordinates.
    coords: CoordsType

    #: Initial maximum dispatchable generation
    _dispatch_generation_max_novre: float

    #: Optimizer-context input.
    input: dqc_input.Input

    #: Initial Loss of Load Expectation over the period.
    _lole_novre: float

    #: Mean capacity factors.
    _mean_capacityfactor: pd.core.generic.NDFrame

    #: Mean demand.
    _mean_demand: float

    #: Control-parameter name.
    param_name: tp.Final[str] = 'alpha'

    #: Optimization-problem type (`'variable`', `'constant`', or `'decoupled`').
    problem: str

    #: Results.
    results: SolverResults

    #: Sets.
    _set_names: tp.MutableSet[str]

    #: Optimizer-context solution.
    solution: dqc_solution.Solution

    #: Variable dimensions.
    variable_dims: VariableDimsType

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextSingleOptimizer',
                 cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Build optimizer context.

        :param app: Context application.
        :param cfg: Optimizer configuration.
        """
        # Initialize as OptimizerBase
        name = 'dispatch_quadratic_cost'
        super(Optimizer, self).__init__(parent, name, cfg=cfg, **kwargs)

        # Coordinates.
        self.coords = OrderedDict()

        # Constraint definitions as dictionnary from constraint name
        # to a tuple with a list of sets and a rule function.
        self._constraint_definitions = {}

    def get_new_input(self, **kwargs) -> dqc_input.Input:
        """Get new input.

        :param returns: New input.
        """
        return dqc_input.Input(self.parent, **kwargs)

    def get_new_solution(self, **kwargs) -> dqc_solution.Solution:
        """Get new solution.

        :param returns: New solution.
        """
        return dqc_solution.Solution(self.parent, **kwargs)

    def _set_variable_dims(self) -> None:
        """Set variable-dimensions mapping."""
        # Problem type
        self.problem = tools.get_required_str_entry(
            self.cfg, 'problem', DEFAULT_PROBLEM)
        assert self.problem in AVAILABLE_PROBLEMS, (
            '"problem" configuration-entry should be in {}'.format(
                AVAILABLE_PROBLEMS))

        set_names = ['vre', 'region']
        self.variable_dims = {'capacity': OrderedSet(['vre', 'region'])}

        if self.problem in ['constant', 'decoupled']:
            self.variable_dims.update({
                'dispatch_generation': OrderedSet(),
                'lost_load': OrderedSet()
            })
            self._mean_capacityfactor = self.input.capacityfactor.unstack(
            ).mean('columns')
            self._mean_demand = self.input.demand.mean()
        elif self.problem == 'variable':
            set_names.append('time')
            self.variable_dims.update({
                'dispatch_generation': OrderedSet(['time']),
                'lost_load': OrderedSet(['time'])
            })

        self._set_names = OrderedSet(set_names)

    def _set_constraints(self) -> None:
        """Set constraints."""
        self._constraint_definitions = {}
        if self.problem in ['constant', 'decoupled']:
            self._constraint_definitions['c_adequacy'] = (
                [], self._adequacy_constant_rule)
        elif self.problem == 'variable':
            self._constraint_definitions['c_adequacy'] = (
                ['time'], self._adequacy_instant_rule)

        constraint_name = 'capacity_max'
        cfg_constraint = tools.get_required_mapping_entry(
            self.cfg, 'constraint')
        if cfg_constraint.get(constraint_name):
            self._constraint_definitions['c_' + constraint_name] = (
                ['vre', 'region'], getattr(
                    self, '_' + constraint_name + '_rule'))

    def _set_cost_rule(self) -> None:
        """Set cost rule."""
        setattr(self, '_cost_rule', getattr(
            self, '_{}_cost_rule'.format(self.problem)))

    def _update_capacity(self, model: pyo.ConcreteModel) -> None:
        """Update positive VRE-capacity variable.

        :param model: Model.
        """
        variable_name = 'capacity'
        dims = self.variable_dims[variable_name]
        indices = [getattr(model, dim) for dim in dims]
        within = pyo.NonNegativeReals
        initialize = 0.
        var = pyo.Var(*indices, within=within, initialize=initialize)
        setattr(model, variable_name, var)

    def _update_dispatch_generation(self, model: pyo.ConcreteModel) -> None:
        """Update dispatchable-generation variable. Should be positive.

        :param model: Model.
        """
        variable_name = 'dispatch_generation'
        dims = self.variable_dims[variable_name]
        indices = [getattr(model, dim) for dim in dims]
        within = pyo.NonNegativeReals
        if self.problem in ['constant', 'decoupled']:
            var = pyo.Var(*indices, within=within,
                          initialize=self._initialize_as_constant_demand_rule)
        elif self.problem == 'variable':
            var = pyo.Var(*indices, within=within,
                          initialize=self._initialize_as_instant_demand_rule)

        setattr(model, variable_name, var)

    def _update_lost_load(self, model: pyo.ConcreteModel) -> None:
        """Update lost-load variable. Should be positive.

        :param model: Model.
        """
        variable_name = 'lost_load'
        dims = self.variable_dims[variable_name]
        indices = [getattr(model, dim) for dim in dims]
        within = pyo.NonNegativeReals
        initialize = 0.
        var = pyo.Var(*indices, within=within, initialize=initialize)
        setattr(model, variable_name, var)

    def _initialize_as_instant_demand_rule(
            self, m: pyo.ConcreteModel, t: datetime) -> float:
        """Rule to initialize time-indexed variable as demand.

        :param m: Model.
        :param t: Timestamp.

        :returns: Demand at timestamp.
        """
        return self.input.demand[t]

    def _initialize_as_constant_demand_rule(self, m: pyo.ConcreteModel) -> float:
        """Rule to initialize variable as mean demand.

        :param m: Model.

        :returns: Mean demand.
        """
        return self._mean_demand

    def _add_constraints_to_model(self, model: pyo.ConcreteModel) -> None:
        """Add constraints to model.

        :param model: Model.
        """
        self.info('Defining constraints')
        for cstr_name, cstr_def in self._constraint_definitions.items():
            indices = [getattr(model, dim) for dim in cstr_def[0]]
            constraint = pyo.Constraint(*indices, rule=cstr_def[1])
            setattr(model, cstr_name, constraint)

    def _set_param_dependent_constraints(
            self, model: pyo.ConcreteModel) -> None:
        """Set parameter dependent constraints.

        :param model: Model.
        """
        self._set_constraint_dispatch_generation_max_novre(model)

    def _set_constraint_dispatch_generation_max_novre(
            self, model: pyo.ConcreteModel) -> None:
        """Set constraint on maximum dispatchable generation.

        :param model: Model.
        """
        self._set_lole_novre()

        self._set_dispatch_generation_max_novre()

        # Set constraint
        model.del_component('c_dispatch_generation_max_novre')
        if self.problem in ['constant', 'decoupled']:
            model.c_dispatch_generation_max_novre = pyo.Constraint(
                rule=self._constant_dispatch_generation_max_novre_rule)
        else:
            model.c_dispatch_generation_max_novre = pyo.Constraint(
                model.time, rule=self._instant_dispatch_generation_max_novre_rule)

    def _set_lole_novre(self) -> None:
        """Set Loss of Load Expectation without VRE."""
        self._lole_novre = dqc_input.get_lole(
            self.param, self.input.ldc, self.input.voll, self.input.cfg)

    def _set_dispatch_generation_max_novre(self) -> None:
        """Set maximum dispatchable generation without VRE."""
        self._dispatch_generation_max_novre = (
            self.input.get_dispatch_generation_max_novre(
                lole_novre=self._lole_novre))

    def _add_solution_for_param(
            self, ds: tp.Optional[xr.Dataset],
            model: pyo.ConcreteModel) -> xr.Dataset:
        """Update solution.

        :param ds: Previous solution dataset.
        :param model: Model.

        :returns: Updated solution.
        """
        # Parse solution
        ds_param = support.parse_solution(model, self.variable_dims, self.cfg)
        ds_param = ds_param.rename(vre='component')

        # Input properties
        nt = len(self.input.ldc.peak_hour)
        ds_param['lolp_novre'] = self._lole_novre / nt
        ds_param['dispatch_generation_max_novre'] = (
            self._dispatch_generation_max_novre)

        # Add param dimension
        ds_param = ds_param.expand_dims({self.param_name: [self.param]})

        ds = (ds_param if not ds else xr.concat(
            [ds, ds_param], dim=self.param_name, data_vars='minimal'))

        return ds

    def _variable_cost_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean yearly total system cost (€/y) for variable problem.

        :param m: Model.

        :returns: Expression.
        """
        expr = self._get_hourly_vre_cost_expr(m)

        # Multiply by time-series length to adapt to sum of variable costs
        expr *= len(m.time)

        # Summed hourly generation variable and lost-load cost
        for t in m.time:
            expr += self._get_instant_dispatch_variable_cost_expr(m, t)
            expr += self._get_instant_lost_load_cost_expr(m, t)

        # Convert to mean of one-year sum
        expr *= dqc_input.YEAR_TO_HOUR / len(m.time)

        return expr

    def _constant_cost_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean yearly total system cost (€/y) for constant problem.

        :param m: Model.

        :returns: Expression.
        """
        expr = self._get_hourly_vre_cost_expr(m)

        # Summed hourly generation variable and lost-load cost
        expr += self._get_constant_dispatch_variable_cost_expr(m)
        expr += self._get_constant_lost_load_cost_expr(m)

        # Convert to mean of one-year sum
        expr *= dqc_input.YEAR_TO_HOUR

        return expr

    def _decoupled_cost_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean yearly total system cost (€/y) for decoupled problem.

        :param m: Model.

        :returns: Expression.
        """
        expr = self._get_hourly_vre_cost_expr(m)

        # Summed hourly generation variable and lost-load cost
        expr += self._get_decoupled_dispatch_variable_cost_expr(m)
        expr += self._get_constant_lost_load_cost_expr(m)

        # Convert to mean of one-year sum
        expr *= dqc_input.YEAR_TO_HOUR

        return expr

    def _adequacy_instant_rule(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get inequality constraint for adequacy at timestamp
          (instantaneous VRE-generation version).

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        total_generation = self._get_instant_total_generation_expr(m, t)

        return total_generation >= self.input.demand[t]

    def _adequacy_constant_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get inequality constraint for adequacy at timestamp
        (time-averaged VRE-generation version).

        :param m: Model.

        :returns: Expression.
        """
        vre_generation = self._get_constant_vre_generation_total_expr(m)

        nonvre_generation = self._get_constant_nonvre_generation_expr(m)

        return (vre_generation + nonvre_generation >= self._mean_demand)

    def _instant_dispatch_generation_max_novre_rule(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get constraint on maximum dispatchable generation at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        return m.dispatch_generation[t] <= self._dispatch_generation_max_novre

    def _constant_dispatch_generation_max_novre_rule(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get constraint on maximum mean dispatchable generation.

        :param m: Model.

        :returns: Expression.
        """
        return m.dispatch_generation <= self._dispatch_generation_max_novre

    def _capacity_max_rule(
            self, m: pyo.ConcreteModel, tec: str, reg: str) -> pyo.Expression:
        """Get maximum-capacity constraint for technology and region.

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.

        :returns: Expression.
        """
        return m.capacity[tec, reg] <= self.input['capacity_max'][tec][reg]

    def _get_hourly_vre_cost_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get hourly VRE cost.

        :param m: Model.

        :returns: Expression.
        """
        return sum(self.input['hourly_rental_cost'][tec] * sum(
            m.capacity[tec, reg] for reg in m.region) for tec in m.vre)

    def _get_instant_dispatch_variable_cost_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get dispatch variable cost at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        # Get dispatchable-generation variable cost
        cost_generation = GET_DISPATCH_VARIABLE_COST(
            m.dispatch_generation[t], self.param)

        return cost_generation

    def _get_decoupled_dispatch_variable_cost_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get decoupled dispatch variable cost.

        :param m: Model.

        :returns: Expression.
        """
        # Get decoupled marginal cost
        decoupled_marginal_cost = dqc_input._get_decoupled_system_marginal_cost(
            self.param, self.input.demand)

        # Get dispatchable-generation variable cost
        cost_generation = decoupled_marginal_cost * m.dispatch_generation

        return cost_generation

    def _get_constant_dispatch_variable_cost_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean dispatch variable cost.

        :param m: Model.

        :returns: Expression.
        """
        # Get dispatchable-generation variable cost
        cost_generation = GET_DISPATCH_VARIABLE_COST(
            m.dispatch_generation, self.param)

        return cost_generation

    def _get_instant_lost_load_cost_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get lost-load cost at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        # Get cost of lost load
        cost_lost_load = self.input.voll * m.lost_load[t]

        return cost_lost_load

    def _get_constant_lost_load_cost_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean lost-load cost.

        :param m: Model.

        :returns: Expression.
        """
        # Get cost of lost load
        cost_lost_load = self.input.voll * m.lost_load

        return cost_lost_load

    def _get_instant_total_generation_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get instant total generation as sum of VRE and non-VRE generation
        at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        vre_generation = self._get_instant_vre_generation_total_expr(m, t)

        nonvre_generation = self._get_instant_nonvre_generation_expr(m, t)

        return vre_generation + nonvre_generation

    def _get_instant_nonvre_generation_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get non-VRE generation as sum of dispatchable generation and
        lost load at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        return m.dispatch_generation[t] + m.lost_load[t]

    def _get_constant_nonvre_generation_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get time-averaged non-VRE generation as sum of dispatchable generation
        and lost load.

        :param m: Model.

        :returns: Expression.
        """
        return m.dispatch_generation + m.lost_load

    def _get_instant_vre_generation_total_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get total VRE generation from capacity and capacity factor
        at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        # Get VRE generation
        vre_generation = sum(
            self._get_instant_vre_generation_expr(m, tec, reg, t)
            for tec in m.vre for reg in m.region)

        return vre_generation

    def _get_constant_vre_generation_total_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get total time-averaged VRE generation from capacity
        and capacity factor.

        :param m: Model.

        :returns: Expression.
        """
        # Get VRE generation
        vre_generation = sum(self._get_constant_vre_generation_expr(
            m, tec, reg) for tec in m.vre for reg in m.region)

        return vre_generation

    def _get_instant_vre_generation_expr(
            self, m: pyo.ConcreteModel, tec: str, reg: str,
            t: datetime) -> pyo.Expression:
        """Get VRE generation at timestamp from capacity and capacity factor
        for technology and region (instantaneous version).

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.
        :param t: Timestamp.

        :returns: Expression.
        """
        return m.capacity[tec, reg] * self.input.capacityfactor[tec, reg, t]

    def _get_constant_vre_generation_expr(
            self, m: pyo.ConcreteModel, tec: str, reg: str) -> pyo.Expression:
        """Get VRE generation at timestamp from capacity and capacity factor
        for technology and region (time-average version).

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.

        :returns: Expression.
        """
        return m.capacity[tec, reg] * self._mean_capacityfactor[tec, reg]
