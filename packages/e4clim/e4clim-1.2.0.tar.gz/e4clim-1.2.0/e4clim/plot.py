"""Various plot functions."""
from pathlib import Path
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pandas.plotting import register_matplotlib_converters
from e4clim.container.geo_data_source import GEO_VARIABLE_NAME
from e4clim.utils import tools

# Register matplotlib datetime-converter
register_matplotlib_converters()

# Matplotlib settings
plt.rc('figure', max_open_warning=0)
plt.rc('font', size=14)
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=(r'\usepackage{siunitx} '
                               r'\usepackage[gen]{eurosym}'))

#: Default plot-colors.
RC_COLORS = rcParams['axes.prop_cycle'].by_key()['color']

#: Default figure format.
DEFAULT_FIG_FORMAT = 'png'


def plot_mask(data_src, crs=None, facecolor='moccasin', edgecolor='dimgrey',
              alpha=0.2, transform=None, with_title=True, set_extent=True,
              cmap_name='tab20', legend=False, scale=0.8, **kwargs):
    """ Plot the mask assigning climate grid points to regions.

    :param data_src: Data source.
    :param crs: Coordinate Reference System (CRS).
    :param facecolor: Face color of the regions.
    :param edgecolor: Edge color of the regions.
    :param alpha: Alpha value for the markers colors.
    :param transform: CRS for transform option of plot methods.
    :param with_title: Whether to add title based on geographic and gridded
      data sources or not.
    :param set_extent: Wheter to reduce extent to mask points.
    :param cmap_name: Colormap name.
    :param legend: Whether to add legend.
    :param scale: Figure-size scale.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    :type alpha: float
    :type transform: :py:class:`cartopy.crs.ABCMeta`
    :type with_title: bool
    :type set_extent: bool
    :type cmap_name: str
    :type legend: bool
    :type zone_plot_kwds: dict
    :type scale: float
    """
    # Configuration
    med = data_src.med
    cfg_plot = med.parse_configuration('plot') or {}
    savefigs_kwargs = tools.get_required_mapping_entry(
        cfg_plot, 'savefigs_kwargs', {})
    fig_format = tools.get_required_str_entry(
        savefigs_kwargs, 'format', DEFAULT_FIG_FORMAT)
    fig_dir = med.cfg.get_plot_directory(data_src, **kwargs)
    markersize = 5
    facecolor = facecolor or tools.get_required_str_entry(
        cfg_plot, 'region_facecolor', 'moccasin')
    edgecolor = edgecolor or tools.get_required_str_entry(
        cfg_plot, 'region_edgecolor', 'dimgrey')
    crs = crs or ccrs.LambertAzimuthalEqualArea()
    fontsize = tools.get_str_entry(cfg_plot, 'fontsize')
    if fontsize:
        plt.rc('font', size=fontsize)
    show = tools.get_required_bool_entry(cfg_plot, 'show', True)

    # Get mask
    mask = data_src.get_mask(for_area=True, **kwargs)

    # Convert geometry to CRS
    gdf = med.geo_src.get_data()[GEO_VARIABLE_NAME]
    gdf_crs = gdf.to_crs(crs.proj4_init)

    # Plot
    med.info('Plotting {} mask for {}'.format(
        med.geo_src.name, data_src.name))
    figsize = rcParams['figure.figsize']
    legend_kwds = None
    if legend:
        legend_kwds = {'loc': 'center right', 'bbox_to_anchor': (1.73, 0.5),
                       'fontsize': 'small'}
        figsize = [figsize[0] / scale, figsize[1]]
    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    cmap = plt.cm.get_cmap(cmap_name, len(gdf_crs))

    # Plot regions
    gdf_crs.reset_index().plot(
        column='zone', ax=ax, facecolor=facecolor, edgecolor=edgecolor,
        cmap=cmap, legend=legend, legend_kwds=legend_kwds, alpha=alpha)

    # Resize box for legend
    if legend:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * scale, box.height])

    # Get grid points within regions
    in_domain = np.where(mask['mask'] > 1)
    if len(in_domain) == 1:
        icoord = in_domain[0]
    else:
        ilat_in, ilon_in = in_domain
        icoord = list(zip(ilat_in, ilon_in))

    if transform is None:
        transform = ccrs.PlateCarree()

    for ic in icoord:
        icc = tools.ensure_collection(ic, list)
        if len(icc) > 1:
            lat, lon = mask.lat[icc[0], icc[1]], mask.lon[icc[0], icc[1]]
            place_index = mask['mask'][icc[0], icc[1]]
        else:
            lat, lon = mask.lat[icc[0]], mask.lon[icc[0]]
            place_index = mask['mask'][icc[0]]
        place_name = str(mask['region'][
            mask.region_index == place_index][0].values)
        c = cmap(np.nonzero(gdf_crs.index == place_name)[0][0])

        ax.scatter(lon, lat, s=markersize, transform=transform, color=c)
    if set_extent:
        if len(in_domain) == 1:
            mask_in = mask.mask[icoord]
        else:
            mask_in = mask.mask[icoord[0], icoord[1]]
        ax.set_extent([mask_in.lon.min(), mask_in.lon.max(),
                       mask_in.lat.min(), mask_in.lat.max()])
    if with_title:
        ax.set_title('{} {}'.format(
            med.geo_src.name.replace('_', '-'), data_src.name.replace('_', '-')))

    fig_filename = 'mask{}.{}'.format(data_src.get_mask_postfix(), fig_format)
    fig_filepath = Path(fig_dir, fig_filename)
    med.info('Saving figure for {} mask for {} to {}'.format(
        med.geo_src.name, data_src.name, fig_filepath))
    fig.savefig(fig_filepath, **savefigs_kwargs)

    if show:
        plt.show(block=False)


