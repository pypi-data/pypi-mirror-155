"""Cost minimization with residual load from dispatchable production with
quadratic variable costs with curtailment."""
from collections import OrderedDict
import numpy as np
import pandas as pd
import pyomo.environ as pyo
from e4clim.container.optimizer import OptimizerBase, SolutionBase, InputBase
from e4clim.utils.optimization_support import (
    _parse_solution, _update_solution_variables, _get_data)


class Optimizer(OptimizerBase):
    """Cost minimization with residual load from dispatchable production with
    quadratic variable costs with curtailment."""

    def __init__(self, app, cfg=None, **kwargs):
        """Build optimizer context.

        :param app: Context application.
        :param cfg: Optimizer configuration.
        """
        # Initialize as OptimizerBase
        name = 'dispatch_quadratic_cost_curtail'
        super(Optimizer, self).__init__(app, name, cfg=cfg, **kwargs)

        #: Demand component manager.
        self.context_component_demand = self.med.context_components[
            self.cfg['component']['demand']]

        #: Generation component managers.
        self.context_component_generation = OrderedDict()
        #: Generation component names.
        self.component_generation_names = set()
        # Add generation components
        for context_component_name in self.cfg['component']['capacityfactor']:
            context_component = self.med.context_components[
                context_component_name]
            self.context_component_generation[
                context_component_name] = context_component
            self.component_generation_names.add(
                context_component.component_name)

        # Overwrite input and solution with module class
        self.input = Input(self, self.cfg.get('input'), **kwargs)
        self.solution = Solution(self, self.cfg, **kwargs)

        #: Model.
        self.model = pyo.ConcreteModel()

        #: Results.
        self.results = None

        #: Sets.
        self._set_names = ['vre', 'region', 'time']

        #: Coordinates.
        self.coords = OrderedDict({})

        #: Variable dimensions.
        self.variable_dims = {'capacity_vre': ['vre', 'region']}

        #: Constraint definitions as dictionnary from constraint name
        #: to a tuple with a list of sets and a rule function.
        self.constraint_definitions = {}
        # 'c_adequacy': (['time'], self._rule_adequacy)

        # Add optional constraints
        cfg_cstr = self.cfg.get('constraint')
        if cfg_cstr is not None:
            if cfg_cstr.get('capacity_vre_total'):
                self.constraint_definitions['c_capacity_vre_total'] = (
                    ['vre'], self.capacity_vre_total_rule)
            if cfg_cstr.get('generation_vre_total'):
                self.constraint_definitions['c_generation_vre_total'] = (
                    ['vre'], self.generation_vre_total_rule)

        #: Initial VRE capacity
        self.initial_capacity_vre = None

        # Update variable names (as groups)
        _update_solution_variables(
            self.solution, self.variable_dims, self.cfg, **kwargs)

    def solve(self, *args, **kwargs):
        """Solve optimization problem."""
        # Get input data
        self.input.get_data(**kwargs)

        # Update sets, coordinates and variables with loaded input
        self._update_sets_coords(**kwargs)
        self._update_state_variables(**kwargs)

        # Cost
        self.info('Defining cost')
        self.model.cost = pyo.Objective(rule=self.cost_rule)

        # Add constraints
        self.info('Defining constraints')
        for cstr_name, cstr_def in self.constraint_definitions.items():
            indices = [getattr(self.model, dim) for dim in cstr_def[0]]
            constraint = pyo.Constraint(*indices, rule=cstr_def[1])
            setattr(self.model, cstr_name, constraint)

        # Create a 'dual' suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        self.model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

        # Create solver
        options = None
        cfg_solver = self.cfg.get('solver')
        if cfg_solver is not None:
            solver_name = cfg_solver.get('name') or 'ipopt'
            options = cfg_solver.get('options')
        solver = pyo.SolverFactory(solver_name)

        # Set solver options
        if options is not None:
            for opt, val in options.items():
                solver.options[opt] = val
        tee = False if self.cfg.get('no_verbose') else True

        # # Set warm start
        # solver.options['warm_start_init_point'] = 'yes'

        # Solve
        self.info('Solving optimization problem')
        self.results = solver.solve(self.model, tee=tee)

        # Check
        if ((self.results.solver.status == pyo.SolverStatus.ok) and
            (self.results.solver.termination_condition ==
             pyo.TerminationCondition.optimal)):
            self.info("Solution feasible and optimal.")
        elif (self.results.solver.termination_condition ==
              pyo.TerminationCondition.infeasible):
            self.warning("Solution infeasible!")
            raise RuntimeError(str(self.results.solver))
        else:
            # something else is wrong
            raise RuntimeError(str(self.results.solver))

        # Parse solution
        ds = _parse_solution(
            self.model, self.variable_dims, self.cfg, **kwargs)

        return ds

    def cost_rule(self, m):
        """Get cost (G€).

        :param m: Model.
        :type m: :py:class:`pyomo.Model`

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        # # CAPEX VRE
        expr = sum(self.input.cfg['capex'][tec] * sum(
            m.capacity_vre[tec, reg] for reg in m.region) for tec in m.vre)

        # Dispatch generation variable costs
        for t in m.time:
            generation_dispatch = self._get_generation_dispatch_expr(m, t)
            expr += (generation_dispatch / 2 *
                     self.input.dispatch_marginal_cost_estimator.predict(
                         [[pyo.value(generation_dispatch)]])[0])

        # Convert from M€ to G€
        expr /= 1.e3

        return expr

    def capacity_vre_total_rule(self, m, tec):
        """Get constraint on VRE generation.

        :param m: Model.
        :param tec: Technology.
        :type m: :py:class:`pyomo.Model`
        :type tec: str

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        # Get total VRE capacity for technology
        capacity_vre_total = sum(m.capacity_vre[tec, reg] for reg in m.region)

        return capacity_vre_total == self.input.capacity_vre_total[tec]

    def generation_vre_total_rule(self, m, tec):
        """Get constraint on VRE generation.

        :param m: Model.
        :param tec: Technology.
        :type m: :py:class:`pyomo.Model`
        :type tec: str

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        generation_vre_total = sum(
            self._get_generation_vre_expr(m, tec, reg, t)
            for reg in m.region for t in m.time)

        return generation_vre_total == self.input.generation_vre_total[tec]

    def _get_generation_dispatch_expr(self, m, t):
        """Get dispatch generation satisfying adequacy with curtailment.

        :param m: Model.
        :param t: Timestamp.
        :type m: :py:class:`pyomo.Model`
        :type t: :py:class:`pyomo.Set`

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        # Total VRE generation
        generation_vre_total = self._get_generation_vre_total_expr(m, t)

        # Get dispatch generation
        generation_dispatch = self.input.load_total[t] - generation_vre_total
        if pyo.value(generation_dispatch < 0.):
            generation_dispatch = 0.

        return generation_dispatch

    def _get_generation_vre_total_expr(self, m, t):
        """Get total VRE generation from capacity and capacity factor.

        :param m: Model.
        :param t: Timestamp.
        :type m: :py:class:`pyomo.Model`
        :type t: :py:class:`pyomo.Set`

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        # Get VRE generation
        generation_vre = sum(self._get_generation_vre_expr(m, tec, reg, t)
                             for tec in m.vre for reg in m.region)

        return generation_vre

    def _get_generation_vre_expr(self, m, tec, reg, t):
        """Get VRE generation from capacity and capacity factor.

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.
        :param t: Timestamp.
        :type m: :py:class:`pyomo.Model`
        :type tec: str
        :type reg: str
        :type t: :py:class:`pyomo.Set`

        :returns: Expression.
        :rtype: :py:class:`pyo.Expression`
        """
        return m.capacity_vre[tec, reg] * self.input[
            'capacityfactor'][tec, reg, t]

    def _update_sets_coords(self, **kwargs):
        """Update sets, coordinates with loaded input."""
        # Update sets and coordinates with loaded input (for time index)
        for set_name in self._set_names:
            s = pyo.Set(ordered=True, initialize=getattr(self.input, set_name))
            setattr(self.model, set_name, s)
            self.coords[set_name] = set_name, s.value_list

    def _update_state_variables(self, **kwargs):
        """Update variables with loaded input."""
        variable_name = 'capacity_vre'
        dims = self.variable_dims[variable_name]
        indices = [getattr(self.model, dim) for dim in dims]

        if self.input.capacity_vre_total is not None:
            # Initialize VRE capacity with mean capacity factors
            x0 = self.input['capacityfactor'].unstack().mean('columns')
            x0 *= self.input.capacity_vre_total.sum() / x0.sum()
            self.initial_capacity_vre = x0
            initialize = self._get_initial_capacity_vre
        else:
            initialize = None

        # Create model variable
        var = pyo.Var(*indices, domain=pyo.NonNegativeReals,
                      initialize=initialize)

        # Add variable to model
        setattr(self.model, variable_name, var)

    def _get_initial_capacity_vre(self, m, tec, reg):
        """Get initial VRE capacity from mean capacity factors.

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.
        :type m: :py:class:`pyomo.Model`
        :type tec: str
        :type reg: str

        :returns: Initial VRE capacity for technology and region.
        :rtype: float
        """
        return self.initial_capacity_vre[tec, reg]


class Input(InputBase):
    """Optimization problem input data source."""

    def __init__(self, optimizer, cfg=None, **kwargs):
        """Initialize input data source.

        :param optimizer: Optimizer.
        :param cfg: Input configuration.
        :type optimizer: :py:class:`.optimization.OptimizerBase`
        :type cfg: mapping
        """
        cfg = {} if cfg is None else cfg
        super(Input, self).__init__(optimizer, cfg=cfg, **kwargs)

        # Set input data period to use
        self._start_date = pd.Timestamp(self.cfg['start_date'])
        self._end_date = pd.Timestamp(
            self.cfg['end_date']) - pd.Timedelta('1 second')

        # Add variable
        self.update_variables(['capacityfactor', 'demand'])

        #: VRE omponents index.
        self.vre = pd.Index(
            [context_component.component_name for context_component in (
                self.optimizer.context_component_generation.values())])

        context_component_names = list(
            self.optimizer.context_component_generation)
        #: Region index.
        self.region = pd.Index(self.optimizer.context_component_generation[
            context_component_names[0]].place_names)

        #: Time index (value set after load).
        self.time = None

        #: Total VRE capacity used as constraint
        self.capacity_vre_total = None
        self.generation_vre_total = None

        #: Dispatch marginal cost estimator
        self.dispatch_marginal_cost_estimator = None

        #: Total load, including storage (GWh).
        self.load_total = None

    def download(self, **kwargs) -> None:
        pass

    def parse(self, **kwargs):
        """Parse optimization problem input data."""
        ds = self.parse_available_components(regional=True, dem_conv=1.e-3,
                                             **kwargs)

        # Set time index
        self.time = ds['capacityfactor'].index.levels[-1]

        return ds

    def get_residual_load(self, ds, **kwargs):
        """Get residual load.

        :param ds: Solution dataset.
        :type ds: mapping

        :returns: VRE generation.
        :rtype: :py:class:`xarray.DataArray`
        """
        # Total VRE generation
        generation_vre = self.get_generation_vre(ds, **kwargs)
        generation_vre_total = generation_vre.sum(['region', 'vre'])

        # Get dispatch generation
        residual = self.load_total.to_xarray() - generation_vre_total

        return residual

    def get_generation_dispatch(self, ds, **kwargs):
        """Get dispatch generation satisfying adequacy with curtailment.

        :param ds: Solution dataset.
        :type ds: mapping

        :returns: VRE generation.
        :rtype: :py:class:`xarray.DataArray`
        """
        da_res = self.get_residual_load(ds, **kwargs)
        generation_dispatch = da_res.where(da_res > 0., 0.)

        return generation_dispatch

    @_get_data
    def get_generation_vre(self, ds, **kwargs):
        """Get constraint on VRE generation.

        :param ds: Solution dataset.
        :type ds: mapping

        :returns: VRE generation.
        :rtype: :py:class:`xarray.DataArray`
        """
        # Get capacity factor as data array
        da_cf = self['capacityfactor'].to_xarray()

        # Get VRE capacities
        da_cap_vre = ds['capacity_vre'].sel(vre=da_cf.vre)

        # Return VRE generation
        return da_cap_vre * da_cf

    def set_capacity_vre_total(self, capacity_vre_total, **kwargs):
        """Set total VRE capacity for constraint.

        :param capacity_vre_total: Total VRE capacity.
        :type capacity_vre_total: :py:class:`xarray.DataArray` or
          :py:class:`pandas.Series`
        """
        self.capacity_vre_total = capacity_vre_total

        # Try to convert to pandas
        try:
            self.capacity_vre_total = self.capacity_vre_total.to_pandas()
        except AttributeError:
            pass

    def set_generation_vre_total(self, generation_vre_total, **kwargs):
        """Set total VRE generation for constraint.

        :param generation_vre_total: Total VRE generation.
        :type generation_vre_total: :py:class:`xarray.DataArray` or
          :py:class:`pandas.Series`
        """
        self.generation_vre_total = generation_vre_total

        # Try to convert to pandas
        try:
            self.generation_vre_total = self.generation_vre_total.to_pandas()
        except AttributeError:
            pass

    def set_dispatch_marginal_cost_estimator(self, estimator, **kwargs):
        """Set dispatch marginal cost estimator.

        :param estimator: Estimator.
        :type estimator: :py:class:`sklearn.base.BaseEstimator`.
        """
        self.dispatch_marginal_cost_estimator = estimator

    def set_load_total(self, load_total, **kwargs):
        """Set total load.

        :param load_total: Total load.
        :type load_total: :py:class:`xarray.DataArray` or
          :py:class:`pandas.Series`
        """
        self.load_total = load_total
        # Try to convert to pandas
        try:
            self.load_total = self.load_total.to_pandas()
        except AttributeError:
            pass

    def get_data_postfix(self, **kwargs):
        """Get data postfix.

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get standard postfix
            postfix = []

            # Demand postfix
            demand_result_mng = self.optimizer.context_component_demand[
                'demand']
            postfix.append(demand_result_mng.get_data_postfix(
                **kwargs).split('_'))

            # Capacity factors postfix
            for context_component in (
                    self.optimizer.context_component_generation.values()):
                postfix.append(context_component['capacityfactor'].
                               get_data_postfix(**kwargs).split('_'))

            # Join postfixes
            postfix = np.concatenate(postfix)
            _, idx = np.unique(postfix, return_index=True)
            postfix = '_'.join(postfix[np.sort(idx)])

            # Add period
            postfix += '_{}-{}'.format(
                self._start_date.date().strftime('%Y%m%d'),
                self._end_date.date().strftime('%Y%m%d'))

        return postfix

    def update_from_coarse(self, med_coarse, ds, est, **kwargs):
        """Update input from coarse model.
        """
        # Get data
        capacity_vre_total = ds['capacity']
        da_gen_vre = med_coarse.optimizer.input.get_generation_vre(ds)
        da_load = med_coarse.optimizer.input.get_load(ds)
        generation_vre_total = da_gen_vre.sum('time')
        da_other = da_gen_vre.sel(
            technology=['wind-offshore', 'river']).sum('technology')

        # Set up
        self.set_capacity_vre_total(capacity_vre_total)
        self.set_generation_vre_total(generation_vre_total)
        self.set_dispatch_marginal_cost_estimator(est)
        self.set_load_total(da_load - da_other)


class Solution(SolutionBase):
    def get_data_postfix(self, **kwargs):
        """Get optimization results postfix with constraints in addition
        to default postfix.

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get default postfix
            postfix = super(Solution, self).get_data_postfix(**kwargs)

        return postfix


def _parse_index(coord):
    """Parse index from coordinate tuple.

    :param coord: Tuple with dimension name and coordinate index.
    :type coord: tuple

    :returns: Index.
    :rtype: :py:class:`pandas.Index`
    """
    index = coord[1]
    try:
        index = pd.DatetimeIndex(index)
    except ValueError:
        index = pd.Index(index)
    index.name = coord[0]

    return index
