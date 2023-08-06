"""Support functions for optimization."""
from collections import OrderedDict
import numpy as np
from orderedset import OrderedSet
import pandas as pd
import typing as tp
import xarray as xr
import pyomo.environ as pyo
from pyomo.opt.results import SolverResults
import e4clim
import e4clim.config as e4cfg
from e4clim.container.optimizer import OptimizerBase
import e4clim.typing as e4tp
from e4clim.utils import tools


MethodType = tp.Callable[[float], float]


def get_data(func):
    """Get data decorator."""

    def inner(self, *args, **kwargs):
        self.get_data(**kwargs)
        return func(self, *args, **kwargs)

    return inner


def update_solution_variables(
        solution:
        'e4clim.container.optimizer_data_source.OptimizerSolutionBase',
        variable_dims: e4tp.StrIterableType, cfg: e4tp.CfgType,
        **kwargs) -> None:
    """Update solution variables.

    :param solution: Solution.
    :param variable_dims: Variable-dimensions mapping.
    :param cfg: Configuration.
    """
    # Add state variables
    solution.update_variables(variable_dims)

    # Add requested dual or rc variables if any
    cfg_display = cfg.get('display') or {}
    for suffix_name, variable_names in cfg_display.items():
        prefix = suffix_name + '__'
        variable_names = tools.ensure_collection(variable_names) or []
        variable_names = [prefix + variable_name
                          for variable_name in variable_names]
        # Add duals to solution variables
        solution.update_variables(variable_names)


def parse_solution(
        model: pyo.ConcreteModel, variable_dims: e4tp.StrIterableType,
        cfg: e4tp.CfgType, **kwargs) -> xr.Dataset:
    """Parse solution into a dataset of arrays.

    :param model: Model.
    :param variable_dims: Variable-dimensions mapping.
    :param cfg: Configuration.

    :returns: Dataset.
    """
    ds = xr.Dataset()

    # Parse state variables
    kwargs = kwargs.copy()
    kwargs['variable_names'] = variable_dims
    ds.update(_parse_variables(model, pyo.value, **kwargs))

    # Parse duals
    ds.update(_parse_suffixes(model, cfg, **kwargs))

    return ds


def _parse_suffixes(model: pyo.ConcreteModel, cfg: e4tp.CfgType,
                    **kwargs) -> dict:
    """Parse suffixes.

    :param model: Model.
    :param cfg: Configuration.

    :returns: Dataset.
    """
    ds = {}
    cfg_display = cfg.get('display') or {}
    kwargs = kwargs.copy()
    for suffix_name, variable_names in cfg_display.items():
        # Get dataset
        suffix = getattr(model, suffix_name)
        prefix = suffix_name + '__'
        kwargs['variable_names'] = variable_names
        ds_new = _parse_variables(model, suffix.get, prefix=prefix, **kwargs)

        # Add to dataset with opposite sign
        ds.update({da_name: -da for da_name, da in ds_new.items()})

    return ds


def _parse_variables(
        model: pyo.ConcreteModel, method: MethodType,
        variable_names: e4tp.StrIterableType, prefix: str = '',
        **kwargs) -> dict:
    """Parse reduced costs.

    :param model: Model.
    :parma method: Method to access variable values.
    :parm suffix: Suffix.
    :param variable_names: Variable name.
    :param prefix: Prefix string to prepend to variable names.

    :returns: Dataset.
    """
    ds = {}
    variable_names = tools.ensure_collection(
        variable_names, OrderedSet) or OrderedSet
    for variable_name in variable_names:
        if hasattr(model, variable_name):
            # Get data array for variable
            variable = getattr(model, variable_name)
            da = _get_dataarray(method, variable, prefix=prefix, **kwargs)

            # Add cost from objective if possible
            try:
                da.attrs['cost_objective'] = pyo.value(model.cost)
            except ValueError:
                pass

            # Add to dataset
            ds[da.name] = da

    return ds