def plot_data_source(data_src, per_region=None, **kwargs):
    """ Plot data from a given source.

    :param data_src: Data source.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type per_region: bool

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    fig_dir = data_src.med.cfg.get_plot_directory(data_src, **kwargs)
    info_msg = ' {}'.format(data_src.name)

    # Get data
    data_src.get_data(**kwargs)

    # Plot dataset
    for variable_name in data_src.variable_component_names:
        plot_regional_dataset(
            data_src, variable_name, fig_dir=fig_dir, info_msg=info_msg,
            per_region=per_region, **kwargs)


def plot_result(context, result_name='result',
                stage=None, per_region=None, **kwargs):
    """ Plot features of a given result manager.

    :param context: Result manager of variable for which to plot
      features.
    :param result_name: `'feature'` or `'prediction'`.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
      Should be provided for `'fit'`.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
    :type context: :py:class:`.component.ContextResult`
    :type result_name: str
    :type stage: str

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    # Get data
    info_msg = ' {}'.format(result_name)
    if result_name == 'feature':
        # Plot feature
        # Make sure that result is loaded and get data
        context.extract(stage, **kwargs)
        data_src = context.feature[stage]
        if not data_src.data:
            return
        info_msg += ' to {}'.format(stage)
    elif result_name == 'result':
        # Plot prediction or (extracted) output
        # Make sure that result is loaded and get data
        context.get_data(**kwargs)

    info_msg += ' {}'.format(context.parent.name)
    fig_dir = context.med.cfg.get_plot_directory(
        context.parent, **kwargs)

    for variable_name in context.variable_component_names:
        plot_regional_dataset(
            context, variable_name, fig_dir=fig_dir, info_msg=info_msg,
            per_region=per_region, **kwargs)


