"""Multi-data source."""
from collections import OrderedDict
from orderedset import OrderedSet
import typing as tp
import e4clim
import e4clim.typing as e4tp
from .data_source import DataSourceBase
from .single_data_source import SingleDataSourceBase


class MultiDataSourceBase(DataSourceBase):

    data: e4tp.MultiDatasetMutableType

    #: Data sources composing multiple single data sources.
    _data_sources: e4tp.SingleDataSourcesType

    #: Variable to data-source mapping and variables list.
    var_data_sources: tp.MutableMapping[str, e4tp.SingleDataSourcesType]

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 data_sources: e4tp.SingleDataSourcesType = None,
                 name: str = None,
                 task_names: e4tp.StrIterableType = OrderedSet(),
                 default_tasks_value: bool = True, **kwargs) -> None:
        """Build data source composed to multiple data sources.

        :param parent: Data-source context.
        :param data_sources: Data-sources dictionary.
        :param name: Name.
        :param task_names: Names of potential tasks for container to perform.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none.

        :raises AssertionError: if both :py:obj:`name` and :py:obj:`data_sources`
          arguments are `None`.
        """
        # Multiple data-source attributes specification
        if name is None:
            assert data_sources is not None, (
                '"data_sources" argument required to infer name when "None".')
            name = self.get_name(data_sources)

        # Initialize as data source
        super(MultiDataSourceBase, self).__init__(
            parent, name, task_names=task_names,
            default_tasks_value=default_tasks_value, **kwargs)

        self.data = OrderedDict()

        self.var_data_sources = OrderedDict()

        if data_sources is not None:
            self.data_sources = data_sources

    @property
    def data_sources(self) -> e4tp.SingleDataSourcesType:
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources: e4tp.SingleDataSourcesType) -> None:
        _set_data_sources(self, data_sources)

    def __setitem__(self, variable_name: str, data: e4tp.DatasetType) -> None:
        """Set items in data sources containing variable.

        :param variable_name: Variable name.
        :param data: Data of variable to set.
        """
        # Data source containing variable
        data_sources = self.var_data_sources[variable_name]

        # Set variable in data source
        for src_name, src_data in data.items():
            data_sources[src_name][variable_name] = src_data
            self.data[src_name][variable_name] = src_data

    @staticmethod
    def get_name(data_sources: tp.Union[e4tp.SingleDataSourcesType,
                                        tp.Iterable[str]]) -> str:
        """Get class name from data_sources.

        :param data_sources: Data-sources list or data-source names list.

        :returns: Multiple data-source name.
        """
        # Note: in principle, data_sources' keys correspond to name
        # attribute of each data_src
        if isinstance(data_sources, tp.Mapping):
            name = '__'.join(data_src.name
                             for data_src in data_sources.values())
        else:
            name = '__'.join(data_sources)

        return name

    def __getitem__(self, variable_name: str) -> tp.Union[
            e4tp.DataArrayType, e4tp.DatasetType]:
        """Get variable data from :py:attr:`data` of data source
          containing variable.

        :param variable_name: Variable name.

        :returns: Variable.

        .. seealso:: :py:meth:`get_single_data_source`
        """
        data_src = self.get_single_data_source(variable_name)

        return data_src[variable_name]

    def get(self, variable_name: str, default=None) -> tp.Union[
            tp.Optional[e4tp.DataArrayType],
            tp.Optional[e4tp.DatasetType]]:
        """Get variable data from :py:attr`data`.

        :param variable_name: Variable name.
        :param default: Default value.

        :returns: Variable.

        .. seealso:: :py:meth:`get_single_data_source`
        """
        data_src = self.get_single_data_source(variable_name)

        return data_src.get(variable_name, default)

    def __contains__(self, variable_name: object) -> bool:
        """Test if variable in data source.

        :param variable_name: Variable name.
        """
        return variable_name in self.variable_component_names

    def __delitem__(self, variable_name: str) -> None:
        """Remove variable from :py:attr:`variables` set
        and from :py:attr:`data` mapping.

        :param variable_name: Variable name.
        """
        # Remove variable
        del self.variable_component_names[variable_name]

        # Remove data for variable
        del self.var_data_sources[variable_name]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.var_data_sources)

    def __len__(self) -> int:
        """Number of variables.

        :returns: Number of variables.
        """
        return len(self.variable_component_names)

    def get_data_sources(
            self, variable_name: str) -> tp.MutableMapping[
                str, SingleDataSourceBase]:
        """Get single data source(s) containing variable.

        :param variable_name: Variable name.

        :returns: Data source(s) associated with variable.
        """
        data_sources = self.var_data_sources[variable_name]

        # Multiple single data sources for this variable
        data = {}
        for src_name, data_src in data_sources.items():
            data[src_name] = data_src

        return data

    def get_single_data_source(
            self, variable_name: str) -> SingleDataSourceBase:
        """Get single data source containing variable.

        :param variable_name: Variable name.

        :returns: Data source(s) associated with variable.

        :raises AssertionError: if data source for variable is not unique.
        """
        data_sources = self.var_data_sources[variable_name]

        assert len(data_sources) == 1, (
            'Data source for "{}" is not unique'.format(variable_name))

        return list(data_sources.values())[0]

    def get_from_all_sources(
            self, variable_name: str, default=None) -> e4tp.DatasetArrayType:
        """Get variable from data source containing variable.

        :param variable_name: Variable name.
        :param default: Default (mapping to) array(s).

        :returns: Mapping from source names to variable-data.

        .. seealso:: :py:meth:`get_data_sources`
        """
        # Data sources containing variable
        data_sources = self.get_data_sources(variable_name)

        # Multiple data sources for this variable
        data = OrderedDict()
        for src_name, data_src in data_sources.items():
            da = data_src[variable_name]
            data[src_name] = da

        return data

    def __str__(self) -> str:
        """Get dataset as string.

        :returns: String.
        """
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '\n'.join('{}\n{}'.format(str(data_src), str(data_src.data))
                       for data_src in self.data_sources.values())

        return s

    def read(self, variable_component_names: e4tp.VCNType = None,
             **kwargs) -> None:
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variable_component_names: Names of components per variable.
        """
        self.read_each_data_source(variable_component_names, **kwargs)

    def write(self, variable_names: e4tp.StrIterableType = None,
              **kwargs) -> None:
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variable_names: Variable(s) to write.
        """
        self.write_each_data_source(variable_names, **kwargs)

    def read_each_data_source(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> None:
        """Read multiple data source.

        :param variable_component_names: Names of components per variable.
        """
        vcn = self.get_vcn_safe(variable_component_names)
        for data_src_name in vcn:
            data_src = self.data_sources[data_src_name]
            data_src_vcn = data_src.variable_component_names
            data_src.read(
                variable_component_names=data_src_vcn, **kwargs)
            self.data[data_src_name] = data_src.data

    def write_each_data_source(
            self, variable_names: e4tp.StrIterableType = None,
            **kwargs) -> None:
        """Write multiple data source.

        :param variable_names: Variable(s) to write. If `None`,
          all variables are written.
        """
        for data_src in self.data_sources.values():
            data_src.write(variable_names=variable_names, **kwargs)

    def get_data_postfix(self, with_src_name: bool = False, **kwargs) -> str:
        """Get multiple data-source postfix as sum of each single
        data-source postfix.

        :param with_src_name: Whether to prefix postfix with source name.

        :returns: Postfix.
        """
        postfix = ''.join(data_src.get_data_postfix(
            with_src_name=with_src_name, **kwargs)
            for data_src in self.data_sources.values())

        return postfix


def _set_data_sources(multi_data_src: MultiDataSourceBase, data_sources:
                      e4tp.SingleDataSourcesType,
                      update_variables: bool = True) -> None:
    """Set data sources.

    :param multi_data_src: Multiple data source.
    :param data_sources: Data sources.
    :param update_variables: Whether to update variables from single
      data sources variables.
    """
    multi_data_src._data_sources = data_sources

    var_data_sources = {}
    for src_name, data_src in multi_data_src._data_sources.items():
        if update_variables:
            # Update variable names
            multi_data_src.update_variables(data_src.variable_component_names)

            # Update variable to data-source mapping
            for variable_name in data_src.variable_component_names:
                var_data_sources[variable_name] = {src_name: data_src}

        # Check if gridded
        if data_src.gridded:
            multi_data_src.gridded = True

    multi_data_src.var_data_sources = var_data_sources

    # Add data sources as children
    multi_data_src.update_children(multi_data_src.data_sources)