def _get_dataarray(method: MethodType, variable: pyo.Var, prefix: str = '',
                   **kwargs) -> xr.DataArray:
    """Parse reduced costs.

    :parma method: Method to access variable values.
    :param variable: Variable.
    :param prefix: Prefix string to prepend to variable names.

    :returns: Data array.
    """
    index_set = variable.index_set()
    if index_set.dimen > 1:
        data, index, names = _get_data_for_multiindex(
            method, variable, index_set)
    else:
        data, index, names = _get_data_for_singleindex(
            method, variable, index_set)

    # Get data frame
    df = pd.DataFrame(data, index=index)[0]
    df = df.unstack() if len(names) > 1 else df

    # Return data array
    array_name = prefix + variable.name
    return xr.DataArray(df, name=array_name)


def _get_data_for_multiindex(
        method: MethodType, variable: pyo.Var, index_set:
        pyo.Set) -> tp.Tuple[tp.List[float], pd.MultiIndex, tp.List[str]]:
    """Get data for multi-index.

    :parma method: Method to access variable values.
    :param variable: Variable.
    :param index_set: Index set.

    :returns: Data, index and names.
    """
    names = [idx.name for idx in index_set.subsets()]
    indices = [pd.Index(idx) for idx in index_set.subsets()]
    index = pd.MultiIndex.from_product(indices, names=names)
    data = [method(variable[idx]) for idx in index]

    return data, index, names


def _get_data_for_singleindex(
        method: MethodType, variable: pyo.Var, index_set:
        pyo.Set) -> tp.Tuple[tp.List[float], pd.Index, tp.List[str]]:
    """Get data for single-index.

    :parma method: Method to access variable values.
    :param variable: Variable.
    :param index_set: Index set.

    """
    names = [index_set.name]
    index = pd.Index(index_set, name=index_set.name)
    data = [method(variable[idx]) for idx in index]

    return data, index, names


def save_dict(di: dict, ds: xr.Dataset, prefix: str = '') -> None:
    """Save a(multi-level) dictionary to a dataset's attributes.

    :param di: Dictionary to save.
      Multi-level dictionaries are flattened and child keys are prefixed
      by parent key.
    :param ds: Dataset in which to save dictionary.
    :param prefix: Prefix to append to child keys of dictionary.
    """
    for key, value in di.items():
        if value is None:
            continue
        elif isinstance(value, bool):
            value = int(value)
        elif isinstance(value, dict):
            save_dict(value, ds, prefix=(key + '_'))
        else:
            ds.attrs[prefix + key] = value