def plot_regional_dataset(data_src, variable_name, fig_dir='', info_msg='',
                          per_region=None, **kwargs):
    """Plot all variable of a regional dataset.

    :param data_src: Dataset.
    :param variable_name: Variable name.
    :param fig_dir: Directory in which to save figure.
    :param info_msg: Log and title information message.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
    :type data_src: mapping
    :type variable_name: str
    :type fig_dir: str
    :type info_msg: str
    :type per_region: bool
    """
    med = data_src.med
    cfg_plot = med.parse_configuration('plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    per_region = per_region or cfg_plot.get('per_region', True)
    fontsize = cfg_plot.get('fontsize')
    if fontsize:
        plt.rc('font', size=fontsize)
    show = cfg_plot.get('show') or True

    med.info('Plotting {} {}'.format(info_msg, variable_name))
    var = data_src.get_data()[variable_name]
    med.info('Variable: {}'.format(variable_name))

    # Define y label with units
    label_units = _get_label_units(var.attrs.get('units'))
    ylabel = r'{}{}'.format(variable_name, label_units)

    # Plot per region
    if not hasattr(var, 'region'):
        # Check if regional data
        var = var.expand_dims(dim='region', axis=-1).assign_coords(
            region=['all'])
    time = var.indexes['time']
    freq_data = time.inferred_freq
    if freq_data is None:
        if (time[1] - time[0]).seconds == 3600:
            freq_data = 'H'
    freq_data = freq_data.upper()
    if ((med.cfg['frequency'] == 'day') and
            (freq_data in ['H', '1H'])):
        var = var.resample(time='D').mean('time')
    for ir, reg_label in enumerate(var.indexes['region']):
        plot_postfix = '_{}'.format(reg_label) if per_region else ''
        reg_msg = ' - {}'.format(reg_label) if per_region else ''
        if per_region or (ir == 0):
            fig, ax = plt.subplots(1, 1)
            da = var.loc[{'region': reg_label}]
            time = da.indexes['time']
            try:
                for component_name in var.indexes['component']:
                    label = '{} {}'.format(component_name, reg_label)
                    ax.plot(time, da.loc[{'component': component_name}],
                            label=label)
            except KeyError:
                ax.plot(time, da, label=reg_label)

        last = (ir == len(var.indexes['region']) - 1)
        if not per_region and last:
            ax.legend(loc='best')
        if per_region or last:
            # Set axes
            ax.set_xlim(time[0], time[-1])
            ax.set_xlabel('time')
            ax.set_ylabel(ylabel)
            info_msg_title = ' '.join(info_msg.split('_'))
            title = '{}{} {}'.format(reg_msg, info_msg_title, variable_name)
            ax.set_title(title)

            # Save figure
            result_postfix = data_src.get_data_postfix(
                variable_name=variable_name, **kwargs)
            fig_filename = '{}{}{}.{}'.format(
                variable_name, result_postfix, plot_postfix, fig_format)
            fig_filepath = Path(fig_dir, fig_filename)
            med.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if show:
        plt.show(block=False)


def plot_generation_feature(context, stage, **kwargs):
    """Plot generation features of a given result manager.

    :param context: Result manager for which to plot features.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
    :type context: :py:class:`.component.ContextResult`
    :type stage: str
    """
    # Plot
    med = context.med
    cfg_plot = med.parse_configuration('plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    fig_dir = med.cfg.get_plot_directory(
        context.parent, **kwargs)
    fig_dir.mkdir(parents=True, exist_ok=True)
    fontsize = cfg_plot.get('fontsize')
    if fontsize:
        plt.rc('font', size=fontsize)
    show = cfg_plot.get('show') or True
    freq = cfg_plot.get('frequency') or 'hour'
    med.info('Plotting features to {} {}'.format(
        stage, context.name))

    # Get data
    context.extract(stage)
    data_src = context.feature[stage]
    if not data_src.data:
        return
    result_postfix = data_src.get_data_postfix(**kwargs)

    # Configure
    units = {'week': 'Wh/w', 'day': 'Wh/d', 'hour': 'Wh/h'}[freq]
    sample_dict = {'hour': 'H', 'day': 'D', 'week': 'W', 'month': 'M',
                   'year': 'Y'}
    sampling = sample_dict[freq]

    # Define groups to plot
    if context.parent.component_name == 'pv':
        groups = {
            # 'irradiance': {
            #     'Irradiance (' + units + '/m2)':
            #     ['global_horizontal_et', 'global_horizontal_surf',
            #      'glob_tilted_surf']},
            'generation': {
                r'PV Generation ($\si{{ {} }}$)'.format(units): ['generation'],
                'Cell Efficiency': ['cell_efficiency']},
            'capacityfactor': {
                'Capacity Factor': ['capacityfactor']}
        }
    elif context.parent.component_name in [
            'wind', 'wind-onshore', 'wind-offshore']:
        groups = {
            'generation': {
                r'Wind Generation ($\si{{ {} }}$)'.format(units):
                ['generation']},
            'capacityfactor': {
                'Capacity Factor': ['capacityfactor']}
        }

    # Get regions
    regions = list(data_src.data.values())[0].indexes['region']

    # Plot for each region
    for reg_label in regions:
        plot_postfix = '_{}_{}'.format(reg_label, freq)

        # Plot per groups
        for group_name, group in groups.items():
            fig = plt.figure()
            ax0 = fig.add_subplot(111)
            any_plot = False
            for k, (label, variable_names) in enumerate(group.items()):
                ax = ax0 if k == 0 else ax0.twinx()
                for iv, variable_name in enumerate(variable_names):
                    da_reg = data_src.get(variable_name)
                    if da_reg is not None:
                        da_reg = da_reg.loc[{'region': reg_label}]
                        da = da_reg.resample(time=sampling).mean(
                            'time', keep_attrs=True)
                        tm = da.indexes['time']
                        ic = (k * len(variable_names) + iv) % len(RC_COLORS)
                        ax.plot(tm, da, label=da.attrs.get('long_name'),
                                color=RC_COLORS[ic])
                        any_plot = True
                ax.set_ylabel(label, color=RC_COLORS[k])
                if len(variable_names) > 1:
                    ax.legend()
            if any_plot:
                ax0.set_xticks(ax.get_xticks()[::2])
                ax0.set_xlabel('time')
                ax0.set_title('{} {} {} {}'.format(
                    reg_label, context.parent.name, stage, freq))
                fig_filename = '{}{}{}.{}'.format(
                    group_name, result_postfix, plot_postfix, fig_format)
                fig_filepath = Path(fig_dir, fig_filename)
                med.info('Saving figure to {}'.format(fig_filepath))
                fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if show:
        plt.show(block=False)


def plot_geo_dist(
        optimizer, lat, lon, capa_pv, capa_wind, mean_penetration=None,
        margin=2., alpha=1., n_markers=4, ms_max=1300., capa_max=10000.,
        trans=0.006, crs=None, facecolor=None, edgecolor=None,
        text=False, units='MW', text_format='{:.1f}', **kwargs):
    """ Plot geographical and technological distribution of RES capacity.

    :param optimizer: Optimizer.
    :param lat: Mean latitude of the regions.
    :param lon: Mean longitude of the regions.
    :param capa_pv: PV capacities.
    :param capa_wind: Wind capacities.
    :param cfg_plot: Plot configuration.
    :param mean_penetration: Penetration rate to add as annotation.
      If `None`, no annotation is added.
    :param margin: Margin at the borders of the plot.
    :param alpha: Alpha value for the markers colors.
    :param n_markers: Number of markers in legend.
    :param ms_max: Maximum marker size.
    :param capa_max: Maximum capacity in legend.
    :param trans: Translation factor to seperate
      markers of the different technologies.
    :param crs: Coordinate Reference System.
    :param facecolor: Face color of the regions.
    :param edgecolor: Edge color of the regions.
    :param text: Whether to add text boxes.
    :param units: The units of the given data.
    :param text_format: Format of the text boxes.
    :type optimizer: :py:class:`.optimization.OptimizerBase`
    :type lat: sequence
    :type lon: sequence
    :type capa_pv: sequence
    :type capa_wind: sequence
    :type cfg_plot: dict
    :type mean_penetration: float
    :type margin: float
    :type alpha: float
    :type n_markers: int
    :type ms_max: float
    :type capa_max: float
    :type trans: float
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    :type text: bool
    :type units: str
    :type text_format: str
    """
    med = optimizer.med
    cfg_plot = med.parse_configuration('plot')
    facecolor = facecolor or cfg_plot.get('region_facecolor') or 'moccasin'
    edgecolor = edgecolor or cfg_plot.get('region_edgecolor') or 'dimgrey'
    crs = crs or ccrs.LambertAzimuthalEqualArea()
    fontsize = cfg_plot.get('fontsize')
    if fontsize:
        plt.rc('font', size=fontsize)

    # Convert geometry to CRS
    gdf = med.geo_src.get_data(**kwargs)[GEO_VARIABLE_NAME]
    gdf_crs = gdf.to_crs(crs.proj4_init)

    fig = plt.figure(figsize=[12, 9])
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Plot regions
    gdf_crs.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor)

    # capa_max = np.max([capa_pv.max(), capa_wind.max()])
    leg_size = (np.round(np.linspace(0., 1., n_markers + 1)[1:], 2)
                * np.round(capa_max, -int(np.log10(capa_max)) + 1))
    exp = 1
    fact = ms_max / leg_size.max()**exp
    trans *= (lon.max() - lon.min()) / 2
    trans_lon = trans * (lon.max() - lon.min()) / 2
    trans_lat = trans * (lat.max() - lat.min()) / 2

    # Draw capacity
    s = capa_pv**exp * fact
    ax.scatter(lon - trans * np.sqrt(s), lat, s=s, c=RC_COLORS[0],
               marker='o', alpha=alpha, transform=ccrs.PlateCarree())

    s = capa_wind**exp * fact
    ax.scatter(lon + trans * np.sqrt(s), lat, s=s, c=RC_COLORS[1],
               marker='o', alpha=alpha, transform=ccrs.PlateCarree())

    # Add text
    if text:
        for k, (c_pv, c_wind) in enumerate(zip(capa_pv, capa_wind)):
            transform = ccrs.PlateCarree()._as_mpl_transform(ax)
            # Annotate PV
            t_lon = lon[k] - 30 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_pv.values), xy=(t_lon, t_lat),
                        xycoords=transform)
            # Annotate wind
            t_lon = lon[k] + 15 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_wind.values), xy=(t_lon, t_lat),
                        xycoords=transform)

    # Draw legend
    h_pv = [plt.plot([-1e9], [-1e9], linestyle='',
                     marker='$\mathrm{PV}$', color='k', markersize=20)[0]]
    h_wind = [plt.plot([-1e9], [-1e9], linestyle='',
                       marker='$\mathrm{Wind}$', color='k', markersize=40)[0]]
    h_pv += [plt.scatter(
        [], [], s=leg_size[s]**exp * fact, c=RC_COLORS[0],
        marker='o', alpha=alpha) for s in np.arange(n_markers)]
    h_wind += [plt.scatter([], [], s=leg_size[s]**exp * fact,
                           c=RC_COLORS[1], marker='o',
                           alpha=alpha) for s in np.arange(n_markers)]
    l_pv, l_wind = [''], ['']
    l_pv += ['' for s in np.arange(n_markers)]
    l_wind += [r'{:} $\si{{MW}}$'.format(int(leg_size[s]))
               for s in np.arange(n_markers)]
    l_wind += [r'{:} $\si{{ {} }}$'.format(int(leg_size[s]), units)
               for s in np.arange(n_markers)]
    ax.legend(h_pv + h_wind, l_pv + l_wind, loc='best', handletextpad=1.,
              labelspacing=2.5, borderpad=1.5, ncol=2, columnspacing=1.5)

    if mean_penetration is not None:
        starget = r'$\mu^* = {:.1f}\%$'.format(mean_penetration * 100)
        plt.annotate(starget, xy=(0.7, 0.02), xycoords='axes fraction')

    # Set extent
    tb = gdf_crs.total_bounds
    extent = tb[0], tb[2], tb[1], tb[3]
    ax.set_extent(extent, crs)

    return fig


