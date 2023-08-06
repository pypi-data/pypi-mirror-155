"""Renewable-energy mean-risk optimization module."""
import os
from collections import OrderedDict
from itertools import product
from copy import deepcopy
import numpy as np
import pandas as pd
import xarray as xr
from scipy.optimize import Bounds, minimize
from cvxopt import solvers, matrix, spmatrix
import matplotlib.pyplot as plt
from matplotlib import rcParams, ticker
from ..container import ensure_collection, load_config
from ..optimization import OptimizerBase, SolutionBase, InputBase
from ..plot import plot_geo_dist
from ..geo import GEO_VARIABLE_NAME


class Optimizer(OptimizerBase):
    """Renewable energy mean risk optimizer."""

    def __init__(self, med, cfg=None, **kwargs):
        """Constructor setting input data period used.

        :param med: Mediator.
        :param cfg: Optimizer configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type cfg: mapping

        .. seealso:: :py:class:`.optimization.OptimizerBase`.
        """
        # Initialize as OptimizerBase
        super(Optimizer, self).__init__(
            med, 'res_mean_risk', cfg=cfg, **kwargs)

        #: Demand component manager.
        self.demand_component_mng = self.med.component_managers.get(
            self.cfg['component'].get('demand'))

        #: Generation component managers.
        self.generation_component_managers = OrderedDict()

        #: Generation component names.
        self.generation_component_names = set()

        # Add generation components
        for component_mng_name in self.cfg['component']['capacity_factor']:
            component_mng = self.med.component_managers[component_mng_name]
            self.generation_component_managers[
                component_mng_name] = component_mng
            self.generation_component_names.add(component_mng.name)

        #: Number of generation components.
        self.n_gen_comp = len(self.generation_component_managers)

        # Overwrite input and solution with module class
        self.input = Input(self, self.cfg['input'], **kwargs)
        self.solution = Solution(self, self.cfg, **kwargs)

        #: Cases to solve.
        self.cases = OrderedDict()
        #: Case keys.
        self.case_keys = self.cfg.pop('cases')
        # Add cases to solve in solution variables
        self.add_cases(**kwargs)

        # Add reference capacity data source(s)
        variable_name = 'capacity'
        for src_name in self.cfg['reference_{}'.format(
                variable_name)].values():
            self.med.add_data_source(src_name, variable_names=variable_name)

    def add_cases(self, **kwargs):
        """Add cases to solution variables."""
        cases_values = []
        prop_names = []
        for keys_orig in self.case_keys:
            keys = keys_orig.copy()
            prop_names.append(keys[-1])
            value = self.cfg
            while len(keys) > 0:
                key = keys.pop(0)
                value = value[key]
            cases_values.append(ensure_collection(value))

        # Product of cases
        cases_prod = product(*cases_values)
        variable_names = set()
        for k, values in enumerate(cases_prod):
            case_name = ''.join([n + str(v)
                                 for (n, v) in zip(prop_names, values)])
            variable_names.add(case_name)
            self.cases[case_name] = values

        # Add variables to solution
        self.solution.update_variables(variable_names, **kwargs)

    def solve(self, **kwargs):
        """Solve optimization problem for all cases."""
        ds = {}
        for case_name, case_values in self.cases.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('Optimizing case {}:'.format(case_name))
            # Configure case
            cfg_case = deepcopy(self.cfg)
            for k, keys_orig in enumerate(self.case_keys):
                # Manage keys tree
                keys = keys_orig.copy()
                cfg_entry = cfg_case
                while len(keys) > 1:
                    key = keys.pop(0)
                    cfg_entry = cfg_entry[key]
                # Set value of each case key
                cfg_entry[keys[0]] = case_values[k]
                if not self.cfg.get('no_verbose'):
                    self.log.info('  - with {} = {}'.format(
                        keys[0], cfg_entry[keys[0]]))

            # Get solution for each case
            ds[case_name] = self.solve_case(cfg_case, **kwargs)

        return ds

    def solve_case(self, cfg_case, **kwargs):
        """Solve optimization problem for a specific case.

        :param cfg_case: Case configuration.
        :type cfg_case: dict

        :returns: Solution.
        :rtype: dict
        """
        # Convert some scalars
        dim_comp_reg_name = 'component_region'
        n_comp_reg = len(self.input['cf'].region_multi)
        max_capacity = float(cfg_case['grid']['max_capacity'])
        min_capacity = float(cfg_case['grid']['min_capacity'])
        if self.demand_component_mng is not None:
            dem_tot_mean = float(self.input['dem_mean'].sum('region'))

            # Shortage, saturation arguments
            max_conventional = np.percentile(
                self.input['dem'].sum('region'),
                cfg_case['grid']['max_conventional'] * 100)
            args_shortage = (
                self.input['cf'].transpose('time', dim_comp_reg_name).values,
                self.input['dem'].transpose('time', 'region').values,
                max_conventional)
            args_saturation = (
                self.input['cf'].transpose('time', dim_comp_reg_name).values,
                self.input['dem'].transpose('time', 'region').values,
                cfg_case['grid']['max_res'])
        else:
            # Get yearly-mean total demand
            dem_tot_mean = cfg_case['total_demand']
            if self.med.cfg['frequency'] == 'month':
                # Get montly-mean total demand
                dem_tot_mean /= 12
            elif self.med.cfg['frequency'] == 'day':
                # Get daily-mean total demand
                dem_tot_mean /= 365
            elif self.med.cfg['frequency'] == 'hour':
                # Get hourly-mean total demand
                dem_tot_mean /= 365 * 24

        # Bounds on capacity
        if cfg_case['cstr'].get('bounds'):
            bounds = Bounds(min_capacity, max_capacity)
        else:
            bounds = None

        # Mask covariance matrix
        mask_cov = self._get_mask_cov(cfg_case['strategy'])
        cf_cov = self.input['cf_cov'].values
        cf_cov_masked = self.input['cf_cov'].where(~ mask_cov, 0.).values

        # List of objective function
        args = [(cf_cov_masked,)]
        funs, jacs, weights = [fun_var], [jac_var], [1.]

        # Add total capacity constraint
        if not (cfg_case['cstr'].get('tot_cap') in [None, False]):
            # Get total capacity
            ref_tot_cap = self.get_reference_total_capacity(**kwargs)

            args_tot_cap = (ref_tot_cap,)
            cfg_tot_cap = cfg_case['cstr'].get('tot_cap')
            if cfg_tot_cap is not None:
                if isinstance(cfg_tot_cap, bool):
                    # Hard constraint
                    if cfg_tot_cap:
                        tot_cap_cstr = {
                            'type': 'eq', 'fun': fun_total_capacity,
                            'jac': jac_total_capacity, 'args': args_tot_cap}
                else:
                    # Soft constraint
                    funs.append(fun_total_capacity_squared)
                    jacs.append(jac_total_capacity_squared)
                    args.append(args_tot_cap)
                    weights.append(cfg_tot_cap)

        # Collect objective functions and jacobians as a weighted sum
        fun = fun_collector(funs, weights)
        jac = fun_collector(jacs, weights)

        # Solve multi-objective problem by setting a
        # target penetration rate
        target_mean_pen_rng = np.arange(cfg_case['penetration']['start'],
                                        cfg_case['penetration']['stop'],
                                        cfg_case['penetration']['step'])

        # Array of optimal capacities
        sol = xr.Dataset()
        dims = (target_mean_pen_rng.shape[0],)
        coord_pen = ('target_mean_penetration', target_mean_pen_rng * 100)
        coords = [coord_pen, (
            dim_comp_reg_name, self.input['cf'].coords[dim_comp_reg_name])]
        sol['capacity'] = xr.DataArray(
            np.empty(dims + (n_comp_reg,)), coords=coords).where(False)
        sol['generation'] = xr.DataArray(
            np.empty(dims + (n_comp_reg,)), coords=coords).where(False)
        sol['risk'] = xr.DataArray(np.empty(dims), coords=[
            coord_pen]).where(False)
        sol['mean_penetration'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['tot_cap'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        if 'pv' in self.generation_component_managers:
            sol['pv_frac'] = xr.DataArray(
                np.empty(dims), coords=[coord_pen]).where(False)
        if self.demand_component_mng is not None:
            sol['shortage'] = xr.DataArray(
                np.empty(dims), coords=[coord_pen]).where(False)
            sol['saturation'] = xr.DataArray(
                np.empty(dims), coords=[coord_pen]).where(False)
        # coords = [coord_pen, self.input['cf'].coords['time'],
        #           self.input['dem'].coords['region']]
        # sol['Pmismatch'] = xr.DataArray(
        #    np.empty(dims + (nt, n_reg)), coords=coords).where(False)
        # coords = [coord_pen, self.input['dem'].coords['region']]
        # PmismatchStd = xr.DataArray(
        #     np.empty(dims + (n_reg,)), coords=coords).where(False)

        # Conversion to GWh/y
        fact = 24 * 365 * 1e-6

        # Loop over range of targets
        for (imu, target_mean_pen) in enumerate(target_mean_pen_rng):
            # Define initial state
            try:
                # Use previous minimizer otherwise
                x0 = res.x
            except (NameError, AttributeError):
                # Use a uniform generation initial state for first iteration
                x0 = (np.ones((n_comp_reg,)) * target_mean_pen / n_comp_reg
                      * dem_tot_mean)

            # Collect constraints
            # SLSQP: constraints are defined as list of dictionaries
            # Total penetration constraint
            args_tot_pen = (self.input['cf_norm'].mean('time').values,
                            target_mean_pen * dem_tot_mean)
            tot_pen_cstr = {'type': 'eq', 'fun': fun_total_penetration,
                            'jac': jac_total_penetration,
                            'args': args_tot_pen}

            # Collect constraints
            constraints = []
            if (isinstance(cfg_case['cstr'].get('tot_cap'), bool)
                    and (cfg_case['cstr'].get('tot_cap') is True)):
                # Hard constraint
                constraints.append(tot_cap_cstr)
            if cfg_case['cstr'].get('total_penetration'):
                constraints.append(tot_pen_cstr)

            # Solve problem
            res = minimize(fun, x0, args=args, jac=jac, bounds=bounds,
                           constraints=constraints, **cfg_case['scipy'])

            # Save results only if total penetration constraint not violated
            gap = (-fun_total_penetration(res.x, *args_tot_pen) * 100
                   / dem_tot_mean)
            if np.abs(gap) > 1.e-3:
                continue

            x = xr.DataArray(res.x, dims=(dim_comp_reg_name,))
            loc = {'target_mean_penetration': target_mean_pen * 100}
            sol['capacity'].loc[loc] = x
            sol['generation'].loc[loc] = (
                x * self.input['cf'].mean('time') * fact)
            sol['mean_penetration'].loc[loc] = get_mean_penetration(
                x.values, self.input['cf_norm'].values, dem_tot_mean)
            # Use full rather than masked covariance matrix when plotting
            # as opposed to when optimizing, so as for the risk to be
            # the same with/without interconnection (global/regional)
            sol['risk'].loc[loc] = get_risk(
                x.values, cf_cov, dem_tot_mean)
            sol['tot_cap'].loc[loc] = res.x.sum()
            if 'pv' in self.generation_component_managers:
                args_pv_frac = (0.,)
                pv_loc = (self.input['cf'].component == 'pv').values
                cstr_ratio = fun_pv_frac(
                    res.x, pv_loc, args_pv_frac) / res.x.sum()
                sol['pv_frac'].loc[loc] = cstr_ratio + args_pv_frac[0]
            if self.demand_component_mng is not None:
                sol['shortage'].loc[loc] = shortage_frequency(
                    res.x, *args_shortage)
                sol['saturation'].loc[loc] = saturation_frequency(
                    res.x, *args_saturation)

        # Add RES generation
        # PRES = (self.input['cf'] * sol['capacity']) * fact
        # coords = [coord_pen, self.input['cf'].coords['time'],
        #           self.input['dem'].coords['region']]
        # PRES = PRES.groupby(
        # PRES.coords[dim_comp_reg_name] % 6).sum(
        # dim_comp_reg_name, skipna=False)
        # del PRES['component'], PRES['region' + 'Multi']
        # PRES = (PRES.rename({dim_comp_reg_name: 'region'}).assign_coords(
        #     **{'region': self.input['dem'].coords['region']})
        #         .transpose('time', coord_pen[0], 'region'))
        # PRESMean = PRES.mean('time')
        # PRESStd = PRES.std('time')
        # sol['PRES'] = PRES

        # Add optimization configuration as attributes
        _save_dict(cfg_case, sol)

        return sol

    def _get_mask_cov(self, strategy):
        """Get covariance-matrix mask for a given strategy.

        :param strategy: Strategy (`'global'`, `'techno'`, or `'none'`)
        :type strategy: str

        :returns: Covariance-matrix mask.
        :rtype: :py:class:`xarray.DataArray`
        """
        dim_comp_reg_name = 'component_region'
        n_comp_reg = len(self.input['cf'].region_multi)
        n_reg = n_comp_reg // self.n_gen_comp

        mask_cov = xr.ones_like(self.input['cf_cov'], dtype=bool)
        if strategy == 'none':
            # Only the variances (diagnonal) are considered in the optimization
            idx = xr.DataArray(range(n_comp_reg),
                               dims=[dim_comp_reg_name + '_i'])
            mask_cov[idx, idx] = False
        elif strategy == 'techno':
            # Covariances between technologies of the same region
            for ic in range(self.n_gen_comp):
                i_diag = ic * n_reg + np.arange(n_reg)
                for jc in range(self.n_gen_comp):
                    j_diag = jc * n_reg + np.arange(n_reg)
                    mask_cov.values[(i_diag, j_diag)] = False
        elif strategy == 'global':
            # Both technological and regional covariances
            mask_cov[:] = False
        else:
            raise RuntimeError(
                'Invalid strategy choice: {}. Should be none, techno or '
                'global.'.format(strategy))

        return mask_cov

    def get_reference_total_capacity(self, capacity=None, **kwargs):
        """Get total capacity from `'grid'` configuration or from data file.

        :param capacity: Capacity array (MW). Default is `None`, in which case
          capacities are concatenated from components output data source(s).
        :type capacity: :py:class:`xarray.DataArray`

        :returns: Total capacity.
        :dtype: float

        .. note:: If possible, the reference total-capacity is read from the
          `'tot_capacity'` entry of the `'grid'` section of the optimizer
          configuration.
          Otherwise, it is computed from the reference capacities obtained
          calling :py:meth:`get_reference_capacity`.
        """
        if 'tot_cap' in self.cfg['grid']:
            tot_cap = float(self.cfg['grid']['tot_cap'])
            if not self.cfg.get('no_verbose'):
                self.log.info('Read total capacity of {:.0f} MW from '
                              'grid configuration'.format(tot_cap))
        else:
            # Get total capacity for each generation component
            da = (self.get_reference_capacity(**kwargs)[0]
                  if capacity is None else capacity)
            tot_cap = float(da.sum(['region', 'component']))
            if not self.cfg.get('no_verbose'):
                self.log.info('Read total capacity of {:.0f} MW from '
                              'generation data'.format(tot_cap))

        return tot_cap

    def get_reference_capacity(self, **kwargs):
        """Aggregate capacity for all generation components.

        :returns: Capacities and data-sources postfix.
        :dtype: :py:class:`tuple` of :py:class:`xarray.DataArray` and
          :py:class:`str`
        """
        syear = '{}-12-31'.format(self.cfg['reference_year'])
        variable_name = 'capacity'
        postfix = ''

        da = None
        for component_mng in self.generation_component_managers.values():
            component_name = component_mng.component_name

            # Read component reference capacity from given data source
            data_src = self.med.data_sources[
                self.cfg['reference_{}'.format(variable_name)][
                    component_name]]
            kwargs_get = kwargs.copy()
            kwargs_get['variable_names'] = variable_name
            kwargs_get['variable_component_names'] = {
                variable_name: self.generation_component_names}
            data = data_src.get_data(**kwargs_get)[variable_name]
            postfix += '_{}_{}{}'.format(
                component_mng.name, data_src.name,
                data_src.get_data_postfix(**kwargs_get))

            # Select
            da_comp = data.sel(time=syear)
            try:
                # Try to select component (if multi-index)
                da_comp = da_comp.sel(component=component_name)
            except ValueError:
                pass

            # Add array
            da = (da_comp if da is None else
                  xr.concat([da, da_comp], dim='component'))

        # Add reference year to postfix
        postfix += '_{}'.format(self.cfg['reference_year'])

        return da, postfix


class Input(InputBase):
    """Optimization problem input data source."""

    def __init__(self, optimizer, cfg=None, **kwargs):
        """Initialize input data source.

        :param optimizer: Optimizer.
        :param cfg: Input configuration. Default is `None`.
        :type optimizer: :py:class:`.optimization.OptimizerBase`
        :type cfg: mapping
        """
        cfg = {} if cfg is None else cfg
        super(Input, self).__init__(optimizer, cfg=cfg, **kwargs)

        # Set input data period to use
        if self.cfg.get('select_period'):
            self.start_date = pd.Timestamp(self.cfg['start_date'])
            self.end_date = pd.Timestamp(self.cfg['end_date'])

        # Add variable
        self.update_variables([
            'cf', 'cf_norm', 'cf_cov'])

        if self.optimizer.demand_component_mng is not None:
            # Add demand variables
            self.update_variables(['dem', 'dem_mean'])

    def download(self, **kwargs):
        pass

    def load(self, **kwargs):
        """Load optimization problem input data."""
        if self.optimizer.demand_component_mng is not None:
            # Get demand data
            variable_name = 'demand'
            result_mng = self.optimizer.demand_component_mng[variable_name]
            kwargs['variable_names'] = variable_name
            da_dem = result_mng.get_data(**kwargs)[variable_name]
        else:
            da_dem = None

        # Get capacity factors
        da_list = []
        variable_name = 'capacity_factor'
        for component_mng in (
                self.optimizer.generation_component_managers.values()):
            # Select component results for output variable
            result_mng = component_mng.result_managers[variable_name]
            kwargs['variable_names'] = variable_name
            da_comp = result_mng.get_data(**kwargs)[variable_name]

            # Make sure that data contains only this component
            if 'component' in da_comp.dims:
                da_comp = da_comp.sel(component=component_mng.component_name,
                                      drop=True)

            # Expand dimension
            da_comp = da_comp.expand_dims('component').assign_coords(
                component=[component_mng.component_name])
            da_list.append(da_comp)
        da_cf = xr.concat(da_list, dim='component')

        # Select period
        if self.cfg.get('select_period'):
            time_slice = slice(self.start_date, self.end_date)
            if self.optimizer.demand_component_mng is not None:
                da_dem = da_dem.sel(time=time_slice)
            da_cf = da_cf.sel(time=time_slice)

        if self.optimizer.demand_component_mng is not None:
            # Select common time-slice between demand and capacity factors
            common_index = da_dem.indexes['time']
            common_index = common_index.intersection(da_cf.indexes['time'])
            da_dem = da_dem.sel(time=common_index)
            da_cf = da_cf.sel(time=common_index)
            if not self.cfg.get('no_verbose'):
                self.log.info('{}-{} period selected'.format(
                    *da_cf.indexes['time'][[0, -1]].to_list()))

        # Sub-sample, if needed
        if self.med.cfg['frequency'] == 'day':
            if self.optimizer.demand_component_mng is not None:
                da_dem = da_dem.resample(time='D').sum('time')
            da_cf = da_cf.resample(time='D').mean('time')
        if self.med.cfg['frequency'] == 'month':
            if self.optimizer.demand_component_mng is not None:
                da_dem = da_dem.resample(time='M').sum('time')
            da_cf = da_cf.resample(time='M').mean('time')

        # Collect input data
        ds = self._collect_data(da_cf, da_dem, **kwargs)

        return ds

    def _collect_data(self, da_cf, da_dem=None, **kwargs):
        """"Collect demand and capacity factor input data
        needed for regional RES distribution optimization problem.

        :param da_cf: Capacity factors data array.
        :param da_dem: Demand data array. Default is `None`.
        :type da_cf: :py:obj:`xarray.DataArray`
        :type da_dem: :py:obj:`xarray.DataArray`

        :returns: Dataset collecting all necessary data.
        :rtype: :py:obj:`xarray.Dataset`
        """
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: (
            'component', 'region_multi')}

        # Problem dimensions
        region = da_cf.coords['region']
        n_reg = len(region)
        n_comp_reg = self.optimizer.n_gen_comp * n_reg

        if da_dem is not None:
            # Make sure that demand regions follow the order of CF regions
            dem = da_dem.sel(region=da_cf.indexes['region'])

            # Try to select component in case needed
            try:
                dem = dem.sel(component=self.optimizer.demand_component_mng.
                              component_name)
            except ValueError:
                pass

            # Convert daily energy (MWh/d) to power (MW)
            if self.med.cfg['frequency'] == 'day':
                dem /= 24
            dem.attrs['units'] = 'MW'

            # Get demand means
            dem_mean = dem.mean('time')
            dem_tot_mean = dem_mean.sum('region')

        # Concatenate energy components and get mean
        cf = da_cf.rename({'region': 'region_multi'}).stack(**dim_comp_reg)

        if da_dem is not None:
            # Normalized capacity factors (rescaled by total mean demand)
            cf_norm = da_cf.copy(deep=True)
            cf_norm /= dem.sum('region') / dem_tot_mean
            cf_norm = cf_norm.rename(
                {'region': 'region_multi'}).stack(**dim_comp_reg)
        else:
            cf_norm = cf

        # Covariance matrix of regional components
        cf_norm_valid = cf_norm.where(~cf_norm.isnull(), 0.)
        cf_cov = xr.DataArray(np.cov(cf_norm_valid, rowvar=False), coords=[
            (dim_comp_reg_name + '_i', range(n_comp_reg)),
            (dim_comp_reg_name + '_j', range(n_comp_reg))])

        cf_cov.attrs['long_name'] = 'Capacity-Factor Covariance'
        cf_cov.attrs['long_name'] = 'Normalized {}'.format(
            cf_cov.attrs['long_name'])

        # Add long names
        cf.attrs['long_name'] = 'Capacity-Factor Time-Series'
        if da_dem is not None:
            cf_norm.attrs['long_name'] = (
                'Demand-Normalized Capacity-Factor Time-Series')
            dem.attrs['long_name'] = 'Demand'
            dem_mean.attrs['long_name'] = 'Demand Mean'

        # Collect as Dataset
        ds = {'cf': cf.reset_index('component_region'),
              'cf_norm': cf_norm.reset_index('component_region'),
              'cf_cov': cf_cov}
        if da_dem is not None:
            ds.update({'dem': dem, 'dem_mean': dem_mean})

        return ds

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
            postfix.append(self.optimizer.demand_component_mng['demand'].
                           get_data_postfix(**kwargs).split('_'))

            # Capacity factors postfix
            for component_mng in (
                    self.optimizer.generation_component_managers.values()):
                postfix.append(component_mng['capacity_factor'].
                               get_data_postfix(**kwargs).split('_'))

            # Join postfixes
            postfix = np.concatenate(postfix)
            _, idx = np.unique(postfix, return_index=True)
            postfix = '_'.join(postfix[np.sort(idx)])

            # Add period
            if self.cfg.get('select_period'):
                postfix += '_{}-{}'.format(
                    self.start_date.date().strftime('%Y%m%d'),
                    self.end_date.date().strftime('%Y%m%d'))

        return postfix

    def plot_reference_capacity(self, **kwargs):
        """Plot map of regional capacity from reference."""
        cfg_plot = load_config(self.med, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        map_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='map', **kwargs)

        # Get reference capacity
        capa_ref, result_postfix = self.optimizer.get_reference_capacity(
            **kwargs)

        # Read the regions coordinates and ensure order
        self.med.geo_src.get_data(variable_names=GEO_VARIABLE_NAME, **kwargs)
        df_coords = self.med.geo_src.read_place_coordinates(**kwargs)
        df_coords = df_coords.loc[capa_ref['region'], :]
        lat, lon = df_coords['lat'].values, df_coords['lon'].values

        # Plot reference capacity
        if not cfg_plot.get('no_verbose'):
            self.log.info('Plotting reference capacity')
        comp_coord = capa_ref['component']
        wind_comp_name = str(comp_coord[comp_coord.isin([
            'wind', 'wind-onshore', 'wind-offshore'])][0].values)
        capa_pv = capa_ref.sel(component='pv')
        capa_wind = capa_ref.sel(component=wind_comp_name)
        fig_filename = 'map_capacity_reference{}.{}'.format(
            result_postfix, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            **self.optimizer.cfg['plot']['dist'], **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)


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

    def plot_mean_risk_front(self, **kwargs):
        """Plot mean-risk optimal frontiers of solutions."""
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: ('component', 'region_multi')}
        cfg_plot = load_config(self.med, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        front_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='front', **kwargs)
        pv_frac_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='pv_frac', **kwargs)
        result_postfixes = []

        # Get total capacity
        capa_ref, _ = self.optimizer.get_reference_capacity(**kwargs)
        ref_tot_cap = self.optimizer.get_reference_total_capacity(
            capa_ref, **kwargs)

        # Mean-risk plot options
        # tau_critic = 1.e-2
        tau_critic = 99.e-2
        colors = ['k'] + rcParams['axes.prop_cycle'].by_key()['color']

        # Make sure input data is loaded
        self.optimizer.input.get_data(**kwargs)
        pv_loc = self.optimizer.input['cf'].component == 'pv'

        # Set up the figures
        fig = plt.figure()
        ax_front = fig.add_subplot(111)
        fig_ratio = plt.figure()
        ax_ratio1 = fig_ratio.add_subplot(111)
        ax_ratio2 = ax_ratio1.twiny()

        # Get the mean penetration and the risk of the observed mix
        dem_tot_mean = float(self.optimizer.input['dem_mean'].sum('region'))
        capa_ref = capa_ref.rename(
            {'region': 'region_multi'}).stack(**dim_comp_reg)
        mean_penetration_obs = get_mean_penetration(
            capa_ref.values, self.optimizer.input['cf_norm'].values,
            dem_tot_mean)
        risk_obs = get_risk(
            capa_ref.values, self.optimizer.input['cf_cov'].values,
            dem_tot_mean)
        pv_capa = capa_ref.loc[{dim_comp_reg_name: pv_loc}]
        pv_frac_obs = float(pv_capa.sum() / capa_ref.sum())
        ax_ratio1.scatter(
            pv_frac_obs * 100, mean_penetration_obs * 100,
            s=self.cfg['plot']['markersize']**2, c=colors[2], marker='o',
            zorder=2)
        label_point_obs = '{} mix'.format(self.cfg['reference_year'])
        if not cfg_plot.get('no_verbose'):
            self.log.info('{}:'.format(label_point_obs))
            self.log.info('  Mean total penetration: {:.1f} %'.format(
                mean_penetration_obs * 100))
            self.log.info(
                '  Total standard deviation: {:.1f} %'.format(risk_obs * 100))
            self.log.info('  Mean-standard deviation ratio: {:.3f}'.format(
                mean_penetration_obs / risk_obs))
            self.log.info(
                '  pv fraction: {:.1f} %'.format(pv_frac_obs * 100))

        # Plot mean-risk point of observed mix
        point_obs = ax_front.scatter(
            risk_obs * 100, mean_penetration_obs * 100,
            s=self.cfg['plot']['markersize']**2, c=colors[-3], marker='o',
            zorder=2)

        # Plot global strategy
        cap_values = [False, True]
        strategy = 'global'
        label_front = {'global': 'Global', 'techno': 'Technology',
                       'none': 'Base'}
        line = {}
        label_line = {}
        for k, cap_val in enumerate(cap_values):
            if not cfg_plot.get('no_verbose'):
                self.log.info('{} strategy:'.format(strategy))
            case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
            sol = self[case_name]
            result_postfixes.append(np.array(
                self.get_data_postfix().split('_')))

            # Plot on pv fraction
            idx_opt = np.arange(0, len(sol['target_mean_penetration']))
            if cap_val:
                # Get index of minimum risk under capacity constraint
                idx_min_risk = int(np.argmin(sol['risk']))
                idx_opt = np.arange(idx_min_risk, len(
                    sol['target_mean_penetration']))
                h_ratio = ax_ratio1.plot(
                    sol['pv_frac'][idx_opt] * 100,
                    sol['target_mean_penetration'][idx_opt],
                    linestyle='-', color=colors[2])[0]
                h_short = ax_ratio2.plot(
                    sol['shortage'][idx_opt] * 100,
                    sol['target_mean_penetration'][idx_opt],
                    linestyle='-', color=colors[3])[0]
                h_sat = ax_ratio2.plot(
                    sol['saturation'][idx_opt] * 100,
                    sol['target_mean_penetration'][idx_opt],
                    linestyle='--', color=colors[3])[0]

            # Get feasible penetrations
            is_val = sol['capacity'].notnull().all(
                dim=dim_comp_reg_name)
            ipen_rng = np.nonzero(is_val.values)[0][[0, -1]].tolist()

            # Get index before shortage or saturation
            idx_no_shortage = np.nonzero(
                (sol['shortage'] < tau_critic).values)[0].tolist()
            idx_no_saturation = np.nonzero(
                (sol['saturation'] < tau_critic).values)[0].tolist()
            idx_no_critic = np.sort(np.intersect1d(
                np.intersect1d(idx_no_shortage, idx_no_saturation),
                idx_opt))

            # Plot mean-risk
            ax_front.plot(
                sol['risk'][idx_opt] * 100,
                sol['mean_penetration'][idx_opt] * 100,
                linestyle='--', linewidth=1, color=colors[k], zorder=1)
            # Thicker plot of non critical situations
            if len(idx_no_critic) > 0:
                line[strategy + str(cap_val)] = ax_front.plot(
                    sol['risk'][idx_no_critic] * 100,
                    sol['mean_penetration'][idx_no_critic] * 100,
                    linestyle='-', linewidth=2, color=colors[k], zorder=1)
                label_cstr = ('frontier (constrained)' if cap_val else
                              'frontier')
                label_line[strategy + str(cap_val)] = '{} {}'.format(
                    label_front[strategy], label_cstr)

            # Get the index of the minimum risk under
            # capacity constraint
            try:
                xmin_ratio = self.cfg['plot']['ratio']['xlim'][0]
                xmax_ratio = self.cfg['plot']['ratio']['xlim'][1]
            except (KeyError, TypeError):
                xmin_ratio, xmax_ratio = ax_ratio1.get_xlim()
            try:
                xmin_front = self.cfg['plot']['front']['xlim'][0]
                xmax_front = self.cfg['plot']['front']['xlim'][1]
            except (KeyError, TypeError):
                xmin_front, xmax_front = ax_front.get_xlim()
            if cap_val:
                mean_penetration = sol['mean_penetration'][
                    idx_min_risk].values * 100
                risk = sol['risk'][idx_min_risk].values * 100
                ratio = mean_penetration / risk
                pv_frac = sol['pv_frac'][idx_min_risk].values
                label_point_min = 'Minimum-variance mix'
                point_min = ax_front.scatter(
                    risk, mean_penetration,
                    s=self.cfg['plot']['markersize']**2,
                    c=colors[k], marker='o', zorder=2)

                if not cfg_plot.get('no_verbose'):
                    self.log.info('{}:'.format(label_point_min))
                    self.log.info(
                        '  Mean total penetration: {:.1f} %'.format(
                            mean_penetration))
                    self.log.info(
                        '  Total standard deviation: {:.1f} %'.format(risk))
                    self.log.info(
                        '  Mean-standard deviation ratio: {:.3f}'.format(
                            ratio))
                    self.log.info('  pv fraction: {:.1f} %'.format(
                        pv_frac * 100))

                # Mark the optimal mix with the same level of risk
                # as the observed mix
                idx_risk_as_obs = np.argmin(
                    np.abs(sol['risk'][idx_min_risk:] - risk_obs))
                pen_risk_as_obs = (
                    sol['mean_penetration'][idx_min_risk:][
                        idx_risk_as_obs]).values * 100
                risk_as_obs = sol['risk'][idx_min_risk:][
                    idx_risk_as_obs].values * 100
                pv_frac_as_obs = sol['pv_frac'][idx_min_risk:][
                    idx_risk_as_obs]
                pv_frac_as_obs = pv_frac_as_obs.values * 100
                label_point_high = 'High-penetration mix'
                if not cfg_plot.get('no_verbose'):
                    self.log.info('{}:'.format(label_point_high))
                    self.log.info(
                        '  Mean total penetration: {:.1f} %'.format(
                            pen_risk_as_obs))
                    self.log.info('  Total standard deviation: {:.1f} %'.format(
                        risk_as_obs))
                    self.log.info(
                        '  Mean-standard deviation ratio: {:.3f}'.format(
                            pen_risk_as_obs / risk_as_obs))
                    self.log.info('  pv fraction: {:.1f} %'.format(
                        pv_frac_as_obs))
                if (idx_risk_as_obs + idx_min_risk) < ipen_rng[-1]:
                    point_high = ax_front.scatter(
                        risk_as_obs, pen_risk_as_obs,
                        s=self.cfg['plot']['markersize']**2*1.2, c=colors[k],
                        marker='d', zorder=2)
                    ax_ratio1.hlines(
                        pen_risk_as_obs,
                        xmin=xmin_ratio, xmax=xmax_ratio,
                        linestyle='--', linewidth=1, color=colors[k],
                        zorder=2)

                # Plot on pv fraction
                ax_ratio1.hlines(
                    [sol['target_mean_penetration'][idx_min_risk]],
                    xmin=xmin_ratio, xmax=xmax_ratio,
                    linestyle='--', linewidth=1, color=colors[k], zorder=2)
            else:
                # Shadow impossible ratios
                x_poly = [xmin_front,  sol['risk'][0] * 100,
                          sol['risk'][-1] * 100,  xmin_front]
                y_poly = np.array([
                    sol['mean_penetration'][0],
                    sol['mean_penetration'][0],
                    sol['mean_penetration'][-1],
                    sol['mean_penetration'][-1]]) * 100
                ax_front.fill(x_poly, y_poly, '0.8')

                # Plot point of agreement
                idx_agree = np.argmin(
                    (sol['capacity'].sum(dim_comp_reg_name)
                     - ref_tot_cap)**2)
                mean_penetration = sol['mean_penetration'][
                    idx_agree].values * 100
                risk = sol['risk'][idx_agree].values * 100
                pv_frac = sol['pv_frac'][idx_agree].values * 100
                ratio = mean_penetration / risk
                label_point_ratio = 'Maximum-ratio mix'
                point_ratio = ax_front.scatter(
                    risk, mean_penetration,
                    s=self.cfg['plot']['markersize']**2,
                    c=colors[k], marker='o', zorder=2)

                if not cfg_plot.get('no_verbose'):
                    self.log.info('{}:'.format(label_point_ratio))
                    self.log.info(
                        '  Mean total penetration: {:.1f} %'.format(
                            mean_penetration))
                    self.log.info(
                        '  Total standard deviation: {:.1f} %'.format(risk))
                    self.log.info(
                        '  Mean-standard deviation ratio: {:.3f}'.format(
                            ratio))
                    self.log.info(
                        '  pv fraction: {:.1f} %'.format(pv_frac))

                # Plot on pv fraction
                ax_ratio1.hlines(
                    [sol['target_mean_penetration'][idx_agree]],
                    xmin=xmin_ratio, xmax=xmax_ratio,
                    linestyle='--', linewidth=1, color=colors[k], zorder=2)

            # Plot feasibility limit
            if (ipen_rng[-1] <
                    sol.dims['target_mean_penetration'] - 1):
                ax_front.scatter(
                    (sol['risk'] * 100)[ipen_rng[-1]],
                    (sol['mean_penetration'] * 100)[ipen_rng[-1]],
                    s=self.cfg['plot']['markersize']**2, c=colors[k],
                    marker='s', zorder=2)

        # Plot techno and none cases if possible
        cap_val = False
        for ist, strategy in enumerate(['techno', 'none']):
            case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
            if case_name in self:
                sol = self[case_name]
                if not cfg_plot.get('no_verbose'):
                    mean_penetration = sol['mean_penetration'][
                        idx_agree].values * 100
                    risk = sol['risk'][idx_agree].values * 100
                    pv_frac = sol['pv_frac'][idx_agree].values * 100
                    ratio = mean_penetration / risk
                    self.log.info('{} strategy:'.format(strategy))
                    self.log.info('Maximum-ratio mix:')
                    self.log.info(
                        '  Mean total penetration: {:.1f} %'.format(
                            mean_penetration))
                    self.log.info(
                        '  Total standard deviation: {:.1f} %'.format(risk))
                    self.log.info(
                        '  Mean-standard deviation ratio: {:.3f}'.format(
                            ratio))
                    self.log.info(
                        '  pv fraction: {:.1f} %'.format(pv_frac))

                label_line[strategy] = '{} frontier'.format(
                    label_front[strategy])
                line[strategy] = ax_front.plot(
                    sol['risk'] * 100, sol['mean_penetration'] * 100,
                    linestyle=self.cfg['plot']['front']['linestyle'][ist],
                    linewidth=1, color=colors[0], zorder=3)

        # Get result postfix
        _, comm1, _ = np.intersect1d(
            *result_postfixes, return_indices=True)
        result_postfix = '_'.join(result_postfixes[0][np.sort(comm1)])

        try:
            ax_front.set_xlim(self.cfg['plot']['front']['xlim'])
        except (KeyError, TypeError):
            pass
        # Adjust both y-axis limits so that both curves ends match
        try:
            ax_front.set_ylim(self.cfg['plot']['front']['ylim'])
        except (KeyError, TypeError):
            pass
        ax_front.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_front.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_front.set_xlabel('Standard Deviation (%)',
                            fontsize=cfg_plot['fs_default'])
        ax_front.set_ylabel('Mean (%)', color=colors[0],
                            fontsize=cfg_plot['fs_default'])
        if self.cfg['plot']['front']['add_legend']:
            # Add legend to fronts
            loc = self.cfg['plot']['front']['legend_loc'] or 'upper left'
            handles = [
                *line['globalTrue'], *line['globalFalse'],
                *line['techno'], *line['none'],
                point_min, point_ratio, point_high,
                point_obs]
            labels = [
                label_line['globalTrue'], label_line['globalFalse'],
                label_line['techno'], label_line['none'],
                label_point_min, label_point_ratio, label_point_high,
                label_point_obs]
            ax_front.legend(handles, labels, loc=loc)

        # Save fronts figure
        fig_filename = 'front{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(front_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Saving front figure to {}'.format(fig_filepath))
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        # Configure and save pv fraction
        plt.legend([h_ratio, h_short, h_sat],
                   ['pv fraction', 'Shortage', 'Saturation'], loc='best')
        ax_ratio1.set_xlabel('pv (%)', color=colors[2],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio2.set_xlabel('Shortage and Saturation (%)', color=colors[3],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio1.set_ylabel('Mean (%)',
                             fontsize=cfg_plot['fs_default'])
        try:
            ax_ratio1.set_xlim(self.cfg['plot']['ratio']['xlim'])
        except (KeyError, TypeError):
            pass
        try:
            ax_ratio2.set_xlim(self.cfg['plot']['freq']['xlim'])
        except (KeyError, TypeError):
            pass
        try:
            ax_ratio1.set_ylim(self.cfg['plot']['front']['ylim'])
        except (KeyError, TypeError):
            pass
        ax_ratio1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        # Save fronts figure
        fig_filename = 'pv_frac{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(pv_frac_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Saving pv fraction figure to {}'.format(fig_filepath))
        fig_ratio.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)

    def plot_mean_risk_front_nocstr(self, **kwargs):
        """Plot mean-risk optimal frontiers of solutions."""
        dim_comp_reg_name = 'component_region'
        cfg_plot = load_config(self.med, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        front_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='front', **kwargs)
        pv_frac_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='pv_frac', **kwargs)
        result_postfixes = []

        # Mean-risk plot options
        # tau_critic = 1.e-2
        tau_critic = 99.e-2
        colors = ['k'] + rcParams['axes.prop_cycle'].by_key()['color']

        # Set up the figures
        fig = plt.figure()
        ax_front = fig.add_subplot(111)
        fig_ratio = plt.figure()
        ax_ratio1 = fig_ratio.add_subplot(111)
        ax_ratio2 = ax_ratio1.twinx()

        # Plot global strategy
        k = 0
        strategy = 'global'
        label_front = {'global': 'Global', 'techno': 'Technology',
                       'none': 'Base'}
        line = {}
        label_line = {}
        if not cfg_plot.get('no_verbose'):
            self.log.info('{} mix:'.format(strategy))
        case_name = 'strategy{}'.format(strategy)
        sol = self[case_name]
        result_postfixes.append(np.array(
            self.get_data_postfix().split('_')))

        # Plot on pv fraction
        idx_opt = np.arange(0, len(sol['target_mean_penetration']))
        # Get index of minimum risk under capacity constraint
        idx_min_risk = int(np.argmin(sol['risk']))
        idx_opt = np.arange(idx_min_risk, len(
            sol['target_mean_penetration']))
        h_ratio = ax_ratio1.plot(
            sol['target_mean_penetration'][idx_opt],
            sol['pv_frac'][idx_opt] * 100,
            linestyle='-', color=colors[2])[0]
        h_short = ax_ratio2.plot(
            sol['target_mean_penetration'][idx_opt],
            sol['shortage'][idx_opt] * 100,
            linestyle='-', color=colors[3])[0]
        h_sat = ax_ratio2.plot(
            sol['target_mean_penetration'][idx_opt],
            sol['saturation'][idx_opt] * 100,
            linestyle='--', color=colors[3])[0]

        # Get feasible penetrations
        is_val = sol['capacity'].notnull().all(
            dim=dim_comp_reg_name)
        ipen_rng = np.nonzero(is_val.values)[0][[0, -1]].tolist()

        # Get index before shortage or saturation
        idx_no_shortage = np.nonzero(
            (sol['shortage'] < tau_critic).values)[0].tolist()
        idx_no_saturation = np.nonzero(
            (sol['saturation'] < tau_critic).values)[0].tolist()
        idx_no_critic = np.sort(np.intersect1d(
            np.intersect1d(idx_no_shortage, idx_no_saturation),
            idx_opt))

        # Plot mean-risk
        ax_front.plot(
            sol['risk'][idx_opt] * 100,
            sol['mean_penetration'][idx_opt] * 100,
            linestyle='--', linewidth=1, color=colors[k], zorder=1)
        # Thicker plot of non critical situations
        if len(idx_no_critic) > 0:
            line[strategy] = ax_front.plot(
                sol['risk'][idx_no_critic] * 100,
                sol['mean_penetration'][idx_no_critic] * 100,
                linestyle='-', linewidth=2, color=colors[k], zorder=1)
            label_line[strategy] = '{} frontier'.format(label_front[strategy])

        # Get the index of the minimum risk under
        # capacity constraint
        try:
            xmin_ratio = self.cfg['plot']['ratio']['xlim'][0]
            xmax_ratio = self.cfg['plot']['ratio']['xlim'][1]
        except (KeyError, TypeError):
            xmin_ratio, xmax_ratio = ax_ratio1.get_xlim()
        try:
            xmin_front = self.cfg['plot']['front']['xlim'][0]
            xmax_front = self.cfg['plot']['front']['xlim'][1]
        except (KeyError, TypeError):
            xmin_front, xmax_front = ax_front.get_xlim()
        mean_penetration = sol['mean_penetration'][
            idx_min_risk].values * 100
        risk = sol['risk'][idx_min_risk].values * 100
        ratio = mean_penetration / risk
        pv_frac = sol['pv_frac'][idx_min_risk].values
        label_point_min = 'Minimum-variance mix'
        point_min = ax_front.scatter(
            risk, mean_penetration,
            s=self.cfg['plot']['markersize']**2,
            c=colors[k], marker='o', zorder=2)

        if not cfg_plot.get('no_verbose'):
            self.log.info('{}:'.format(label_point_min))
            self.log.info(
                '  Mean total penetration: {:.1f} %'.format(
                    mean_penetration))
            self.log.info('  Total standard deviation: {:.1f} %'.format(risk))
            self.log.info(
                '  Mean-standard deviation ratio: {:.3f}'.format(ratio))
            self.log.info('  pv fraction: {:.1f} %'.format(
                pv_frac * 100))
        else:
            # Shadow impossible ratios
            x_poly = [xmin_front,  sol['risk'][0] * 100,
                      sol['risk'][-1] * 100,  xmin_front]
            y_poly = np.array([
                sol['mean_penetration'][0],
                sol['mean_penetration'][0],
                sol['mean_penetration'][-1],
                sol['mean_penetration'][-1]]) * 100
            ax_front.fill(x_poly, y_poly, '0.8')

        # Plot feasibility limit
        if (ipen_rng[-1] <
                sol.dims['target_mean_penetration'] - 1):
            ax_front.scatter(
                (sol['risk'] * 100)[ipen_rng[-1]],
                (sol['mean_penetration'] * 100)[ipen_rng[-1]],
                s=self.cfg['plot']['markersize']**2, c=colors[k],
                marker='s', zorder=2)

        # Plot techno and none cases if possible
        for ist, strategy in enumerate(['techno', 'none']):
            case_name = 'strategy{}'.format(strategy)
            if case_name in self:
                sol = self[case_name]
                label_line[strategy] = '{} frontier'.format(
                    label_front[strategy])
                line[strategy] = ax_front.plot(
                    sol['risk'] * 100, sol['mean_penetration'] * 100,
                    linestyle=self.cfg['plot']['front']['linestyle'][ist],
                    linewidth=1, color=colors[0], zorder=3)

        # Get result postfix
        if len(result_postfixes) > 1:
            _, comm1, _ = np.intersect1d(
                *result_postfixes, return_indices=True)
            result_postfixes_list = result_postfixes[0][np.sort(comm1)]
        else:
            result_postfixes_list = result_postfixes[0]
        result_postfix = '_'.join(result_postfixes_list)

        try:
            ax_front.set_xlim(self.cfg['plot']['front']['xlim'])
        except (KeyError, TypeError):
            pass
        # Adjust both y-axis limits so that both curves ends match
        try:
            ax_front.set_ylim(self.cfg['plot']['front']['ylim'])
        except (KeyError, TypeError):
            pass
        ax_front.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_front.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_front.set_xlabel('Standard Deviation (%)',
                            fontsize=cfg_plot['fs_default'])
        ax_front.set_ylabel('Mean (%)', color=colors[0],
                            fontsize=cfg_plot['fs_default'])
        if self.cfg['plot']['front']['add_legend']:
            # Add legend to fronts
            loc = self.cfg['plot']['front']['legend_loc'] or 'upper left'
            handles = [
                *line['global'], *line['techno'], *line['none'], point_min]
            labels = [
                label_line['global'], label_line['techno'],
                label_line['none'], label_point_min]
            ax_front.legend(handles, labels, loc=loc)

        # Save fronts figure
        fig_filename = 'front{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(front_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Saving front figure to {}'.format(fig_filepath))
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        # Configure and save pv fraction
        plt.legend([h_ratio, h_short, h_sat],
                   ['pv fraction', 'Shortage', 'Saturation'], loc='best')
        ax_ratio1.set_xlabel('pv (%)', color=colors[2],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio2.set_xlabel('Shortage and Saturation (%)', color=colors[3],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio1.set_ylabel('Mean (%)',
                             fontsize=cfg_plot['fs_default'])
        try:
            ax_ratio1.set_xlim(self.cfg['plot']['ratio']['xlim'])
        except (KeyError, TypeError):
            pass
        try:
            ax_ratio2.set_xlim(self.cfg['plot']['freq']['xlim'])
        except (KeyError, TypeError):
            pass
        try:
            ax_ratio1.set_ylim(self.cfg['plot']['front']['ylim'])
        except (KeyError, TypeError):
            pass
        ax_ratio1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        # Save fronts figure
        fig_filename = 'pv_frac{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(pv_frac_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Saving pv fraction figure to {}'.format(fig_filepath))
        fig_ratio.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)

    def plot_capacity_for_case(self, case_name, target_mean_pen, **kwargs):
        """Plot map of regional capacity from solution.

        :param case_name: Case name (e.g. `'strategyglobal'`).
        :param target_mean_pen: Target total mean penetration value.
        :type case_name: str
        :type target_mean_pen: float
        """
        dim_comp_reg_name = 'component_region'
        cfg_plot = load_config(self.med, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        map_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='map', **kwargs)

        # Make sure input data is loaded
        da_cf = self.optimizer.input.get_data(**kwargs)['cf']
        comp_coord = da_cf['component']
        pv_loc = comp_coord == 'pv'
        wind_comp_name = str(comp_coord[comp_coord.isin([
            'wind', 'wind-onshore', 'wind-offshore'])][0].values)
        wind_loc = da_cf.component == wind_comp_name

        # Select solution
        sol = self[case_name]

        # Read the regions coordinates and ensure order
        self.med.geo_src.get_data(variable_names=GEO_VARIABLE_NAME, **kwargs)
        df_coords = self.med.geo_src.read_place_coordinates(**kwargs)
        df_coords = df_coords.loc[sol['region'], :]
        lat, lon = df_coords['lat'].values, df_coords['lon'].values

        # Make sure regions coordinates are ordered
        idx_agree = np.argmin(
            np.abs(sol['mean_penetration'] - target_mean_pen))
        risk = float(sol['risk'][idx_agree])
        mean_penetration = float(sol['mean_penetration'][idx_agree])
        # Plot maximum ratio map
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Plotting at penetration {:.1f}% and risk {:.1f}%'.format(
                    mean_penetration * 100, risk * 100))
        capa_pv = sol['capacity'][{'target_mean_penetration': idx_agree,
                                   dim_comp_reg_name: pv_loc}]
        capa_wind = sol['capacity'][{'target_mean_penetration': idx_agree,
                                     dim_comp_reg_name: wind_loc}]
        starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
        result_postfix = '{}_{}'.format(self.get_data_postfix(), case_name)
        fig_filename = 'map_capacity{}{}.{}'.format(
            result_postfix, starget, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            mean_penetration=mean_penetration,
                            **self.cfg['plot']['dist'], **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)

    def plot_capacity_three_cases(self, strategy='global', **kwargs):
        """Plot map of regional capacity from solution.

        :param strategy: Strategy (`'global'`, `'techno'`, or `'none'`)
        :type strategy: str
        """
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: ('component', 'region_multi')}
        cfg_plot = load_config(self.med, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        map_dir = self.med.cfg.get_plot_directory(
            self.optimizer, subdirs='map', **kwargs)

        # Make sure input data is loaded
        self.optimizer.input.get_data(**kwargs)
        comp_coord = self.optimizer.input['cf']['component']
        pv_loc = comp_coord == 'pv'
        wind_comp_name = str(comp_coord[comp_coord.isin([
            'wind', 'wind-onshore', 'wind-offshore'])][0].values)
        wind_loc = comp_coord == wind_comp_name
        region = self.optimizer.input['dem'].region

        # Select constrained solution
        cap_val = True
        case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
        sol = self[case_name]

        # Select unconstrained solution
        cap_val = False
        case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
        sol_free = self[case_name]

        # Read the regions coordinates and ensure order
        self.med.geo_src.get_data(variable_names=GEO_VARIABLE_NAME, **kwargs)
        df_coords = self.med.geo_src.read_place_coordinates(**kwargs)
        df_coords = df_coords.loc[region, :]
        lat, lon = df_coords['lat'].values, df_coords['lon'].values

        # Get total capacity
        capa_ref, _ = self.optimizer.get_reference_capacity(**kwargs)
        ref_tot_cap = self.optimizer.get_reference_total_capacity(
            capa_ref, **kwargs)

        # Make sure regions coordinates are ordered
        idx_agree = np.argmin(
            (sol_free.capacity.sum(dim_comp_reg_name)
             - ref_tot_cap)**2)
        target_mean_pen = float(sol['target_mean_penetration'][idx_agree])
        risk = float(sol['risk'][idx_agree])
        mean_penetration = float(sol['mean_penetration'][idx_agree])
        # Plot maximum ratio map
        if not cfg_plot.get('no_verbose'):
            self.log.info('Plotting for the maximum ratio at penetration '
                          '{:.1f}% and risk {:.1f}%'.format(
                              mean_penetration * 100, risk * 100))
        capa_pv = sol['capacity'][{'target_mean_penetration': idx_agree,
                                   dim_comp_reg_name: pv_loc}]
        capa_wind = sol['capacity'][{'target_mean_penetration': idx_agree,
                                     dim_comp_reg_name: wind_loc}]
        starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
        result_postfix = '{}_{}'.format(self.get_data_postfix(),
                                        strategy)
        fig_filename = 'map_capacity{}{}.{}'.format(
            result_postfix, starget, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            mean_penetration=mean_penetration,
                            **self.cfg['plot']['dist'], **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        idx_min_risk = int(np.argmin(sol['risk']))
        target_mean_pen = float(sol['target_mean_penetration'][
            idx_min_risk])
        risk = float(sol['risk'][idx_min_risk])
        mean_penetration = float(sol['mean_penetration'][idx_min_risk])
        capa_pv = sol['capacity'][{'target_mean_penetration': idx_min_risk,
                                   dim_comp_reg_name: pv_loc}]
        capa_wind = sol['capacity'][{
            'target_mean_penetration': idx_min_risk,
            dim_comp_reg_name: wind_loc}]
        if not cfg_plot.get('no_verbose'):
            self.log.info(
                'Plotting at penetration {:.1f}% for the minimum risk '
                '{:.1f}%'.format(mean_penetration * 100, risk * 100))
        starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
        fig_filename = 'map_capacity{}{}.{}'.format(
            result_postfix, starget, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            mean_penetration=mean_penetration,
                            **self.cfg['plot']['dist'], **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        # Add observed mean/risk point of the observed mix
        dem_tot_mean = float(self.optimizer.input['dem_mean'].sum('region'))

        # Define the risk function
        # Objective function and its arguments
        x = capa_ref.rename({'region': 'region_multi'}).stack(
            **dim_comp_reg)

        # Get the mean penetration and the risk of the observed mix
        risk_obs = get_risk(
            x.values, self.optimizer.input['cf_cov'].values, dem_tot_mean)

        # Plot for increased penetration for the same decrease of
        # mean/risk ratio
        # idx_max_mean = int(np.argmax(sol['mean_penetration']))
        is_val = sol['capacity'].notnull().all(dim=dim_comp_reg_name)
        itarget_mean_pen_rng = np.nonzero(
            is_val.values)[0][[0, -1]].tolist()
        idx_risk_as_obs = np.argmin(
            np.abs(sol['risk'][idx_min_risk:] - risk_obs))
        if (idx_risk_as_obs + idx_min_risk) < itarget_mean_pen_rng[-1]:
            target_mean_pen = float(sol['mean_penetration'][idx_min_risk:][
                idx_risk_as_obs].values * 100)
            risk = float(sol['risk'][idx_min_risk:]
                         [idx_risk_as_obs].values)
            mean_penetration = float(sol['mean_penetration'][idx_min_risk:]
                                     [idx_risk_as_obs].values)
            idx = np.arange(len(sol['risk']))[idx_min_risk:][
                idx_risk_as_obs]
            capa_pv = sol['capacity'][{'target_mean_penetration': idx,
                                       dim_comp_reg_name: pv_loc}]
            capa_wind = sol['capacity'][{
                'target_mean_penetration': idx,
                dim_comp_reg_name: wind_loc}]
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Plotting at penetration {:.1f}% for a risk '
                    '{:.1f}% identical to that of the observed '
                    'mix'.format(mean_penetration * 100, risk * 100))
            starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
            fig_filename = 'map_capacity{}{}.{}'.format(
                result_postfix, starget, fig_format)
            fig_filepath = os.path.join(map_dir, fig_filename)
            fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                                mean_penetration=mean_penetration,
                                **self.cfg['plot']['dist'], **kwargs)
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)


