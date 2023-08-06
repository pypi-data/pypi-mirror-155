"""Single-data source."""
from collections import OrderedDict
from orderedset import OrderedSet
import typing as tp
import e4clim
from e4clim.container.data_source import DataSourceBase
import e4clim.typing as e4tp
from e4clim.utils import tools


class SingleDataSourceBase(DataSourceBase):

    data: e4tp.DatasetMutableType

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str, task_names: e4tp.StrIterableType = OrderedSet(),
                 default_tasks_value: bool = True, **kwargs) -> None:
        """Initialize single data source.

        :param parent: Data-source context.
        :param name: Name.
        :param task_names: Names of potential tasks for container to perform.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none.

        .. warning:: At the moment, a variable can only belong to one data source.
        """
        # Initialize as data source
        super(SingleDataSourceBase, self).__init__(
            parent, name, task_names=task_names,
            default_tasks_value=default_tasks_value, **kwargs)

        self.data = OrderedDict()

    def get_data_sources(
            self, variable_name: str) -> tp.MutableMapping[
                str, 'SingleDataSourceBase']:
        """Get single data source(s) containing variable.

        :param variable_name: Variable name.

        :returns: Data source(s) associated with variable.
        """
        return {self.name: self}

    def get_single_data_source(
            self, variable_name: str) -> 'SingleDataSourceBase':
        """Get single data source containing variable.
        Useful when data source is multiple.

        :param variable_name: Variable name.

        :returns: Data source(s) associated with variable.
        """
        return self

    def update(self, ds=e4tp.DatasetType, /, **kwargs) -> None:
        """Update data with given dataset.

        :param ds: Dataset.

        .. warning:: Existing variables are replaced by new variables.
          May be problematic if the intension is to concatenate existing
          with new components.
        """
        for variable_name in ds.keys():
            if 'component' in ds[variable_name]:
                component_names = ds[variable_name][
                    'component'].values.tolist()
            else:
                component_names = [None]
            self.variable_component_names[variable_name] = OrderedSet()
            for component_name in tools.ensure_collection(
                    component_names, OrderedSet):
                self.variable_component_names[variable_name].add(
                    component_name)

        # Update dataset
        self.data.update(ds)

    def read(self, variable_component_names: e4tp.VCNType = None,
             **kwargs) -> None:
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variable_component_names: Names of components per variable.
        """
        self.read_variables(
            variable_component_names=variable_component_names, **kwargs)

    def write(self, variable_names: e4tp.StrIterableType = None,
              **kwargs) -> None:
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variable_names: Variable(s) to write.
        """
        self.write_variables(variable_names=variable_names, **kwargs)

    def __setitem__(self, variable_name: str,
                    data: e4tp.DataArrayType) -> None:
        """Set item in :py:attr:`data`.

        :param variable_name: Variable name.
        :param data: Data of variable to set.
        """
        self.data[variable_name] = data

    def get_data_postfix(self, **kwargs) -> str:
        """Get data-source postfix.
        A user-defined postfix may be defined in the `'postfix'`
        entry of the data source configuration.
        Otherwise, the standard postfix is used by calling
        :py:meth:`get_postfix`.
        The data-source name is prepended.

        :returns: Postfix.
        """
        # Get user-defined postfix or standard postfix
        postfix = tools.get_str_entry(
            self.cfg, 'postfix')
        if postfix is None:
            postfix = self.get_postfix(**kwargs)

        # Prepend data-source name
        with_src_name = kwargs.get('with_src_name')
        if with_src_name:
            postfix = '_{}{}'.format(self.name, postfix)

        return postfix

    def get_postfix(self, **kwargs) -> str:
        """Return empty postfix string.

        :returns: Postfix.
        """
        return ''
