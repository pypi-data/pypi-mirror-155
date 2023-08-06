"""Photovoltaic farm model definition."""
import pandas as pd
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.gridded_data_source import GriddedDataSourceBase
from e4clim.container.strategy import ExtractorBase
import e4clim.typing as e4tp
from e4clim.utils.climate import get_temperature_at_height
from e4clim.utils.learn import get_transform_function
from e4clim.utils.radiation import (
    HorizontalRadiationComputer, TiltedRadiationComputer)
from e4clim.utils import tools

#: Available-dataset names.
VARIABLE_NAMES: tp.Final[tp.Set[str]] = {
    'global_horizontal_et', 'global_horizontal_surf',
    'global_tilted_surf', 'generation', 'capacityfactor',
    'cell_efficiency'
}


class Strategy(ExtractorBase):
    """Photovoltaic model."""
    #: Default result name.
    DEFAULT_RESULT_NAME: tp.Final[str] = 'capacityfactor'

    #: Capacity factor.
    capacityfactor: xr.DataArray
    #: Cell efficiency.
    cell_efficiency: tp.Optional[xr.DataArray]
    #: Clearness index.
    clearness_index: tp.Optional[xr.DataArray]
    #: Generation.
    generation: tp.Optional[xr.DataArray]
    #: Global horizontal extraterrestrial irradiance.
    global_horizontal_et: tp.Optional[xr.DataArray]
    #: Global horizontal surface irradiance.
    global_horizontal_surf: tp.Optional[xr.DataArray]
    #: Global tilted surface irradiance.
    global_tilted_surf: tp.Optional[xr.DataArray]

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        """
        if parent.name != self.DEFAULT_RESULT_NAME:
            self.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    parent.result_name, self.DEFAULT_RESULT_NAME,
                    self.name))

        super(Strategy, self).__init__(
            parent=parent, name=name, cfg=cfg, variable_names=VARIABLE_NAMES,
            **kwargs)

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Compute photovoltaic electricity generation from climate data.

        :param stage: Modeling stage: `'fit'` or `'predict'`.
          May be required if features differ in prediction stage.

        :returns: Transformed dataset.

        :raises AssertionError: if

            * :py:obj:`stage` attribute is `None`,
            * data source is not :py:class:`GriddedDataSourceBase`.

        """
        assert stage is not None, '"stage" argument is not optional here'

        data_src = self.data_sources[stage]
        variable_component_names = self.stage_variable_component_names[stage]
        assert isinstance(data_src, GriddedDataSourceBase), (
            'Data source for "{}" should be "ParsingMultiDataSourceBase"'
            ''.format(stage))

        # Download data if needed
        data_src.manage_download(
            variable_component_names=variable_component_names, **kwargs)

        # Functions to apply to the input climate data
        other_functions: tp.Iterable[e4tp.TransformStrictType] = [
            self.get_generation, data_src.get_regional_mean]
        transform_function = get_transform_function(
            data_src, stage, other_functions=other_functions,
            modifier=self.parent.modifier)

        # Get pv generation from climate data
        ds = data_src.parse_finalize(
            transform=transform_function,
            variable_component_names=variable_component_names)

        return ds

    def get_extractor_postfix(self, **kwargs) -> str:
        """Get extractor postfix.

        returns: Postfix.
        """
        postfix = '{}_{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        return postfix

    def get_generation(
            self, ds: xr.Dataset = None,
            data_src: GriddedDataSourceBase = None, **kwargs) -> xr.Dataset:
        """Compute the photovoltaic electricity generation
        from the daily climate dataset.

        :param ds: Dataset containing climate variables from which to
          compute generation.
        :param data_src: Data source object from which to get features.

        :returns: A dataset containing the electricity generation.

        :raises AssertionError: if

            * :py:obj:`ds` argument is `None`,
            * :py:obj:`data_src` argument is `None`.

        .. note::
          * The dataset should contain a `lat` and a `lon` coordinate
            variables.
          * The dataset should contain a `surface_downward_radiation` variable
            for the global horizontal radiation at the surface.
          * If the dataset contains a `surface_temperature` variable
            for the surface temperature,
            the temperature dependent cell efficiency is computed.
          * If the dataset contains a `surface_temperature` variable
            for the surface temperature,
            the temperature dependent cell efficiency is computed.

        .. warning:: Time index in dataset :py:obj:`ds` should be UTC.

        """
        assert ds is not None, '"ds" argument required'
        assert data_src is not None, '"data_src" argument required'

        # Get HOURLY time index (UTC)
        time = ds.indexes['time']
        freq_data = time.inferred_freq.upper()
        if freq_data in ['D', '1D']:
            time = pd.date_range(start=time[0], freq='H',
                                 end=(time[-1] + pd.Timedelta(23, 'H')))

        # Get surface temperature
        temp_a = None
        if 'surface_temperature' in ds:
            temp_0 = ds['surface_temperature']
            z_0 = float(temp_0.attrs['height'])

            # Adjust to surface temperature (2m)
            temp_a = get_temperature_at_height(temp_0, z_0, 2.)

        # Get hourly global horizontal extraterrestrial radiation
        self.info('Getting hourly global extraterrestrial solar radiation')
        hrc_hour = HorizontalRadiationComputer(
            time, ds.lat, ds.lon,
            global_horizontal_surf=ds['surface_downward_radiation'],
            angles_in_degrees=True)
        self.global_horizontal_et = hrc_hour.global_horizontal_et

        # Recycle solar computer
        sc_hour = hrc_hour.sc

        cfg_surface = tools.get_required_mapping_entry(self.cfg, 'surface')
        if freq_data in ['D', '1D']:
            if temp_a is not None:
                # Up-sample temperature
                temp_a = temp_a.resample(time='H').ffill().reindex(
                    time=time, method='ffill')

            # Get daily-mean global horizontal extraterrestrial radiation
            self.info('Getting daily-mean global horizontal extraterrestrial '
                      'solar radiation')
            global_horizontal_et_day = self.global_horizontal_et.resample(
                time='D').mean('time', keep_attrs=True)
            global_horizontal_surf_day = ds['surface_downward_radiation']

            # Get clearness index from DAILY-averaged
            # toa and surface radiations
            self.info('Getting daily-mean clearness index')
            rc_day = HorizontalRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=global_horizontal_et_day,
                global_horizontal_surf=global_horizontal_surf_day,
                angles_in_degrees=True)
            clearness_index_day = rc_day.clearness_index

            # Up-sample daily clearness index to hourly
            self.info('Up-sampling clearness index to hours')
            self.clearness_index = clearness_index_day.resample(
                time='H').ffill().reindex(time=time, method='ffill')

            # Radiations computation from clearness index and hourly
            # global horizontal extraterrestrial radiation
            self.info(
                'Getting hourly global horizontal surface radiation from '
                'hourly horizontal extraterrestrial radiation and '
                'up-sampled clearness index')
            rc_hour = TiltedRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=self.global_horizontal_et,
                clearness_index=self.clearness_index,
                angles_in_degrees=True, solar_computer=sc_hour, **cfg_surface)

            self.global_horizontal_surf = rc_hour.global_horizontal_surf

        elif freq_data in ['H', '1H']:
            # Radiations computation from hourly global horizontal
            # extraterrestrial and surface radiation (from source)
            self.global_horizontal_surf = ds['surface_downward_radiation']
            rc_hour = TiltedRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=self.global_horizontal_et,
                global_horizontal_surf=self.global_horizontal_surf,
                angles_in_degrees=True, solar_computer=sc_hour, **cfg_surface)

        self.info('Computing hourly global tilted surface radiation')
        self.global_tilted_surf = rc_hour.global_tilted_surf

        # Get hourly solar generation
        self.info('Computing hourly photovoltaic generation')
        cfg_module = tools.get_required_mapping_entry(self.cfg, 'module')
        self.generation, self.cell_efficiency = get_pv_power(
            self.global_tilted_surf, temp_a, **cfg_module)

        # Get hourly capacity factor
        nominal_power = tools.get_required_float_entry(
            cfg_module, 'nominal_power')
        self.capacityfactor = self.generation / nominal_power

        # Save key variables in object (e.g. for plots)
        if self.med.cfg['frequency'] == 'day':
            # Add daily-integrated variables to dataset
            self.info('Resampling from hourly to daily frequency')
            for variable_name in VARIABLE_NAMES:
                setattr(self, variable_name, getattr(
                    self, variable_name).resample(time='D').sum(
                        'time', keep_attrs=True))

            # Manage daily units
            generation_units = 'Wh/d'
            self.capacityfactor /= 24
        else:
            generation_units = 'Wh'

        try:
            self.capacityfactor.name = self.parent.result_name
            self.capacityfactor.attrs['long_name'] = (
                'Photovoltaic Capacity Factor')
            self.capacityfactor.attrs['units'] = ''
            self.generation.attrs['units'] = generation_units
        except AttributeError:
            pass

        ds = xr.Dataset({variable_name: getattr(self, variable_name)
                         for variable_name in VARIABLE_NAMES})

        return ds