def fun_collector(functions, weights=None, collector=sum):
    """Define a new function `f(x, *args)` given by some (weighted)
    aggregation of given functions (e.g. weighted sum).
    Each function `functions[k](x, *args[k])`
    takes the same first argument `x`, as secondary arguments
    those in the sequence `args[k]`, and returns a scalar.

    :param functions: Functions to aggregate.
    :param weights: Weights assigned to each summed function.
      If None, all functions are given the same weight one.
      Default is `None`.
    :param collector: Function used to aggregate the results
      of the given sequence of functions. Default is :py:func:`sum`.
    :type functions: sequence
    :type weights: sequence
    :type collector: function

    :returns: Function taking as arguments `x` and a sequence of sequences
      of other arguments of all functions,
      in the same order as :py:obj:`functions`, and returning the weighted sum
      of results of functions as a float.
    :rtype: function
    """
    # Use uniform weights if not given
    if weights is None:
        weights = [1.] * len(functions)

    # Define collector
    def f(x, args):
        return collector([(weights[k] * functions[k](x, *(args[k])))
                          for k in range(len(functions))])

    return f


def fun_var(x, cf_cov, **kwargs):
    """Objective function given by the variance associated with
    a capacity distribution and a capacity factors covariance matrix.

    :param x: State vector.
    :param cf_cov: pv/wind capacity factors covariances.
    :type x: :py:class:`numpy.array`
    :type cf_cov: :py:class:`numpy.array`

    :returns: Value of objective function.
    :rtype: float
    """
    # Compute objective
    obj = x.dot(cf_cov.dot(x))

    return obj


