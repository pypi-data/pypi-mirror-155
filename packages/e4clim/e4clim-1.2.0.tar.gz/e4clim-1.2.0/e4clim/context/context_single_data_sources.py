from e4clim.config import import_class_from_cfg
from e4clim.container.base import ContainerBase
from e4clim.container.single_data_source import SingleDataSourceBase
import e4clim.typing as e4tp
from .base import ContextBase


class ContextSingleDataSourcesMixin(ContextBase):
    """To mix with :py:class:`.context_data_sources.ContextDataSources`
    to manage single data sources."""

    _data_sources: e4tp.DataSourcesType

    def __init__(self, parent: ContainerBase,
                 name: str = 'context_data_sources', cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize data-source context.

        :param parent: Parent.
        :param name: Name.
        :param cfg: Configuration.
        """
        super(ContextSingleDataSourcesMixin, self).__init__(
            name, cfg=cfg, parent=parent, **kwargs)

    def build_single_data_source(
            self, name: str,
            variable_component_names: e4tp.VCNType = None,
            parent: ContainerBase = None, **kwargs) -> SingleDataSourceBase:
        """Initialize a data source, inject to context,
        and return it as well.

        :param name: Data-source name.
        :param variable_component_names: Names of components per variable.
        :param parent: Container for which to add data source.

        :returns: Data source.

        :raises AssertionError: if data source not
          :py:class:`e4clim.container.single_data_source.SingleDataSourceBase`.
        """
        # Verify that data source not already added by other containers
        if name not in self._data_sources:
            data_src = self.build_data_source(
                name, variable_component_names, parent, **kwargs)
            self._data_sources[name] = data_src
            self.info('{} data source injected'.format(name))
        else:
            data_src_any = self._data_sources[name]

            assert isinstance(data_src_any, SingleDataSourceBase), (
                'Data source should be "SingleDataSourceBase"')

            data_src = data_src_any
            # Add variable names to existing data source, if needed
            if variable_component_names is not None:
                data_src.update_variables(variable_component_names)

        return data_src

    def build_data_source(
            self, name: str, variable_component_names: e4tp.VCNType = None,
            parent: ContainerBase = None, **kwargs) -> SingleDataSourceBase:
        """Build data source.

        :param name: Data-source name.
        :param variable_component_names: Names of components per variable.
        :param parent: Container for which to add data source.

        :returns: Data source.

        :raises AssertionError: if data-source configuration not found.
        """
        # Add data source configuration
        cfg_src = self.med.parse_configuration(name, parent)

        assert cfg_src is not None, (
            '"{}" configuration required but not found'.format(name))

        theclass = import_class_from_cfg(cfg_src)

        assert (theclass is not None), (
            'Could not import class for "{}" data source'.format(name))

        # Create data source and inject it to context
        data_src = theclass(
            self, name, cfg=cfg_src,
            variable_component_names=variable_component_names, **kwargs)

        return data_src
