from orderedset import OrderedSet
import xarray as xr
import e4clim
from e4clim.container.strategy import ExtractorBase
import e4clim.typing as e4tp
from e4clim.utils import tools


class Strategy(ExtractorBase):
    """Default feature extractor implementation.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, parent: 'e4clim.context.context_result.ContextResult',
                 name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize strategy.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.

        :raises AssertionError: if :py:obj:`cfg` not given.

        .. note::

          * The name of the variables to concatenate are given in the
            `'variables_to_concat'` entry of the container configuration.
            If this entry is empty, the name of the strategy result manager
            is used instead.
          * The dimension along which to concatenate must be given
            in the `'dim_to_concat'` entry of the container configuration.
        """
        assert cfg is not None, '"cfg" argument required.'

        # Variables to concatenate.
        variable_names = tools.get_required_iterable_str_entry(
            cfg, 'variables_to_concat', OrderedSet,
            OrderedSet([self.parent.result_name]))

        # Extractor initialization
        super(Strategy, self).__init__(
            parent=parent, name=name, cfg=cfg,
            variable_names=variable_names, **kwargs)

        #: Dimension along which to concatenate.
        self.dim_to_concat = self.cfg.get('dim_to_concat')

    def transform(self, stage: str = None, **kwargs) -> e4tp.DatasetType:
        """Default transform: return identical data source
        and prevent writing.

        :param stage: Modeling stage: `'fit'` or `'predict'`.

        :returns: Dataset.

        :raises AssertionError: if data for variables in single data
          sources are not :py:class:`xarray.DataArray`.
        """
        assert stage is not None, '"stage" argument is not optional here'
        data_src = self.data_sources[stage]
        self.info(
            '{} {} feature concatenation along {} dimension:'.format(
                self.parent.parent.component_name, self.parent.result_name,
                self.dim_to_concat))

        # Get data (letting multiple data source manage variables)
        kwargs_data_src = kwargs.copy()
        kwargs_data_src.pop('variable_names', None)
        data_src.get_data(**kwargs_data_src)

        ds = {}
        for variable_name in self.variable_names:
            self.info(
                '  - Concatenating {} variable:'.format(variable_name))

            # Collect data for variable from all single data sources
            data = []
            for src_name, single_data_src in (
                    data_src.get_data_sources(variable_name).items()):
                self.info(
                    '    - Adding {} data source'.format(src_name))
                da = single_data_src[variable_name]
                assert isinstance(da, xr.DataArray), (
                    'data for variable "{}" in "{}" data source should be '
                    '"DataArray"'.format(variable_name, single_data_src.name))
                data.append(da)

            # Concatenate
            ds[variable_name] = xr.concat(data, dim=self.dim_to_concat)

        return ds