def jac_var(x, cf_cov, **kwargs):
    """Jacobian of objective function given by the variance associated with
    a capacity distribution and a capacity factors covariance matrix.

    :param x: State vector.
    :param cf_cov: pv/wind capacity factors covariances.
    :type x: :py:class:`numpy.array`
    :type cf_cov: :py:class:`numpy.array`

    :returns: Value of objective function.
    :rtype: float
    """
    # Compute objective
    jac = 2 * np.dot(cf_cov, x)

    return jac


def get_mean_penetration(x, cf, dem_tot=None, **kwargs):
    """Get mean total target penetration.

    :param x: State vector.
    :param cf: Capacity factors per region and component.
    :param dem_tot: (Mean) total demand.
      To provide if capacity factors provided are not normalized
      by demand.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem_tot: :py:class:`float` or :py:class:`numpy.array`

    :returns: Value of the left-hand side of constraint.
    :rtype: float
    """
    # Get mean penetration
    mean_pen = np.nanmean(cf.dot(x))

    # Divide by total demand
    if dem_tot is not None:
        mean_pen /= dem_tot

    return mean_pen


def get_risk(x, cf_cov, dem_tot, **kwargs):
    """Get risk.

    :param x: State vector.
    :param cf_cov: pv/wind capacity factors covariances.
    :param dem_tot: (Mean) total demand to normalize.
    :type x: :py:class:`numpy.array`
    :type cf_cov: :py:class:`numpy.array`
    :type dem_tot: :py:class:`float` or :py:class:`numpy.array`

    :returns: Value of objective function.
    :rtype: float
    """
    # Get risk
    risk = np.sqrt(fun_var(x, cf_cov))

    # Normalize
    if dem_tot is not None:
        risk /= dem_tot

    return risk


