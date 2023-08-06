"""Solution for cost minimization with residual load from dispatchable
production with (symmetric or not) quadratic variable costs."""
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import numpy as np
import pandas as pd
from pathlib import Path
import typing as tp
import xarray as xr
from e4clim.container.optimizer_data_source import OptimizerSolutionBase
import e4clim.typing as e4tp
from e4clim.utils.logging import LoggingContext
import e4clim.utils.optimization_support as support
from e4clim.utils import tools
from . import dqc_input
if tp.TYPE_CHECKING:
    from .. import dispatch_quadratic_cost


class Solution(OptimizerSolutionBase):

    #: Optimizer.
    optimizer: 'dispatch_quadratic_cost.Optimizer'

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

    def _add_diagnostics_for_this_param(
            self, param: float, ds: xr.Dataset,
            da_cf: xr.DataArray) -> xr.Dataset:
        """Add diagnostics to dataset.

        :param param: Quadratic cost-function coefficient.
        :param ds: Solution dataset.
        :param da_cf: Capacity factor.

        :returns: Dataset with diagnostics.
        """
        self.optimizer.input._add_novre_diagnostics_for_this_param(param, ds)

        self._add_vre_diagnostics_for_this_param(param, ds, da_cf)

        return ds

    def _add_vre_diagnostics_for_this_param(
            self, param: float, ds: xr.Dataset,
            da_cf: xr.DataArray) -> xr.Dataset:
        """Add diagnostics with VRE to dataset.

        :param param: Quadratic cost-function coefficient.
        :param ds: Solution dataset.
        :param da_cf: Capacity factor.

        :returns: Dataset with diagnostics with VRE.
        """
        src_in = self.optimizer.input

        dgmn = float(ds['dispatch_generation_max_novre'])
        ds['generation'] = support.get_vre_generation(ds['capacity'], da_cf)
        ds['mean_penetration'] = support.get_mean_penetration(
            ds['generation'], src_in.demand)
        ds['residual'] = support.get_residual(ds['generation'], src_in.demand)
        ds['rldc'] = self.get_residual_load_duration_curve(ds['residual'])
        ds['dispatch_generation'] = dqc_input._get_dispatch_generation(
            ds['residual'], dgmn)
        ds['lost_load'] = dqc_input._get_lost_load(ds['residual'], dgmn)
        ds['system_marginal_cost'] = dqc_input._get_system_marginal_cost(
            param, ds['dispatch_generation'], ds['lost_load'], src_in.voll)
        ds['constant_system_marginal_cost'] = (
            dqc_input._get_constant_system_marginal_cost(
                param, ds['residual']))
        ds['decoupled_system_marginal_cost'] = (
            dqc_input._get_decoupled_system_marginal_cost(
                param, src_in.demand))
        ds['mean_vre_total_cost_plant'] = (
            self.get_mean_vre_total_cost_plant(ds['capacity']))
        ds['mean_vre_total_cost'] = self.get_mean_vre_total_cost(
            ds['capacity'])
        ds['mean_vre_revenue_plant'] = self.get_mean_vre_revenue_plant(
            param, da_cf, ds['dispatch_generation'], ds['lost_load'])
        ds['mean_vre_revenue'] = self.get_mean_vre_revenue(
            param, ds['capacity'], da_cf, ds['dispatch_generation'],
            ds['lost_load'])
        ds['curtailed_energy_fraction'] = (
            dqc_input._get_curtailed_energy_fraction(
                ds['generation'], ds['residual']))
        ds['mean_dispatch_variable_cost'] = (
            dqc_input._get_mean_dispatch_variable_cost(
                param, ds['dispatch_generation']))
        ds['dispatch_fixed_cost_recommission'] = (
            dqc_input._get_dispatch_fixed_cost(
                param, ds['dispatch_generation'], dgmn, src_in.cfg))
        ds['mean_lost_load_cost'] = dqc_input._get_mean_lost_load_cost(
            ds['lost_load'], src_in.voll)
        ds['mean_dispatch_total_cost'] = (
            dqc_input._get_mean_dispatch_total_cost(
                param, src_in.cfg, mean_dispatch_variable_cost=float(
                    ds['mean_dispatch_variable_cost']),
                dispatch_fixed_cost=float(ds[
                    'dispatch_fixed_cost_novre'])))
        ds['mean_dispatch_revenue'] = dqc_input._get_mean_dispatch_revenue(
            ds['dispatch_generation'], ds['system_marginal_cost'])
        ds['mean_system_total_cost'] = self.get_mean_system_total_cost(
            param, src_in.cfg, src_in.voll, mean_vre_total_cost=float(
                ds['mean_vre_total_cost']),
            mean_dispatch_total_cost=float(ds['mean_dispatch_total_cost']),
            mean_lost_load_cost=float(ds['mean_lost_load_cost']))
        ds['constant_mean_system_total_cost'] = self.get_mean_system_total_cost(
            param, src_in.cfg, src_in.voll,
            mean_vre_total_cost=float(ds['mean_vre_total_cost']),
            dispatch_fixed_cost=float(ds['dispatch_fixed_cost_novre']),
            demand=src_in.demand,
            dispatch_generation=ds['residual'], problem='constant')
        ds['decoupled_mean_system_total_cost'] = self.get_mean_system_total_cost(
            param, src_in.cfg, src_in.voll,
            mean_vre_total_cost=float(ds['mean_vre_total_cost']),
            dispatch_fixed_cost=float(ds['dispatch_fixed_cost_novre']),
            demand=src_in.demand,
            dispatch_generation=ds['residual'], problem='decoupled')
        nt = len(src_in.ldc.peak_hour)
        lole_novre = int(ds['lolp_novre'] * nt + 0.1)
        ds['dispatch_generation_max_lole_as_novre'] = (
            self.get_dispatch_generation_max(ds['rldc'], lole_novre))
        ds['capacity_credit'] = self.get_capacity_credit(
            dgmn, float(ds['dispatch_generation_max_lole_as_novre']),
            ds['capacity'])
        ds['lcoe'] = self.get_lcoe(ds['capacity'], ds['generation'])
        if 'dual__c_capacity_max' in ds:
            ds['vre_marginal_rent'] = self.get_vre_marginal_rent(
                ds['capacity'], ds['generation'], ds['dual__c_capacity_max'])
        ds['value_factor_plant'] = dqc_input._get_value_factor_plant(
            da_cf, ds['system_marginal_cost'])
        ds['value_factor'] = self.get_value_factor(
            ds['generation'], ds['system_marginal_cost'])

        return ds

    def get_dispatch_generation_max(
            self, rldc: xr.DataArray, lole: float) -> float:
        """Get maximum dispatchable generation with VRE.

        :param rldc: Residual load duration curve.
        :param lole: Loss of Load Expectation over the period.

        :returns: Maximum dispatchable generation.
        """
        dispatch_generation_max = float(rldc[lole])

        return dispatch_generation_max

    def get_capacity_credit(
            self, dispatch_generation_max_novre: float,
            dispatch_generation_max_lole_as_novre: float,
            capacity: xr.DataArray) -> float:
        """Get capacity credit, i.e. the fraction of the dispatchable
        generation capacity that can be removed while preserving the
        loss of load expectation.

        :param dispatch_generation_max_novre: Maximum dispatchable generation
          without VRE.
        :param dispatch_generation_max_lole_as_novre: Maximum dispatchable
          generation for the loss of load expectation without VRE.
        :param capacity: VRE Capacity.

        :returns: Capacity credit.
        """
        return ((dispatch_generation_max_novre -
                 dispatch_generation_max_lole_as_novre) /
                capacity.sum(['component', 'region']))

    def get_residual_load_duration_curve(
            self, residual: xr.DataArray) -> xr.DataArray:
        """Get residual load duration curve.

        :param residual: Residual.

        :returns: Residual load duration curve.
        """
        peak_residual = residual.sortby(residual, ascending=False).values
        coord_hour = ('peak_hour', self.optimizer.input.ldc.peak_hour.data)
        rldc = xr.DataArray(peak_residual, coords=[coord_hour],
                            attrs=residual.attrs)

        return rldc

    def get_lcoe(self, capacity: xr.DataArray,
                 generation: xr.DataArray) -> xr.DataArray:
        """Get Levelized Cost of Electricity for VRE mix.

        :param capacity: Capacities.
        :param generation: VRE generation.

        :returns: Levelized Cost of Electricity for VRE mix.
        """
        hrc = xr.DataArray(self.input['hourly_rental_cost']).expand_dims(
            region=capacity['region'])
        cost = (hrc * capacity).sum(['component', 'region'])
        gen_mean = generation.sum(['component', 'region']).mean('time')
        lcoe = cost / gen_mean

        return lcoe

    def get_value_factor(self, generation: xr.DataArray,
                         system_marginal_cost: xr.DataArray) -> xr.DataArray:
        """Get value factor for VRE mix.

        :param generation: VRE generation.
        :param system_marginal_cost: System marginal cost.

        :returns: Value factor for VRE mix.
        """
        gen_tot = generation.sum(['component', 'region'])
        value_factor = (gen_tot * system_marginal_cost).mean('time')
        gen_mean = gen_tot.mean('time')
        value_factor /= gen_mean * system_marginal_cost.mean('time')
        fact = len(generation['component']) * len(generation['region'])

        return value_factor.where(gen_mean > dqc_input.TOL * fact)

    def get_vre_marginal_rent(
            self, capacity: xr.DataArray, generation: xr.DataArray,
            dual__c_capacity_max: xr.DataArray) -> xr.DataArray:
        """Get marginal rent for VRE mix.

        :param capacity: Capacities.
        :param generation: VRE generation.
        :param dual__c_capacity_max: Duals of maximum VRE capacity
          constraints, i.e. economic rents for VRE plants.

        :returns: Rent.
        """
        rent = (dual__c_capacity_max * capacity).sum(['component', 'region'])
        gen_mean = generation.sum(['component', 'region']).mean('time')
        marginal_rent = rent / dqc_input.YEAR_TO_HOUR / gen_mean

        return marginal_rent

    def get_mean_vre_total_cost(self, capacity: xr.DataArray) -> float:
        """Get mean yearly VRE total cost (yearly rental cost).

        :param capacity: Capacities.

        :returns: Mean VRE cost.
        """
        return float(self.get_mean_vre_total_cost_plant(
            capacity).dot(capacity))

    def get_mean_vre_total_cost_plant(
            self, capacity: xr.DataArray) -> xr.DataArray:
        """Get mean yearly VRE cost per plant (yearly rental cost).

        :param capacity: Capacities.

        :returns: Mean VRE cost per plant.
        """
        rental_cost = xr.DataArray(self.optimizer.input['hourly_rental_cost'])
        coords = [('region', capacity.region.data),
                  ('component', capacity.component.data)]
        data = [rental_cost.sel(component=capacity.component)] * len(
            capacity.region)

        return xr.DataArray(data, coords=coords).transpose(
            'component', 'region') * dqc_input.YEAR_TO_HOUR

    def get_mean_vre_revenue(
            self, alpha: float, capacity: xr.DataArray,
            capacity_factor: xr.DataArray, dispatch_generation: xr.DataArray,
            lost_load: xr.DataArray) -> xr.DataArray:
        """Get mean VRE revenue.

        :param alpha: Quadratic cost-function coefficient.
        :param capacity: Capacities.
        :param capacity_factor: Capacity factors.
        :param dispatch_generation: Dispatch_Generation demand.
        :param lost_load: Lost load.

        :returns: Mean VRE revenue.
        """
        mean_vre_revenue_plant = self.get_mean_vre_revenue_plant(
            alpha, capacity_factor, dispatch_generation, lost_load)
        mean_vre_revenue = mean_vre_revenue_plant.dot(capacity)

        return mean_vre_revenue

    def get_mean_vre_revenue_plant(
            self, alpha: float, capacity_factor: xr.DataArray,
            dispatch_generation: xr.DataArray,
            lost_load: xr.DataArray) -> xr.DataArray:
        """Get mean yearly VRE revenue per plant.

        :param alpha: Quadratic cost-function coefficient.
        :param capacity_factor: Capacity factors.
        :param dispatch_generation: Dispatch_Generation demand.
        :param lost_load: Lost load.

        :returns: Mean yearly VRE revenue per plant.
        """
        # Get system cost
        voll = self.optimizer.input.voll
        system_marginal_cost = dqc_input._get_system_marginal_cost(
            alpha, dispatch_generation, lost_load, voll)

        # Get VRE revenue for each plant
        mean_vre_revenue_plant = (system_marginal_cost *
                                  capacity_factor).mean('time')

        return mean_vre_revenue_plant * dqc_input.YEAR_TO_HOUR

    def get_mean_system_total_cost(
            self, alpha: float, cfg: e4tp.CfgType, voll: float,
            capacity: xr.DataArray = None,
            dispatch_generation: xr.DataArray = None,
            lost_load: xr.DataArray = None,
            dispatch_generation_max_novre: float = None,
            mean_dispatch_variable_cost: float = None,
            dispatch_fixed_cost: float = None,
            mean_lost_load_cost: float = None,
            mean_vre_total_cost: float = None,
            mean_dispatch_total_cost: float = None,
            demand: pd.Series = None, problem: str = 'variable') -> float:
        """Get mean total cost (VRE, dispatch and lost load).

        :param alpha: Quadratic cost-function coefficient.
        :param cfg: Input configuration.
        :param voll: Value of Lost Load.
        :param capacity: Capacities.
          If `None`, :py:obj`mean_vre_total_cost` should be given.
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
        :param mean_vre_total_cost: VRE total cost.
          If `None`, :py:obj:`capacity` should be given to compute it.
        :param mean_dispatch_total_cost: Dispatch total cost.
          If `None`, other arguments should be given to compute it.
        :param demand: Demand.
          Should not be `None` if :py:obj:`problem` equals `'decoupled'`.
        :param problem: Optimization-problem type.

        :returns: Mean system total cost for problem.
        """
        if mean_vre_total_cost is None:
            assert capacity is not None, (
                '"capacity" argument should be given when'
                '"mean_vre_total_cost" is not')
            mean_vre_total_cost = self.get_mean_vre_total_cost(
                capacity)

        mean_system_total_except_vre_cost = (
            dqc_input._get_mean_system_total_cost_novre(
                alpha, cfg, voll,
                dispatch_generation=dispatch_generation,
                lost_load=lost_load,
                dispatch_generation_max_novre=dispatch_generation_max_novre,
                mean_dispatch_variable_cost=mean_dispatch_variable_cost,
                dispatch_fixed_cost=dispatch_fixed_cost,
                mean_lost_load_cost=mean_lost_load_cost,
                mean_dispatch_total_cost=mean_dispatch_total_cost,
                demand=demand, problem=problem))

        return mean_system_total_except_vre_cost + mean_vre_total_cost

    def get_dispatch_distribution(
            self, alpha_list: tp.Collection,
            loadpoints: tp.Union[int, tp.Sequence],
            read: bool = False, n_jobs: int = None, **kwargs) -> xr.Dataset:
        """Compute properties for all dispatch plants and for different
        values of alpha.

        :param alpha_list: Sequence of quadratic cost-function coefficients.
        :param loadpoints: load points or number of load points.
        :param read: Whether to read previously computed data or not.
        :param n_jobs: Number of parallel jobs to run.
          If `None`, the number of jobs is chosen as the number of cores.

        :returns: Dispatch-distribution dataset.
        """
        src_in = self.optimizer.input
        ds = self.data
        data_dir = self.get_data_directory()
        postfix = self.get_data_postfix()
        if isinstance(loadpoints, tp.Sized):
            n_prod = len(loadpoints)
        else:
            n_prod = loadpoints
            loadpoints = np.linspace(
                0., ds['dispatch_generation_max_novre'].max(), n_prod)
        filename = '{}_{}_step{}{}.nc'.format(
            self.name, 'effects', n_prod, postfix)
        effects_filepath = Path(data_dir, filename)
        if not read:
            # Compute merit-order effects for each alpha in parallel
            verbose = not bool(self.optimizer.cfg.get('no_verbose'))
            n_jobs = n_jobs or np.min([cpu_count(), len(alpha_list)])
            func = self.get_merit_order_effects_at_loadpoint

            if n_jobs > 1:
                # Get data in parallel
                data = Parallel(n_jobs=n_jobs, verbose=verbose)(
                    delayed(
                        src_in.get_costs_dispatch_distribution_for_alpha)(
                            alpha, ds.sel(alpha=alpha, method='nearest'),
                            loadpoints)
                    for alpha in alpha_list)
                ds_dis = xr.concat(data, dim='alpha')

                data = Parallel(n_jobs=n_jobs, verbose=verbose)(
                    delayed(self.get_optimal_dispatch_capacity_for_alpha)(
                        ds.sel(alpha=alpha, method='nearest'),
                        ds_dis.sel(alpha=alpha, method='nearest'))
                    for alpha in alpha_list)
                ds_dis = ds_dis.merge(xr.concat(data, dim='alpha'))

                data = Parallel(n_jobs=n_jobs, verbose=verbose)(
                    delayed(dqc_input.get_dispatch_distribution_for_alpha)(
                        func, alpha, ds.sel(alpha=alpha, method='nearest'),
                        ds['rldc'], loadpoints, **kwargs)
                    for alpha in alpha_list)
                ds_dis = ds_dis.merge(xr.concat(data, dim='alpha'))
            else:
                # Get data in serial
                data = [src_in.get_costs_dispatch_distribution_for_alpha(
                    alpha, ds.sel(alpha=alpha, method='nearest'),
                    loadpoints) for alpha in alpha_list]
                ds_dis = xr.concat(data, dim='alpha')

                data = [self.get_optimal_dispatch_capacity_for_alpha(
                        ds.sel(alpha=alpha, method='nearest'),
                        ds_dis.sel(alpha=alpha, method='nearest'))
                        for alpha in alpha_list]
                ds_dis = ds_dis.merge(xr.concat(data, dim='alpha'))

                data = [dqc_input.get_dispatch_distribution_for_alpha(
                    func, alpha, ds.sel(alpha=alpha, method='nearest'),
                    ds['rldc'], loadpoints, **kwargs)
                    for alpha in alpha_list]
                ds_dis = ds_dis.merge(xr.concat(data, dim='alpha'))

            # Save dataset
            ds_dis.to_netcdf(effects_filepath)
        else:
            ds_dis = xr.load_dataset(effects_filepath)

        return ds_dis

    def get_merit_order_effects_at_loadpoint(
            self, alpha: float, loadpoint: float, ds: xr.Dataset,
            rccdf: xr.DataArray) -> xr.Dataset:
        """Get wholesale price effect, utilization effect and fixed cost
        for dispatch plant at load point.

        :param alpha: Quadratic cost-function coefficient.
        :param loadpoint: load point above which plant is active.
        :param ds: Solution dataset.
        :param rccdf: Residual complementary CDF.

        :returns: Dispatch distribution of startup fraction,
          wholesale price effect, utilization effect,
          mean system marginal cost with and without VRE, utilization with and
          without VRE for dispatch plant.
        """
        ds_dis = xr.Dataset()

        (ds_dis['utilization_effect'], ds_dis['utilization_novre'], ds_dis[
            'utilization'], peak_hour_at_energy,
         residual_peak_hour_at_energy) = (
             self.get_utilization_effect_at_loadpoint(loadpoint, rccdf))

        src_in = self.optimizer.input
        ds_dis['mean_system_marginal_cost_novre'] = (
            self.get_mean_system_marginal_cost_at_loadpoint(
                alpha, src_in.ldc, peak_hour_at_energy,
                ds['dispatch_generation_max_novre']))

        ds_dis['mean_system_marginal_cost'] = (
            self.get_mean_system_marginal_cost_at_loadpoint(
                alpha, ds['rldc'], residual_peak_hour_at_energy,
                ds['dispatch_generation_max_novre']))

        marginal_cost = dqc_input.GET_DISPATCH_MARGINAL_COST(
            loadpoint, alpha)
        ds_dis['wholesale_price_effect'] = (
            self.get_wholesale_price_effect_at_loadpoint(
                ds_dis['mean_system_marginal_cost_novre'],
                ds_dis['mean_system_marginal_cost'], marginal_cost,
                ds_dis['utilization_effect']))

        # Get startup fractions
        ds_dis['startup_fraction'] = self.get_startup_fraction_at_loadpoint(
            loadpoint, ds['residual'], ds_dis['utilization'])

        return ds_dis.expand_dims('loadpoint').assign_coords(
            energy=[loadpoint])

    def get_wholesale_price_effect_at_loadpoint(
            self, mean_system_marginal_cost_novre: float,
            mean_system_marginal_cost: float, marginal_cost: float,
            utilization_effect: float) -> float:
        """Get wholesale price effect for dispatch plant at load point.

        :param mean_system_marginal_cost_novre: Mean system cost for dispatch
          plant at load point without VRE.
        :param mean_system_marginal_cost: Mean system cost for dispatch
          plant at load point with VRE.
        :param marginal_cost: Marginal cost of dispatchable generation.
        :param utilization_effect: Utilization effect for dispatch plant at
          load point.

        :returns: Wholesale price effect at load point.
        """
        if np.abs(utilization_effect - 1) < dqc_input.TOL:
            wholesale_price_effect = 0.
        else:
            wholesale_price_effect = (
                (1. - mean_system_marginal_cost /
                 mean_system_marginal_cost_novre) * (1 - utilization_effect) *
                (1. / (1. - marginal_cost / mean_system_marginal_cost_novre)))

        return wholesale_price_effect

    def get_mean_system_marginal_cost_at_loadpoint(
            self, alpha: float, ldc: xr.DataArray, peak_hour_at_energy: float,
            dispatch_generation_max_novre: float) -> float:
        """Get mean system cost for dispatch plant at load point.

        :param alpha: Quadratic cost-function coefficient.
        :param ldc: (Residual) load duration curve.
        :param peak_hour_at_energy: (Residual) peak hour at load point.
        :param dispatch_generation_max_novre: Maximum dispatchable generation.

        :returns: Mean system cost.
        """
        # Get LDC above load point
        ldc_above_loadpoint = ldc.sel(
            peak_hour=slice(None, peak_hour_at_energy))

        # Get lost load corresponding to LDC above load point
        lost_load_above_loadpoint = (ldc_above_loadpoint
                                     - dispatch_generation_max_novre)
        lost_load_above_loadpoint = lost_load_above_loadpoint.where(
            lost_load_above_loadpoint >= 0, 0)
        dispatch_generation_above_loadpoint = (
            ldc_above_loadpoint - lost_load_above_loadpoint)
        voll = self.optimizer.input.voll
        system_marginal_cost = dqc_input._get_system_marginal_cost(
            alpha, dispatch_generation_above_loadpoint,
            lost_load_above_loadpoint, voll)

        with LoggingContext('py.warnings', level='ERROR'):
            mean_system_marginal_cost = system_marginal_cost.mean(
                'peak_hour')

        return float(mean_system_marginal_cost)

    def get_startup_fraction_at_loadpoint(
            self, loadpoint: float, load: xr.DataArray,
            utilization: float) -> float:
        """Get fraction of utilized hours which are start-ups
        for dispatch plant at load point.

        :param loadpoint: load point above which plant is active.
        :param load: (Residual) load.
        :param utilization: Utilization.

        :returns: Start-up fraction knowing utilization.
        """
        capacityfactor = (load >= loadpoint).astype(int)
        isup = (capacityfactor[1:].values - capacityfactor[:-1].values) > 0
        startup_fraction = (isup.sum() / (len(isup) + 1) / utilization
                            if utilization > 0 else np.nan)

        return startup_fraction

    def get_utilization_effect_at_loadpoint(
            self, loadpoint: float,
            rccdf: xr.DataArray) -> tp.Tuple[
                float, float, float, float, float]:
        """Get fraction of utilization reduction from without VRE to with
        VRE at load point.

        :param loadpoint: load point above which plant is active.
        :param rccdf: Residual complementary CDF.

        :returns: Utilization effect, utilization without VRE and
          utilization at load point.
        """
        utilization_novre, peak_hour_at_energy = (
            dqc_input._get_utilization_at_loadpoint(
                loadpoint, self.optimizer.input.ccdf))

        utilization, residual_peak_hour_at_energy = (
            dqc_input._get_utilization_at_loadpoint(
                loadpoint, rccdf, loadpoint_label='residual_loadpoint'))

        utilization_effect = 1. - utilization / utilization_novre

        return (utilization_effect, utilization_novre, utilization,
                peak_hour_at_energy, residual_peak_hour_at_energy)

    def get_optimal_dispatch_capacity_for_alpha(
            self, ds: xr.Dataset, ds_dis: xr.Dataset) -> xr.Dataset:
        """Get optimal dispatchable capacity distribution for
        (residual) load duration curve.

        :param ds: Solution dataset.
        :param ds_dis: Dispatch-distribution dataset.

        :returns: Optimal dispatchable capacity distribution and
          corresponding costs.
        """
        ds_opt = xr.Dataset()
        rldc = ds['rldc']
        nt = len(rldc['peak_hour'])

        # Sort by marginal cost
        marginal_cost = ds_dis['marginal_cost'].sortby(ds_dis['marginal_cost'])
        rental_cost = ds_dis['rental_cost'].sortby(ds_dis['marginal_cost'])

        # Assign number as coordinate
        n_prod = len(rental_cost['loadpoint'])
        producers = np.arange(n_prod)
        marginal_cost = marginal_cost.rename(
            loadpoint='producer').assign_coords(producer=producers)
        rental_cost = rental_cost.rename(
            loadpoint='producer').assign_coords(producer=producers)

        # Initialize optimal solution
        opt_dispatch_capacity = xr.ones_like(marginal_cost) * np.nan

        # Add VoLL
        voll = self.optimizer.input.voll
        da_voll = xr.DataArray([voll], coords=[('producer', [n_prod])])
        da_zero = xr.DataArray([0.], coords=[('producer', [n_prod])])
        marginal_cost = xr.concat([marginal_cost, da_voll], dim='producer')
        rental_cost = xr.concat([rental_cost, da_zero], dim='producer')

        producer_prev = 0
        prob_ref = rldc[rldc > 0][-1]['peak_hour'] / nt
        prob_prev = prob_ref
        totcap_prev = 0.
        peak_producers = marginal_cost['producer'].values[1:]
        while producer_prev < n_prod:
            # Get optimal dispatch probabilities with respect to i
            peak_marginal_cost = marginal_cost.sel(producer=peak_producers)
            peak_rental_cost = rental_cost.sel(producer=peak_producers)
            marginal_cost_i = marginal_cost.sel(producer=producer_prev)
            rental_cost_i = rental_cost.sel(producer=producer_prev)
            prob_i = _get_optimal_dispatch_probability(
                marginal_cost_i, rental_cost_i,
                peak_marginal_cost, peak_rental_cost)

            # Get index of producer with maximum probability
            i_max = prob_i.argmax()
            producer_max = peak_producers[i_max]
            prob_max = prob_i.sel(producer=producer_max)

            # Check if utilization higher than for previous producer
            if producer_max < n_prod:
                if prob_max < prob_prev:
                    cap = rldc.sel(
                        peak_hour=prob_max * nt, method='ffill') - totcap_prev
                    opt_dispatch_capacity.loc[
                        {'producer': producer_prev}] = cap
                    totcap_prev += cap
            else:
                break

            # Update state
            producer_prev = producer_max
            prob_prev = min(prob_max, prob_ref)
            peak_producers = peak_producers[peak_producers > producer_max]

        # Save in dataset removing VoLL
        ds_opt['opt_dispatch_capacity'] = opt_dispatch_capacity
        ds_opt['opt_marginal_cost'] = marginal_cost.sel(
            producer=producers)
        ds_opt['opt_rental_cost'] = rental_cost.sel(producer=producers)

        return ds_opt


def _get_optimal_dispatch_probability(
        marginal_cost_0: xr.DataArray, rental_cost_0: xr.DataArray,
        marginal_cost_1: xr.DataArray,
        rental_cost_1: xr.DataArray) -> xr.DataArray:
    """Get optimal dispatch probability.

    :param marginal_cost_0: First producer's marginal cost.
    :param rental_cost_0: First producer's rental cost.
    :param marginal_cost_1: Second producer's marginal cost.
    :param rental_cost_1: Second producer's rental cost.

    :returns: Probability.
    """
    return (rental_cost_1 - rental_cost_0) / (
        marginal_cost_0 - marginal_cost_1)
