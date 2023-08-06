"""Multi-data source with parsing methods."""
from orderedset import OrderedSet
import typing as tp
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools
from .multi_data_source import MultiDataSourceBase, _set_data_sources
from .parsing_data_source import ParsingDataSourceBase
from .parsing_single_data_source import ParsingSingleDataSourceBase


class ParsingMultiDataSourceBase(ParsingDataSourceBase, MultiDataSourceBase):
    """Parsing multi-data source."""
    data: e4tp.MultiDatasetMutableType

    #: Data sources composing multiple parsing data sources.
    _data_sources: e4tp.ParsingSingleDataSourcesType

    #: Variable to data-source mapping and variables list.
    var_data_sources: tp.MutableMapping[str, e4tp.SingleDataSourcesType]

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 data_sources: e4tp.SingleDataSourcesType = None,
                 name: str = None, cfg: e4tp.CfgType = None,
                 variable_component_names: e4tp.VCNType = None,
                 task_names=None, **kwargs):
        """Build data source with downloading and parsing capabilities.

        :param parent: Data-sources context.
        :param data_sources: Data-sources dictionary.
        :param name: Data-source name.
        :param med: Mediator.
        :param cfg: Data-source configuration.
        :param variable_component_names: Names of components per variable.
        :param parent: Parent container.
        :param task_names: Names of potential tasks for container to perform.
        """
        # Add download and parse tasks per variable
        if variable_component_names is not None:
            variable_names = tools.ensure_collection(variable_component_names,
                                                     OrderedSet)
            if task_names is None:
                task_names = OrderedSet()
            for variable_name in variable_names:
                task_names.add('parse__{}'.format(variable_name))
                task_names.add('download__{}'.format(variable_name))

        super(ParsingMultiDataSourceBase, self).__init__(
            parent, data_sources=data_sources, name=name, cfg=cfg,
            variable_component_names=variable_component_names,
            task_names=task_names, **kwargs)

    @property
    def data_sources(self) -> e4tp.ParsingSingleDataSourcesType:
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources:
                     e4tp.ParsingSingleDataSourcesType) -> None:
        _set_data_sources(self, data_sources)

    def get_single_data_source(
            self, variable_name: str) -> ParsingSingleDataSourceBase:
        """Get single data source containing variable.

        :param variable_name: Variable name.

        :returns: Data source(s) associated with variable.

        :raises AssertionError: if data source for variable is not unique.
        """
        data_sources = self.var_data_sources[variable_name]

        assert len(data_sources) == 1, (
            'Data source for "{}" is not unique'.format(variable_name))

        data_src = list(data_sources.values())[0]

        assert isinstance(data_src, ParsingSingleDataSourceBase), (
            'Data source should be "ParsingSingleDataSourceBase"')

        return data_src

    def download(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> None:
        """Download multiple data source calling
        :py:meth:`ParsingDataSourceBase.download` of each data source.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are downloaded.

        .. seealso:: :py:meth:`ParsingDataSourceBase.download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, ParsingDataSourceBase):
                data_src.download(
                    variable_component_names=variable_component_names,
                    **kwargs)

    def manage_download(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> None:
        """Manage multiple data-source download calling
        :py:meth:`ParsingDataSourceBase.manage_download` of each data source.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are downloaded.

        .. seealso:: :py:meth:`ParsingDataSourceBase.manage_download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, ParsingDataSourceBase):
                data_src.manage_download(
                    variable_component_names=variable_component_names,
                    **kwargs)

    def parse(self, variable_component_names: e4tp.VCNStrictType = None,
              **kwargs) -> e4tp.MultiDatasetType:
        """Parse multiple data source calling
        :py:meth:`ParsingDataSourceBase.parse` of each data source.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are parsed.

        .. seealso:: :py:meth:`ParsingDataSourceBase.parse`
        """
        d = {}
        for data_src_name, data_src in self.data_sources.items():
            if isinstance(data_src, ParsingDataSourceBase):
                multi_data = data_src.parse(
                    variable_component_names=variable_component_names,
                    **kwargs)
                d[data_src_name] = multi_data

        return d

    def parse_finalize(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> e4tp.MultiDatasetType:
        """Parse multiple data source calling
        :py:meth:`ParsingDataSourceBase.parse` of each data source and
        finalizing.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are parsed.

        .. seealso:: :py:meth:`ParsingDataSourceBase.parse`,
          :py:meth:`ParsingDataSourceBase.finalize_array`
        """
        d = {}
        for data_src_name, data_src in self.data_sources.items():
            # Parse and finalize
            d[data_src_name] = data_src.parse_finalize(
                variable_component_names=variable_component_names,
                **kwargs)

        return d

    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.MultiDatasetMutableType:
        """Parse data from multiple data sources calling
        :py:meth:`ParsingDataSourceBase.get_data` of each data source.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are taken.

        :returns: Dataset :py:attr:`data`.

        .. seealso:: :py:meth:`ParsingDataSourceBase.get_data`
        """
        return self.get_data_each_data_source(
            variable_component_names=variable_component_names, **kwargs)

    def get_data_each_data_source(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> e4tp.MultiDatasetMutableType:
        """Parse data from multiple data sources calling
        :py:meth:`ParsingDataSourceBase.get_data` of each data source.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are taken.

        :returns: Dataset :py:attr:`data`.

        .. seealso:: :py:meth:`ParsingDataSourceBase.get_data`
        """
        for data_src_name, data_src in self.data_sources.items():
            if isinstance(data_src, ParsingDataSourceBase):
                # Get data for single source, transmitting keywords
                data_src.get_data(
                    variable_component_names=variable_component_names,
                    **kwargs)

                self.data[data_src_name] = data_src.data

        return self.data

    def get_data_callback(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> None:
        """Get data callback for each data source.

        :param variable_component_names: Names of components per variable.
        """
        for data_src_name, data_src in self.data_sources.items():
            data_src.get_data_callback(
                variable_component_names=variable_component_names, **kwargs)

        return