def fun_total_penetration(x, cf, dem_tot):
    """Function defining the equality constraint on total target penetration.

    :param x: State vector.
    :param cf: (Mean) capacity factors per region and component.
    :param dem_tot: (Mean) total demand.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem_tot: :py:class:`float` or :py:class:`numpy.array`

    :returns: Value of the left-hand side of constraint.
    :rtype: float
    """
    return dem_tot - np.dot(cf, x)


def jac_total_penetration(x, cf, *args):
    """Function defining Jacobian of the equality constraint
    on total target penetration.

    :param x: State vector(not used).
    :param cf: (Mean) capacity factors per region and component.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -cf


def fun_total_capacity(x, tot_cap):
    """Function defining the equality constraint on total capacity.

    :param x: State vector.
    :param tot_cap: Total capacity.
    :type x: :py:class:`numpy.array`
    :type tot_cap: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    return tot_cap - x.sum()


def jac_total_capacity(x, *args):
    """Function defining Jacobian of equality constraint on total capacity.

    :param x: State vector.
    :type x: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -np.ones((x.shape[0],))


def fun_total_capacity_squared(x, tot_cap):
    """Function defining soft equality constraint on total capacity
    by returning squared deviation from total capacity.

    :param x: State vector.
    :param tot_cap: Total capacity.
    :type x: :py:class:`numpy.array`
    :type tot_cap: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    return (tot_cap - x.sum())**2


