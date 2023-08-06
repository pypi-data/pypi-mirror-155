"""Renewable-energy mean-risk optimization module."""
from collections import OrderedDict
from datetime import datetime
import numpy as np
from orderedset import OrderedSet
import pandas as pd
import pyomo.environ as pyo
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.optimizer_data_source import (
    OptimizerInputBase, OptimizerSolutionBase)
from e4clim.container.parsing_data_source import ParsingDataSourceBase
import e4clim.typing as e4tp
import e4clim.utils.optimization_support as support
from e4clim.utils import tools

#: Year to hour conversion constant.
YEAR_TO_HOUR = 365.25 * 24


class Optimizer(support.OptimizerWithPyomo):
    """Renewable energy mean risk optimizer."""

    #: Optimizer-context input.
    input: 'Input'

    #: Control-parameter name.
    param_name: tp.Final[str] = 'vre_cost_max'

    #: Optimizer-context solution.
    solution: 'Solution'

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextSingleOptimizer',
                 cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Build optimizer context.

        :param app: Context application.
        :param cfg: Optimizer configuration.
        """
        # Initialize as OptimizerBase
        name = 'mva'
        super(Optimizer, self).__init__(parent, name, cfg=cfg, **kwargs)

        #: Coordinates.
        self.coords = OrderedDict()

        #: Constraint definitions as dictionnary from constraint name
        #: to a tuple with a list of sets and a rule function.
        self._constraint_definitions = {}

    def get_new_input(self, **kwargs) -> None:
        """Get new input.

        :param returns: New input.
        """
        return Input(self.parent, **kwargs)

    def get_new_solution(self, **kwargs) -> None:
        """Get new solution.

        :param returns: New solution.
        """
        return Solution(self.parent, **kwargs)

    def _set_variable_dims(self) -> None:
        """Set variable-dimensions mapping."""
        self._set_names = OrderedSet(['vre', 'region', 'time'])
        self.variable_dims = {'capacity': OrderedSet(['vre', 'region'])}

    def _set_constraints(self) -> None:
        """Set constraints."""
        self._constraint_definitions = {}

        constraint_name = 'capacity_max'
        cfg_constraint = tools.get_required_mapping_entry(
            self.cfg, 'constraint')
        if cfg_constraint.get(constraint_name):
            self._constraint_definitions['c_' + constraint_name] = (
                ['vre', 'region'], getattr(
                    self, '_' + constraint_name + '_rule'))

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

    def _set_param_dependent_constraints(
            self, model: pyo.ConcreteModel) -> None:
        """Set parameter dependent constraints.

        :param model: Model.
        """
        model.del_component('c_vre_cost_max')
        model.c_vre_cost_max = pyo.Constraint(rule=self._vre_cost_max_rule)

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

        # Add control-parameter dimension
        ds_param = ds_param.expand_dims({self.param_name: [self.param]})

        ds = (ds_param if not ds else xr.concat(
            [ds, ds_param], dim=self.param_name, data_vars='minimal'))

        return ds

    def _cost_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get mean yearly total system cost (€/y).

        :param m: Model.

        :returns: Expression.
        """
        # Summed hourly generation variable and lost-load cost
        mean: pyo.Expression = 0
        mean_square: pyo.Expression = 0
        for t in m.time:
            residual_load = self._get_residual_expr(m, t)
            mean += residual_load
            mean_square += residual_load**2
        mean /= len(m.time)
        mean_square /= len(m.time)
        variance = mean_square - mean**2
        expr = mean**self.cfg['kappa'] + self.cfg['beta'] * variance

        # Convert to mean yearly sum
        expr *= YEAR_TO_HOUR

        return expr

    def _capacity_max_rule(
            self, m: pyo.ConcreteModel, tec: str, reg: str) -> pyo.Expression:
        """Get maximum-capacity constraint for technology and region.

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.

        :returns: Expression.
        """
        return m.capacity[tec, reg] <= self.input['capacity_max'][tec][reg]

    def _vre_cost_max_rule(self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get maximum-capacity constraint for technology and region.

        :param m: Model.
        :param tec: Technology.
        :param reg: Region.

        :returns: Expression.
        """
        return self._get_hourly_vre_cost_expr(m) <= self.param

    def _get_hourly_vre_cost_expr(
            self, m: pyo.ConcreteModel) -> pyo.Expression:
        """Get hourly VRE cost.

        :param m: Model.

        :returns: Expression.
        """
        return sum(self.input.hourly_rental_cost[tec] * sum(
            m.capacity[tec, reg] for reg in m.region) for tec in m.vre)

    def _get_residual_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get generation cost at timestamp.

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        vre_generation_total = self._get_instant_vre_generation_total_expr(
            m, t)

        residual = self.input.demand[t] - vre_generation_total

        return residual

    def _get_instant_vre_generation_total_expr(
            self, m: pyo.ConcreteModel, t: datetime) -> pyo.Expression:
        """Get total VRE generation from capacity and capacity factor
        at timestamp (instantaneous version).

        :param m: Model.
        :param t: Timestamp.

        :returns: Expression.
        """
        # Get VRE generation
        vre_generation = sum(
            self._get_instant_vre_generation_expr(m, tec, reg, t)
            for tec in m.vre for reg in m.region)

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


class Input(OptimizerInputBase,
            support.OptimizerInputComponentsParserMixin):
    """Optimization problem input data source."""

    #: Capacity factors.
    capacityfactor: pd.core.generic.NDFrame

    #: Demand.
    demand: pd.core.generic.NDFrame

    #: Region index.
    region: pd.Index
    #: Time index (value set after load).
    _time: pd.Index
    #: VRE components index.
    vre: pd.Index

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

        self._init_period()

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

    def _init_period(self) -> None:
        """Initialize optimization period."""
        self._start_date = pd.Timestamp(self.cfg['start_date'])
        self._end_date = pd.Timestamp(
            self.cfg['end_date']) - pd.Timedelta('1 second')

    def _init_variables(self) -> tp.Set:
        """Initialize input variables and return names of variables to read.

        :returns: Names of variables to read.
        """
        self.update_variables({'capacityfactor', 'demand',
                               'hourly_rental_cost'})

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

        ds['hourly_rental_cost'] = self.get_hourly_rental_costs()

        return ds

    def get_data_callback(self, *args, **kwargs) -> None:
        """Add inputs as attributes."""
        self.capacityfactor = tools.get_frame_safe(self.data, 'capacityfactor')
        self.demand = tools.get_frame_safe(self.data, 'demand')
        self.hourly_rental_cost = tools.get_frame_safe(
            self.data, 'hourly_rental_cost')

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

    def get_hourly_rental_costs(self) -> pd.Series:
        """Get hourly rental costs.

        :returns: Hourly rental costs.
        """
        index = pd.Index(self.component_generation_names)
        index.name = 'component'

        data = [_get_hourly_rental_cost_for_component(
            component_name, self.cfg) for component_name in index]

        return pd.Series(data, index=index)


class Solution(OptimizerSolutionBase):

    #: Optimizer.
    optimizer: Optimizer

    def _add_diagnostics_for_this_param(
            self, param: float, ds: xr.Dataset,
            da_cf: xr.DataArray) -> xr.Dataset:
        """Add diagnostics with VRE to dataset.

        :param param: Quadratic cost-function coefficient.
        :param ds: Solution dataset.
        :param da_cf: Capacity factor.

        :returns: Dataset with diagnostics with VRE.
        """
        src_in = self.optimizer.input
        ds['generation'] = support.get_vre_generation(ds['capacity'], da_cf)
        ds['mean_penetration'] = support.get_mean_penetration(
            ds['generation'], src_in['demand'])
        ds['residual'] = support.get_residual(
            ds['generation'], src_in['demand'])

        return ds

    def get_data_postfix(self, **kwargs) -> str:
        """Get optimization results postfix with constraints in addition
        to default postfix.

        :returns: Postfix.
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get default postfix
            postfix_safe = super(Solution, self).get_data_postfix(**kwargs)

            capmax = self.cfg['constraint'].get('capacity_max')
            if capmax:
                postfix_safe += ''.join(
                    '_capmax{}'.format(v)
                    for v in tools.ensure_collection(capmax, list))
        else:
            postfix_safe = str(postfix)

        return postfix_safe


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