class OptimizerInputComponentsParserMixin:
    """Mix to
    :py:class:`e4clim.container.optimizer_data_source.OptimizerInputBase`
    to add available-components parsing functionalities."""
    #: Demand component manager.
    context_component_demand: (
        'e4clim.context.context_component.ContextComponent')

    #: Generation component contexts.
    context_component_generation: tp.MutableMapping[
        str, 'e4clim.context.context_component.ContextComponent']

    #: Generation component names.
    component_generation_names: tp.MutableSet[str]

    def parse_available_components(
            self, regional: bool = False, dem_conv: float = 1.,
            **kwargs) -> tp.MutableMapping[str, pd.DataFrame]:
        """Load available components.

        :param regional: Whether data is regional.
        :param dem_conv: Factor to apply to the demand data.

        :returns: Input data.
        """
        if self.context_component_demand is not None:
            variable_name = 'demand'
            result_mng = self.context_component_demand[variable_name]
            kwargs['variable_component_names'] = {variable_name}
            da_dem = result_mng.get_data(**kwargs)[variable_name]

            # Select period
            start_date = pd.Timestamp(self.cfg['start_date'])
            end_date = pd.Timestamp(
                self.cfg['end_date']) - pd.Timedelta('1 second')
            time_slice = slice(start_date, end_date)
            da_dem = da_dem.sel(time=time_slice)

        if self.context_component_generation is not None:
            # Get capacity factors
            da_list = []
            variable_name = 'capacityfactor'
            for context_component in (
                    self.context_component_generation.values()):
                # Select component results for output variable
                result_mng = context_component.context_results[variable_name]
                kwargs['variable_component_names'] = {variable_name}
                da_comp = result_mng.get_data(**kwargs)[variable_name]

                # Make sure that data contains only this component
                if 'component' in da_comp.dims:
                    da_comp = da_comp.sel(
                        component=context_component.component_name, drop=True)

                # Expand dimension
                da_comp = da_comp.expand_dims(
                    {'component': [context_component.component_name]})
                da_list.append(da_comp)
            da_cf = xr.concat(da_list, dim='component')

            # Select period
            start_date = pd.Timestamp(self.cfg['start_date'])
            end_date = pd.Timestamp(
                self.cfg['end_date']) - pd.Timedelta('1 second')
            time_slice = slice(start_date, end_date)
            da_cf = da_cf.sel(time=time_slice)

            # Rename component to vre to avoid model conflicts
            da_cf = da_cf.rename(component='vre')

        if (self.context_component_demand is not None) and (
                self.context_component_generation is not None):
            # Select common time-slice between demand and capacity factors
            common_index = da_dem.indexes['time']
            common_index = common_index.intersection(da_cf.indexes['time'])
            da_dem = da_dem.sel(time=common_index)
            da_cf = da_cf.sel(time=common_index)
            self.info('{}-{} period selected'.format(
                *da_cf.indexes['time'][[0, -1]].to_list()))

        # Sub-sample, if needed
        if self.med.cfg['frequency'] == 'day':
            if self.optimizer.context_component_demand is not None:
                da_dem = da_dem.resample(time='D').sum('time')
            if self.context_component_generation is not None:
                da_cf = da_cf.resample(time='D').mean('time')
        if self.med.cfg['frequency'] == 'month':
            if self.optimizer.context_component_demand is not None:
                da_dem = da_dem.resample(time='M').sum('time')
            if self.context_component_generation is not None:
                da_cf = da_cf.resample(time='M').mean('time')

        ds = OrderedDict()
        if self.context_component_demand is not None:
            # Try to select component in case needed
            try:
                da_dem = da_dem.sel(
                    component=self.context_component_demand.component_name)
            except (KeyError, ValueError):
                pass

            # Get total demand
            da_dem = da_dem.sum('region')

            # Convert demand units
            da_dem *= dem_conv

            # Set time index
            self.time = da_dem.indexes['time']

            # Add to dataset as series
            ds['demand'] = da_dem.to_pandas()
            ds['demand'].index.name = 'time'

        if self.context_component_generation:
            # Remove invalid values
            da_cf = da_cf.where(~da_cf.isnull(), 0.)

            # Set time index
            self.time = da_cf.indexes['time']

            if regional:
                # Add to dataset as multi-indexed series
                ds['capacityfactor'] = da_cf.stack(stacked=[
                    'vre', 'region', 'time']).to_pandas()
            else:
                if self.capacity_vre is None:
                    # Set uniform VRE mix
                    self.capacity_vre = xr.ones_like(
                        da_cf.isel(time=0, drop=True))

                # Average total capacity factors
                _, weights = xr.broadcast(da_cf, self.capacity_vre)
                da_cf_total = da_cf.reduce(
                    np.average, ['region'], weights=weights)
                ds['capacityfactor'] = da_cf_total.transpose(
                    'vre', 'time').to_pandas().stack()

        return ds


CoordsType = tp.MutableMapping[str, tp.Tuple[str, tp.Sequence]]
CstrType = tp.Tuple[tp.Sequence[str], tp.Callable[..., pyo.Expression]]
CstrDefType = tp.MutableMapping[str, CstrType]
VariableDimsType = tp.MutableMapping[str, tp.MutableSet[str]]