def jac_total_capacity_squared(x, tot_cap):
    """Function defining Jacobian of soft equality constraint
    on total capacity.

    :param x: State vector.
    :type x: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -2 * np.ones((x.shape[0],)) * (tot_cap - x.sum())


def fun_regional_transmission(x, *args):
    """Function defining inequality constraint on regional transmission.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param trans: Regional transimission capacity.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type trans: :py:class:`numpy.array`

    :returns: Value of left-hand side of constraint.
    :rtype: :py:class:`numpy.array`
    """
    dem_t = args[1]
    nt, n_reg = dem_t.shape
    trans_t = np.tile(args[2], (nt, 1))
    omega_t = np.tile(x, (nt, 1))
    omega_t_pv = omega_t[:, :n_reg]
    omega_t_wind = omega_t[:, n_reg:]
    cf_t_pv = args[0][:, :n_reg]
    cf_t_wind = args[0][:, n_reg:]
    #  T_i+D_i(t)-\omega_i \eta_i(t)-\omega_{i + n_reg}
    #      \eta_{i + n_reg}(t)
    y = (trans_t + dem_t - omega_t_pv * cf_t_pv -
         omega_t_wind * cf_t_wind).flatten()

    return y


def jac_regional_transmission(x, *args):
    """Function defining Jacobian of inequality constraint
    on regional transimission.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param trans: Regional transimission capacity.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type trans: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    dem_t = args[1]
    nt, n_reg = dem_t.shape
    cf_t = args[0]
    cf_t_pv = cf_t[:, :n_reg]
    cf_t_wind = cf_t[:, n_reg:]
    jac = np.zeros((n_reg * 2, nt * n_reg))
    for k in np.arange(n_reg):
        jac[k, k::n_reg] = -cf_t_pv[:, k]
        jac[k + n_reg, k::n_reg] = -cf_t_wind[:, k]

    # Return transpose of Jacobian as scipy stacks constraints vertically
    return jac.T