def get_pv_power(
        global_tilted_surf: xr.DataArray, temp_a: xr.DataArray = None,
        wind_speed: tp.Union[xr.DataArray, float] = 1., area: float = 1.675,
        n_modules: int = 1, eff_elec: float = 0.86, eff_cell: float = None,
        thermal_loss: float = 0.004, temp_ref: float = 298.15,
        temp_cell_noct: float = 319.15,
        nominal_power: float = None) -> tp.Tuple[
            xr.DataArray, xr.DataArray]:
    """Set photovoltaic power from inclinaison, clearness index
    and surface air temperature.

    :param global_tilted_surf: Global tilted surface radiation
      (W/m2, or Wh/m2/h).
    :param temp_a: Surface air temperature (K).
      If None, the temperature of the cell is considered to be the same
      as the reference temperature temp_ref.
    :param wind_speed: Magnitude of the wind velocity (m/s).
    :param area: Area of each module (m2).
    :param n_modules: Number of modules.
    :param eff_elec: Efficiency of the electronics
      (inverter, array and power conditionning, etc.).
    :param eff_cell: Efficiency of the cell at the reference temperature
      temp_ref. If None, compute it from the nominal power.
    :param thermal_loss: Efficiency loss per degree Kelvin
      away from the reference temperature.
    :param temp_ref: Reference temperature (K).
    :param temp_cell_noct: Cell temperature at the
      Nominal Operating Cell Temperature (NOCT) (K).
    :param nominal_power: Nominal power of the module (W). See note.
      Only used to compute the efficiency of the cell eff_cell
      at the reference temperature temp_ref if eff_cell is not given.

    :returns: Electric power delivered by the array (W/m2, or Wh/m2/h).

    .. warning::
      The global tilted radiation `global_tilted_surf` should be given as
      power in W/m2, or as averaged power in Wh/m2/h to avoid erros
      in cell efficiency computations.
    """
    # Temperature dependent efficiency of the cell
    eff_cell_t = get_cell_efficiency(
        temp_a=temp_a, global_tilted_surf=global_tilted_surf, area=area,
        wind_speed=wind_speed, eff_cell=eff_cell, thermal_loss=thermal_loss,
        temp_ref=temp_ref, temp_cell_noct=temp_cell_noct,
        nominal_power=nominal_power)

    # Electric power delivered by the array
    total_area = area * n_modules
    total_radiation = tp.cast(xr.DataArray, total_area) * global_tilted_surf
    total_eff = tp.cast(xr.DataArray, eff_elec) * eff_cell_t
    generation = total_eff * total_radiation

    # Name power if possible
    if isinstance(generation, xr.DataArray):
        generation.name = 'generation'
        generation.attrs['long_name'] = 'Photovoltaic Array Generation'
        generation.attrs['units'] = (
            '{:s}'.format(global_tilted_surf.units.strip('/ m2'))
            if hasattr(global_tilted_surf, 'units') else 'Wh')

    return generation, eff_cell_t