class OptimizerWithPyomo(OptimizerBase):
    """Adds functionalities to solve with :py:class:`pyomo`
    to :py:class:`e4clim.container.optimizer.OptimizerBase`."""

    #: Constraint definitions as dictionnary from constraint name
    #: to a tuple with a list of sets and a rule function.
    _constraint_definitions: CstrDefType

    #: Coordinates.
    coords: CoordsType

    #: Cost rule.
    _cost_rule: tp.Callable[..., pyo.Expression]

    #: Variance weight.
    param: float

    #: Parent container.
    parent: 'e4clim.context.context_optimizer.ContextSingleOptimizer'

    #: Results.
    results: SolverResults

    #: Sets.
    _set_names: tp.MutableSet[str]

    #: Variable dimensions.
    variable_dims: VariableDimsType

    def __init__(self, parent:
                 'e4clim.context.context_optimizer.ContextOptimizerBase',
                 name: str, cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Build optimizer context.

        :param app: Context application.
        :param cfg: Optimizer configuration.
        """
        super(OptimizerWithPyomo, self).__init__(
            parent, name, cfg=cfg, **kwargs)

        #: Coordinates.
        self.coords = OrderedDict()

        #: Constraint definitions as dictionnary from constraint name
        #: to a tuple with a list of sets and a rule function.
        self._constraint_definitions = {}

    def solve(self, **kwargs) -> e4tp.DatasetType:
        """Solve optimization problem.

        :returns: Solution dataset.
        """
        self._set_variable_dims()

        self._set_constraints()

        self._set_cost_rule()

        model = self._build_model()

        solver, tee = self._build_solver()

        ds = self._solve_for_each_param(model, solver, tee)

        ds = self.add_diagnostics_for_each_param(ds)

        return ds

    def _set_cost_rule(self) -> None:
        """Set cost rule. By default, just verify that `_cost_rule`
        is a static attribute method."""
        assert hasattr(self, '_cost_rule'), (
            '"_cost_rule" attribute method required')

    def _build_model(self) -> pyo.ConcreteModel:
        """Build model."""
        model = pyo.ConcreteModel()

        self._update_sets_coords(model)
        self._update_state_variables(model)
        self._add_constraints_to_model(model)

        # Create a 'dual' suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

        return model

    def _update_sets_coords(self, model: pyo.ConcreteModel) -> None:
        """Update sets, coordinates with loaded input.

        :param model: Model.
        """
        # Update sets and coordinates with loaded input (for time index)
        for set_name in self._set_names:
            s = pyo.Set(ordered=True, initialize=getattr(
                self.input, set_name))
            setattr(model, set_name, s)
            self.coords[set_name] = set_name, s.ordered_data()

    def _update_state_variables(self, model: pyo.ConcreteModel) -> None:
        """Update state variables.

        :param model: Model.
        """
        for variable_name in self.variable_dims:
            getattr(self, '_update_' + variable_name)(model)

    def _add_constraints_to_model(self, model: pyo.ConcreteModel) -> None:
        """Add constraints to model.

        :param model: Model.
        """
        self.info('Defining constraints')
        for cstr_name, cstr_def in self._constraint_definitions.items():
            indices = [getattr(model, dim) for dim in cstr_def[0]]
            constraint = pyo.Constraint(*indices, rule=cstr_def[1])
            setattr(model, cstr_name, constraint)

    def _build_solver(self) -> tp.Tuple[pyo.SolverFactory, bool]:
        """Build solver.

        :param optimizer: Optimizer.

        :returns: Solver and solver-verbose flag.
        """
        options = None
        cfg_solver = self.cfg.get('solver')
        if cfg_solver is not None:
            solver_name = tools.get_required_str_entry(
                cfg_solver, 'name', 'ipopt')
            options = tools.get_mapping_entry(cfg_solver, 'options')
        solver = pyo.SolverFactory(solver_name)

        tee = self._set_solver_options(solver, options)

        return solver, tee

    def _set_solver_options(
            self, solver: pyo.SolverFactory,
            options: tp.Mapping[str, tp.Any] = None) -> bool:
        """Set solver options.

        :param solver: Solver.
        :param options: Options.

        :returns: Verbose flag.
        """
        if options is not None:
            for opt, val in options.items():
                solver.options[opt] = val
        tee = not self.cfg.get('no_verbose')

        return tee

    def _solve_for_each_param(
            self, model: pyo.ConcreteModel, solver: pyo.SolverFactory,
            tee: bool) -> xr.Dataset:
        """Solve for each control-parameter value.

        :param model: Model.
        :param solver: Solver.
        :param tee: Verbose mode.

        :returns: Solution dataset.
        """
        param_rng = e4cfg.get_param_rng(self.cfg, self.param_name)

        ds = xr.Dataset()
        for param in param_rng:
            self.param = param
            self._solve_for_this_param(model, solver, tee)

            ds = self._add_solution_for_param(ds, model)

        return ds

    def _solve_for_this_param(
            self, model: pyo.ConcreteModel, solver: pyo.SolverFactory,
            tee: bool) -> None:
        """Solve for each control-parameter value.

        :param model: Model.
        :param solver: Solver.
        :param tee: Verbose mode.
        """
        self.info('Solving for {} = {:.2e}'.format(
            self.param_name, self.param))

        if hasattr(self, '_set_param_dependent_constraints'):
            self._set_param_dependent_constraints(model)

        self.info('Defining cost')
        model.del_component('cost')
        model.cost = pyo.Objective(rule=self._cost_rule)

        self.info('Solving optimization problem')
        self.results = solver.solve(model, tee=tee)

        self._check_status()

    def add_diagnostics_for_each_param(
            self, ds: xr.Dataset = None,
            df_cf: pd.core.generic.NDFrame = None) -> xr.Dataset:
        """Update solution with diagnostics for each control-parameter value.

        :param ds: Solution dataset.
        :param df_cf: Alternative capacity factors.

        :returns: Solution dataset with diagnostics.
        """
        self.info('Adding diagnostics for all parameter values')

        if ds is None:
            ds = self.solution.data

        # Get capacity factors from input as data array
        if df_cf is None:
            df_cf = self.input.capacityfactor
        da_cf = xr.DataArray(df_cf).unstack().sel(
            region=ds['capacity'].region).rename(vre='component')

        # Add diagnostics
        ds_with = xr.Dataset()
        param_name = self.param_name
        for param in ds['capacity'].indexes[param_name]:
            # Select data for param
            ds_param = ds.sel(**{param_name: param})

            # Add diagnostics for param
            ds_param = self.solution._add_diagnostics_for_this_param(
                param, ds_param, da_cf)

            # Add param coordinate
            ds_param = ds_param.expand_dims({self.param_name: [param]})

            # Concatenate
            ds_with = (ds_param if not ds_with else
                       xr.concat([ds_with, ds_param], dim=param_name,
                                 data_vars='minimal'))

        # Add capacity-factor to dataset
        ds_with['capacityfactor'] = da_cf

        return ds_with

    def _check_status(self) -> None:
        """Check solver solution status."""
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


def get_vre_generation(
        capacity: xr.DataArray, capacityfactor: xr.DataArray) -> xr.DataArray:
    """Get VRE generation.

    :param capacity: Capacity.
    :param capacityfactor: Capacity factor.

    :returns: VRE generation.
    """
    return capacity * capacityfactor


def get_residual(vre_generation: xr.DataArray,
                 demand: pd.core.generic.NDFrame) -> xr.DataArray:
    """Get residual load from difference of load and VRE generation.

    :param vre_generation: VRE generation.
    :param demand: Demand.

    :returns: Residual demand.
    """
    vre_generation_total = vre_generation.sum(['component', 'region'])
    residual = xr.DataArray(demand) - vre_generation_total

    return residual


def get_mean_penetration(vre_generation: xr.DataArray,
                         demand: pd.core.generic.NDFrame) -> float:
    """Get mean penetration.

    :param vre_generation: VRE generation.
    :param demand: Demand.

    :returns: Mean penetration.
    """
    return vre_generation.sum(['component', 'region']).mean(
        'time') / demand.mean()