def fun_shortage(x, cf, dem, max_conventional):
    """Function defining inequality constraint on RES production shortage,
    when the production from RES is not able
    to meet fraction of demand not met by conventional components.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_conventional: Maximum possible total conventional production.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_conventional: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    nt, n_reg = dem.shape
    omega_t = np.tile(x, (nt, 1))

    y = (omega_t * cf).sum(1) + max_conventional - dem.sum(1)

    return y


def jac_shortage(x, cf, *args):
    """Function defining Jacobian of inequality constraint on
    RES production shortage, when production from RES is not able
    to meet fraction of demand not met by conventional components.

    :param x: State vector(not used).
    :param cf: Time-dependent capacity factors.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return cf


def shortage_frequency(x, *args):
    """Compute frequency of occurence of shortage situations
    defined as situations when the production from RES is not able
    to meet the fraction of the demand not met by conventional components.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_conventional: Maximum possible total conventional production.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_conventional: float

    :returns: Frequency of occurence of shortage situations.
    :rtype: float
    """
    y = fun_shortage(x, *args)
    y_val = y[~np.isnan(y)]
    shortage_frequency = np.sum(y_val < 0.) / y_val.shape[0]

    return shortage_frequency


def fun_saturation(x, cf, dem, max_res):
    """Function defining the inequality constraint on the saturation,
    defined as situations when the production from RES exceeds
    the theoretical limit that the network can support.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_res: Maximum RES penetration, i.e. maximum fraction
      of production from RES over demand that the network can support.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_res: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    nt, n_reg = dem.shape
    omega_t = np.tile(x, (nt, 1))

    y = max_res * dem.sum(1) - (omega_t * cf).sum(1)

    return y


def jac_saturation(x, cf, *args):
    """Function defining Jacobian of the inequality constraint
    on the saturation, defined as situations when the production from RES
    exceeds the theoretical limit that the network can support.

    :param x: State vector(not used).
    :param cf: Time-dependent capacity factors.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -cf