def get_cell_efficiency(
        temp_a: xr.DataArray = None,
        global_tilted_surf: tp.Union[xr.DataArray, float] = 800.,
        wind_speed: tp.Union[xr.DataArray, float] = 1.,
        area: float = 1., eff_cell: float = None,
        thermal_loss: float = 0.004, temp_ref: float = 298.15,
        temp_cell_noct: float = 319.15,
        nominal_power: float = None) -> xr.DataArray:
    """Get temperature dependent cell efficiency.

    :param temp_a: Surface air temperature (K).
      If None, the temperature of the cell is considered to be the same
      as the reference temperature temp_ref.
    :param global_tilted_surf: Global tilted radiation (W/m2, or Wh/m2/h).
    :param wind_speed: Magnitude of the wind velocity (m/s).
    :param area: Area of each module (m2).
      (inverter, array and power conditionning, etc.).
    :param eff_cell: Efficiency of the cell at the reference temperature
      temp_ref. If None, compute it from the nominal power.
    :param thermal_loss: Efficiency loss per degree Kelvin
      away from the reference temperature.
    :param temp_ref: Reference temperature (K).
    :param temp_cell_noct: Cell temperature at _noct (K).
    :param nominal_power: Nominal power of the module (W). See note.
      Only used to compute the efficiency of the cell eff_cell
      at the reference temperature temp_ref if eff_cell is not given.

    :returns: Temperature dependent cell efficiency.

    :raises AssertionError: if both :py:obj:`eff_cell` and
      :py:obj:`nominal_power` are `None`.

    .. note::
        * The thermal model of Duffie and Beckman (2013)
          is used here to compute the efficiency of the cell
          for a given ambient temperature.
        * The global tilted radiation :py:obj:`global_tilted_surf` should be
          given as power in W/m2, or as averaged power in Wh/m2/h to avoid
          erros in cell efficiency computations.

    .. seealso::
        Duffie, J.A., Beckman, W.A., 2013.
        *Solar Energy and Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.
    """
    # Radiation on module plane at _noct (W/m2)
    global_tilted_surf_noct = 800.
    # Ambient Temperature at _noct (K)
    temp_a_noct = 293.15
    # Light intensity at STC (W/m2). See note.
    ir_std = 1000.

    # If not given, compute cell efficiency from nominal power
    if eff_cell is None:
        assert nominal_power is not None, (
            'Either "eff_cell" or "nominal_power" argument required')
        eff_cell = (nominal_power / ir_std) / area

    if temp_a is None:
        # If the ambient temperature is not given, the cell temperature
        # is taken as the same as the reference temperature. As a result,
        # the cell efficiency does not depend on the temperature.
        temp_cell = temp_ref
    else:
        # Compute temperature dependent efficiency of module
        loss_ratio = 9.5 / (5.7 + 3.8 * tp.cast(float, wind_speed))

        # Cell temperature (K). See note.
        temp_cell = (temp_a + (global_tilted_surf / global_tilted_surf_noct)
                     * loss_ratio * (temp_cell_noct - temp_a_noct))

    # Temperature dependent efficiency of the cell
    eff_cell_t = eff_cell * (1 - thermal_loss * (temp_cell - temp_ref))

    # Name
    if isinstance(eff_cell_t, xr.DataArray):
        eff_cell_t.name = 'cell_efficiency'
        eff_cell_t.attrs['long_name'] = 'Wheather Dependent Cell Efficiency'
        eff_cell_t.attrs['units'] = ''

    return tp.cast(xr.DataArray, eff_cell_t)