def plot_band_spectrum(med, ds, filt, time_slice=None,
                       plot_freq=['Y', 'D', 'H'], var_ylims={},
                       add_legend=False, **kwargs):
    """Plot band spectrum, i.e. the integration of power spectrum over
    frequency bands.

    :param med: Mediator.
    :param ds: Dataset of output variables of components.
    :param filt: Filtered data.
    :param time_slice: Period to select.
    :param plot_freq: Frequencies for which to plot.
    :param var_ylims: Mapping of y-axis limits to result-manager names.
    :param add_legend: Whether to add the legend.
    :type med: :py:class:`.mediator.Mediator`
    :type ds: mapping
    :type filt: mapping
    :type time_slice: slice
    :type plot_freq: sequence
    :type var_ylims: mapping
    :type add_legend: bool
    """
    cfg_plot = med.parse_configuration('plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    lw = {'Y': 3, 'D': 2, 'H': 1}
    zo = {'Y': 3, 'D': 2, 'H': 1}
    labels = {'Y': 'Yearly-mean', 'D': 'Daily-mean', 'H': 'Hourly'}
    var_labels = {'demand': '', 'capacityfactor': 'Capacity Factor'}
    comp_labels = {
        'demand': 'Demand', 'pv': 'PV', 'wind': 'Wind',
        'wind-onshore': 'Onshore Wind', 'wind-offshore': 'Offshore Wind'}
    figsize = kwargs.get('figsize') or rcParams['figure.figsize']
    fontsize = cfg_plot.get('fontsize')
    if fontsize:
        plt.rc('font', size=fontsize)
    show = cfg_plot.get('show') or True

    for context_component_name, ds_comp in ds.items():
        context_component = med[context_component_name]
        fig_dir = med.cfg.get_plot_directory(context_component, **kwargs)
        for res_variable_name, da in ds_comp.items():
            context = context_component[res_variable_name]
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            filt_var = filt[context_component_name][res_variable_name]
            for ifr, freq in enumerate(filt_var):
                dum = filt_var[freq]
                if time_slice is not None:
                    dum = dum.sel(time=time_slice)
                if ifr == 0:
                    ts = dum
                else:
                    ts += dum
                if freq in plot_freq:
                    ax.plot(ts.time, ts, linewidth=lw[freq], zorder=zo[freq],
                            label=labels[freq])

            ylabel = '{} {}'.format(comp_labels[context_component_name],
                                    var_labels[res_variable_name])
            label_units = _get_label_units(da.attrs.get('units'))
            if (not label_units) and (res_variable_name == 'capacityfactor'):
                label_units = r' (\si{{\%}})'
            ylabel += label_units
            ax.set_ylabel(ylabel)
            # Add limits
            ylim = var_ylims.get(res_variable_name)
            if ylim is not None:
                ax.set_ylim(ylim)

            # Add legend only if regions not present
            if add_legend:
                ax.legend(loc='upper right')

            # Save figure
            result_postfix = context.get_data_postfix(**kwargs)
            if time_slice is not None:
                result_postfix += '_{}_{}'.format(
                    time_slice.start, time_slice.stop)
            fig_filename = 'filtered_{}{}.{}'.format(
                context.name, result_postfix, fig_format)
            fig_filepath = Path(fig_dir, fig_filename)
            med.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if show:
        plt.show(block=False)


def _get_label_units(units):
    """Get label unit.

    :param prop_name: Property name.
    :type prop_name: str

    :returns: Label unit.
    :rtype: str
    """
    return r' ($\si{{ {} }}$)'.format(units) if units else ''