def saturation_frequency(x, cf, dem, max_res):
    """Compute frequency of occurence of saturation situations
    defined as situations when the production from RES exceeds
    the theoretical limit that the network can support.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_res: Maximum RES penetration, i.e. the maximum
        fraction of production from RES over the demand that the network
        can support.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_res: float

    :returns: Frequency of occurence of saturation situations.
    :rtype: float
    """
    y = fun_saturation(x, cf, dem, max_res)
    y_val = y[~np.isnan(y)]
    saturation_frequency = np.sum(y_val < 0.) / y_val.shape[0]

    return saturation_frequency


def fun_pv_frac(x, pv_loc, pv_frac):
    """Function defining equality constraint on fraction of pv capacity
    over pv + wind capacity.

    :param x: State vector.
    :param pv_loc: Boolean index of pv capacities.
    :param pv_frac: pv capacity over total capacity.
    :type x: :py:class:`numpy.array`
    :type pv_loc: :py:class:`numpy.array`
    :type pv_frac: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    jac = -np.ones((x.shape[0],)) * pv_frac
    jac[pv_loc] += 1.

    y = np.dot(jac, x)

    return y


def jac_pv_frac(x, *args):
    """Jacobian of function defining equality constraint
    on fraction of pv capacity over pv + wind capacity.

    :param x: State vector.
    :param pv_frac: pv capacity over total capacity (pv + wind).
    :type x: :py:class:`numpy.array`
    :type pv_frac: float

    :returns: Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    n_reg = int((x.shape[0] + 0.1) / 2)
    pv_frac = args[0]
    jac = -np.ones((x.shape[0],)) * pv_frac
    jac[:n_reg] += 1.

    return jac


def get_bounds_cstr(lb=None, ub=None, dim=None, sparse=False):
    """Get linear constraint corresponding to lower and upper bounds
    on state.

    :param lb: Lower bound(s). Default is `None`.
    :param ub: Upper bound(s). Default is `None`.
    :param dim: Problem dimension. Should be given if bounds are scalar.
      Default is `None`.
    :param sparse: If `True`, return matrices as spmatrix
        and vectors as matrix. Default is `False`.
    :type lb: float, :py:class:`numpy.array`
    :type ub: float, :py:class:`numpy.array`
    :type dim: int
    :type sparse: bool

    :returns: A tuple containing matrix `G` and vector
         `h` defining constraint `G x <= h`.
    :rtype: tuple of :py:class:`numpy.array`,
        or :py:class:`cvxopt.spmatrix` and :py:class:`cvxopt.cvxmatrix`.

    .. note:: Constraint is adapted to the quadprod module.
        To use the CVXOPT module, the oposite should be taken.
    """
    # Make sure that bounds are vectors
    h = []
    G, v, i, j = [], [], [], []
    if lb is not None:
        if not hasattr(lb, "__len__"):
            lba = np.ones((dim,)) * lb
        else:
            dim = len(lb)
            lba = lb
        if sparse:
            v.append(-1. * np.ones(dim))
            i.append(np.arange(dim))
            j.append(np.arange(dim))
        else:
            G.append(-np.eye(dim))
        h.append(-lba)
    if ub is not None:
        if not hasattr(ub, "__len__"):
            uba = np.ones((dim,)) * ub
        else:
            dim = len(ub)
            uba = ub
        if sparse:
            v.append(np.ones(dim))
            i.append(np.arange(dim))
            j.append(np.arange(dim))
        else:
            G.append(np.eye(dim))
        h.append(uba)

    # Matrix G and vector h for `G x <= h`
    h = np.concatenate(h)
    if sparse:
        v = np.concatenate(v)
        i = np.concatenate(i)
        j = np.concatenate(j)
        G = spmatrix(v, i, j)
        h = matrix(h)
    else:
        G = np.concatenate(G, axis=0)

    return (G, h)


def get_weighted_sum_cstr(weights, target_sum):
    """Get linear equality constraint corresponding
    to a weighted sum.

    :param weights: Weights of mean.
    :param target_sum: Target value of weighted sum.
    :type weights: :py:class:`numpy.array`
    :type target_sum: float

    :returns: A tuple containing matrix `A` and vector
         `b` defining constraint `A x = b`.
    :rtype: tuple of :py:class:`numpy.ndarray`.
    """
    return (np.expand_dims(weights, 0), np.array([target_sum]))


