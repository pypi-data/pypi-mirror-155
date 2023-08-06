"""Data source reading from files direclty."""
from pathlib import Path
import typing as tp
import e4clim
from e4clim.container.gridded_data_source import (
    GriddedDataSourceBase)
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp
from e4clim.utils import tools


class DataSource(ParsingSingleDataSourceBase):
    """Data source reading from files direclty."""

    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'reader'

    def __init__(
            self, parent: 'e4clim.context.base.ContextBase',
            name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize data source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> tp.Optional[e4tp.VCNStrictType]:
        """Ignore download passing on variable to component names mapping."""
        return variable_component_names

    def parse(self, variable_component_names: e4tp.VCNType = None,
              **kwargs) -> e4tp.DatasetType:
        """Skip parsing data to read directly.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: :py:class:`xarray.Dataset()`
        """
        self.read(variable_component_names=variable_component_names, **kwargs)

        return self.data

    def get_data_path(self, variable_name: str = None, makedirs: bool = True,
                      **kwargs) -> Path:
        """Get data-source filepath.

        :param variable_name: Data variable.
        :param makedirs: Make directories if needed.

        :returns: Filepath.

        :raises AssertionError: if "variable_name" argument not provided..
        """
        assert variable_name is not None, '"variable_name" argument required'

        var_paths = tools.get_required_mapping_entry(self.cfg, 'path')
        path_list = tools.get_required_iterable_str_entry(
            var_paths, variable_name, list)

        return Path(*path_list)


class GriddedDataSource(GriddedDataSourceBase, DataSource):
    def __init__(
            self, parent: 'e4clim.context.base.ContextBase',
            name: str, cfg: e4tp.CfgType = None, **kwargs) -> None:
        """Initialize data source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        super(GriddedDataSource, self).__init__(
            parent, name, cfg=cfg, **kwargs)

        dims = tools.get_iterable_str_entry(self.cfg, 'dims', list)
        if dims is not None:
            self._dims = tuple(dims)

    def get_grid_filepath(self, *args, **kwargs) -> Path:
        """Return data file as gridded file.

        :returns: Grid filepath.
        """
        variable_name = list(self.variable_component_names)[0]

        return self.get_data_path(variable_name=variable_name, **kwargs)