def fun_distribute_cv_square(x, *args):
    """Objective function on conventional power and transmission for
    power flow analysis.

    :param x: Conventional power at each node.
    :param power_mismatch: Difference between load and the production
      at each node (MW).
    :param q: Parameter controling the weight given to minimization
      of conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type q: float

    :returns: Value of objective function.
    :rtype: float
    """
    power_mismatch, q = args

    obj = ((1. - q) * np.sum(x**2) + q * np.sum((x - power_mismatch)**2))

    return obj


def jac_distribute_cv_square(x, *args):
    """Jacobian of objective function on conventional power
    and transmission for power flow analysis.

    :param x: Conventional power at each node.
    :param power_mismatch: Difference between load and production
      at each node (MW).
    :param q: Parameter controling the weight given to minimization
      of conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type q: float

    :returns: Jacobian vector of objective function.
    :rtype: :py:class:`numpy.array`
    """
    power_mismatch, q = args

    jac = 2 * (x - q * power_mismatch)

    return jac


def distribute_cv_square(power_mismatch, r):
    """Distribute conventional capacity optimally while supplying mismatch
    between load and fatal production at each time step,
    independently of other types of production.

    :param power_mismatch: Difference between load and RES production
      at each node(MW).
    :param r: Parameter controling weight given to minimization of
      conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type r: float

    :returns: Conventional production at each node.
    :rtype: :py:class:`numpy.array`

    .. note::
        * The conventional production is optimally distributed subject
            to the total production summing to zero at each time step,
            i.e. such that the sum of the conventional and the RES production
            equals the load, constraining the conventional production at
            all nodes but the first one to be positive.
            Without this bound, one would have:

                * For `r = 0`, the conventional production is uniformly
                    distributed.
                * For `r = 1`, the conventional production compensates
                    the mismatch between the RES produciton and the demand,
                    i.e. there is no transmission.
                * For `0 <= r \<= 1`, the conventional production by a mix of the two.

        * Since may(for each time step) small
            (the size given by the number of regions)
            quadratic programming problems, we use the active region
            quadratic programming algorithm implemented in quadprog.
    """
    nt, n_reg = power_mismatch.shape

    # Get matrix defining quadratic objective function
    P = 2 * np.eye(n_reg)

    # Get matrix and vector defining positiveness constraints
    # on CV production
    lb = np.zeros((n_reg,))
    # Allow for negative production on slack bus 1
    lb[0] = -1.e27
    (G0, h0) = get_bounds_cstr(lb=lb, dim=n_reg)
    G0, h0 = -G0, -h0

    # Solve problem at each time step
    P_cv = np.empty((nt, n_reg))
    for t in np.arange(nt):
        Pt = power_mismatch[t]

        # Get vector defining quadratic objective function
        q = -2 * r * Pt

        # Get matrix and vector defining constraint on sum of
        # conventional capacity supplying mismatch
        (A, b) = get_weighted_sum_cstr(np.ones((n_reg,)), Pt.sum())

        # Concatenate equality and inequality constraints
        G = np.concatenate([A, G0], axis=0)
        h = np.concatenate([b, h0], axis=0)

        # Optimize
        res = solve_qp(P, -q, G.T, h, meq=1)

        # Save result
        P_cv[t] = res[0]

    return P_cv


def distribute_cv_mean_square(power_mismatch, r, window_length=None):
    """Distribute conventional capacity while supplying mismatch between
    load and production, minimizing variance.

    :param power_mismatch: Difference between load and production
      at each node (MW).
    :param r: Parameter controling weight given to minimization of
      conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :param window_length: Length of windows over which to average.
        If `None`, average over whole time series. Default is `None`.
    :type power_mismatch: :py:class:`numpy.array`
    :type r: float
    :type window_length: int

    :returns: Conventional production at each node.
    :rtype: :py:class:`numpy.array`

    .. note::

        * The conventional production is optimally distributed subject
          to the total production summing to zero at each time step,
          i.e. such that the sum of the conventional and the RES production
          equals the load, while constraining the conventional production
          at all nodes but the first one to be positive.
          The optimization is done with a compromise between
          the variance of the conventional production(q close to 0) and the
          variance of the transmission(q close to 1).
        * The optimization problem being high dimensional, due to the states
          including several time steps and all regions,
          we use the interio-point quadratic programming algorithm.

    """
    nt, n_reg = power_mismatch.shape
    if window_length is None:
        window_length = nt
    n_window = int(nt / window_length)
    rest = np.mod(nt, window_length)
    if rest > 0:
        # If remaining is long, add a window, otherwise keep in previous window
        if rest > window_length / 2:
            n_window += 1

    # Configure solver
    solvers.options['show_progress'] = False

    # Loop over windows
    P_cv = np.empty((nt, n_reg))
    for window in np.arange(n_window):
        # Get mismatch power window, making sure to cover whole time series
        if window == (n_window - 1):
            Pm_window = power_mismatch[window*window_length:]
        else:
            Pm_window = power_mismatch[window *
                                       window_length:(window+1)*window_length]

        # Last window may be shorter, update length
        nt_window = Pm_window.shape[0]
        dim = n_reg * nt_window

        # Get matrix defining quadratic objective function
        P = spmatrix(2. / nt_window, np.arange(dim), np.arange(dim))

        # Get matrix and vector defining positiveness constraints
        # on CV production
        lb = np.zeros((dim,))
        # Allow for negative production on slack bus 1
        lb[:nt_window] = -1.e15
        (G, h) = get_bounds_cstr(lb=lb, sparse=True)

        # Get matrix and vector defining constraint on sum of
        # conventional capacity supplying mismatch
        A = np.zeros((nt_window, dim))
        v = np.ones((dim,))
        i = np.tile(np.arange(nt_window), n_reg)
        j = np.arange(dim)
        A = spmatrix(v, i, j)
        b = matrix(Pm_window.sum(1))

        # Get vector defining quadratic objective function
        q = -r * P * matrix(Pm_window.T.flatten())

        # Use previous optimum as initial state if possible
        if (window > 0):
            # Make sure that vectors have same length
            if len(res['y']) == nt_window:
                initvals = {'x': res['x'], 's': res['s'], 'y': res['y'],
                            'z': res['z']}
            else:
                initvals = None

        else:
            initvals = None

        # Optimize
        res = solvers.qp(P, q, G=G, h=h, A=A, b=b, initvals=initvals)

        # Save result
        x = np.array(res['x'])[:, 0].reshape(n_reg, nt_window).T
        if window == (n_window - 1):
            P_cv[window*window_length:] = x
        else:
            P_cv[window*window_length:(window+1)*window_length] = x

    return P_cv


def quad_prog_active_set(G, c, A, b=None):
    """Brute-force active set method to solve convex quadratic program.

    :param G: Positive definite matrix.
    :param c: Linear vector.
    :param A: Linear constraint matrix.
    :param b: Constant vector for linear constraints.
    :type G: array_like
    :type c: array_like
    :type A: array_like
    :type b: array_like

    :returns: Tuple containing:

        * Optimization problem solution.
        * Lagrange multipliers.

    :rtype: tuple of :py:class:`numpy.ndarray`

    .. note:: This function is used for pedagogical purposes only.
      Favor using more advanced solvers (e.g. quadprog or from scipy).
    """
    m, n = A.shape
    idx = np.arange(n)
    b = np.zeros((m,)) if b is None else b

    # Inverse covariance matrix
    Gm1 = np.linalg.inv(G)

    # Get initial guess solving unbounded problem
    x = -Gm1.dot(c)

    # Get active set
    ix0 = x < 0
    W = ix0.nonzero()[0]
    x[ix0] = 0.
    while True:
        print('Active set:', W)
        m = W.shape[0]
        # Solve for step and Lagrange multipliers
        K = np.zeros((n + m, n + m))
        K[:n, :n] = G
        K[n:, :n] = A[W]
        K[:n, n:] = -A[W].T
        g = G.dot(x) + c
        pl = np.linalg.inv(K).dot(np.concatenate([-g, np.zeros((m,))]))
        p, lambdak = np.split(pl, [n])

        if np.linalg.norm(p, np.inf) < 1.e-6:
            if (lambdak >= 0).all():
                return x, lambdak
            else:
                # Remove constraint with minimum Lagrangian from active set
                jj = np.argmin(lambdak)
                W = np.setdiff1d(W, jj)
        else:
            # Compute alpha
            Ap = A.dot(p)
            ineg = Ap < 0
            v = np.zeros((n,))
            v[ineg] = (b - A.dot(x))[ineg] / Ap[ineg]
            alpha, iBlock = 1, None
            isel = np.intersect1d(np.setdiff1d(idx, W), ineg.nonzero()[0])
            if len(isel) > 0:
                ivmin = np.argmin(v[isel])
                if v[ivmin] < 1:
                    iBlock, alpha = isel[ivmin], v[isel][ivmin]

            # Update state
            x += alpha * p

            # Add blocking constraint
            W = W if iBlock is None else np.union1d(W, iBlock)


def _save_dict(di, ds, prefix=''):
    """Save a(multi-level) dictionary to a dataset's attributes.

    :param di: Dictionary to save.
      Multi-level dictionaries are flattened and child keys are prefixed
      by parent key.
    :param ds: Dataset in which to save dictionary.
    :param prefix: Prefix to append to child keys of dictionary.
    :type di: dict
    :type ds: :py:class:`xarray.Dataset`
    :type prefix: str
    """
    for key, value in di.items():
        if value is None:
            continue
        elif isinstance(value, bool):
            value = int(value)
        elif isinstance(value, dict):
            _save_dict(value, ds, prefix=(key + '_'))
        else:
            ds.attrs[prefix + key] = value


# def fun_covariance(x, *args):
#     """Objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Value of objective function.
#     :rtype: float
#     """
#     obj = np.dot(x, np.dot(args[0], x))

#     return obj


# def jac_covariance(x, *args):
#     """Jacobian of objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Jacobian vector.
#     :rtype: :py:class:`numpy.array`
#     """
#     J = 2 * np.dot(args[0], x)

#     return J


# def hess_covariance(x, *args):
#     """Hessian of objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Value of Hessian.
#     :rtype: :py:class:`numpy.array`
#     """
#     H = 2 * args[0]

#     return H
