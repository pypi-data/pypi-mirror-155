"""Data-source base definitions."""
from abc import ABC, abstractmethod
from collections import OrderedDict
from orderedset import OrderedSet
import pandas as pd
from pathlib import Path
import typing as tp
import xarray as xr
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools
from .base import ContainerBase


class DataSourceBase(ContainerBase, tp.MutableMapping, ABC):
    """Base data-source class for APIs."""

    #: Data-source data.
    data: tp.Union[e4tp.DatasetMutableType, e4tp.MultiDatasetMutableType]

    #: Whether this is a gridded data source.
    gridded: bool

    #: Data-source variable names.
    variable_component_names: e4tp.VCNStrictMutableType

    def __init__(
            self, parent: 'e4clim.context.base.ContextBase',
            name: str, cfg: e4tp.CfgType = None,
            variable_component_names: e4tp.VCNType = None,
            task_names: e4tp.StrIterableType = None, **kwargs) -> None:
        """Build data source linked to mediator.

        :param parent: Data-sources context.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :param variable_component_names: Names of components per variable.
        :param task_names: Names of potential tasks for container to perform.
        :param parent: Parent container.
        """
        # Add read tasks per variable
        if variable_component_names is not None:
            variable_names = tools.ensure_collection(variable_component_names,
                                                     OrderedSet)
            if task_names is None:
                task_names_safe = OrderedSet()
            else:
                task_names_safe = tools.ensure_collection(
                    task_names, OrderedSet)

            if variable_names is not None:
                for variable_name in variable_names:
                    task_names_safe.add('read__{}'.format(variable_name))
                    task_names_safe.add('write__{}'.format(variable_name))
        else:
            task_names_safe = None

        # Initialize as container
        super(DataSourceBase, self).__init__(
            name, cfg=cfg, task_names=task_names_safe, parent=parent, **kwargs)

        self.gridded = False

        self.variable_component_names = OrderedDict()

        # Add set of variable names composing dataset
        if variable_component_names is not None:
            self.update_variables(variable_component_names)

    def get_vcn_safe(self, vcn:
                     e4tp.VCNType = None) -> e4tp.VCNStrictMutableType:
        """Get safe variable-component names.

        :param vcn: Variable-component names to check.

        :returns: Type-safe variable-component names.
        """
        if vcn is None:
            return self.variable_component_names
        else:
            variable_names = tools.ensure_collection(vcn, OrderedSet)
            vcn_safe = OrderedDict()
            for variable_name in variable_names:
                if isinstance(vcn, tp.Mapping):
                    component_names = tools.ensure_collection(
                        vcn[variable_name], OrderedSet) or OrderedSet()
                else:
                    component_names = OrderedSet()
                vcn_safe[variable_name] = component_names

            return vcn_safe

    def update_variables(self, variable_component_names: e4tp.VCNType,
                         **kwargs) -> None:
        """Add variable names to data source.

        :param variable_component_names: Names of components per variable.
        """
        # Update variables
        variable_names = tools.ensure_collection(
            variable_component_names, OrderedSet)
        if isinstance(variable_component_names, tp.Mapping):
            for variable_name, component_names in (
                    variable_component_names.items()):
                if variable_name not in self.variable_component_names:
                    self.variable_component_names[
                        variable_name] = OrderedSet()
                vcn_vn = self.variable_component_names[variable_name]
                component_names_safe = tools.ensure_collection(
                    component_names, OrderedSet)
                if component_names_safe is not None:
                    for component_name in component_names_safe:
                        vcn_vn.add(component_name)
        else:
            for variable_name in variable_names:
                if variable_name not in self.variable_component_names:
                    self.variable_component_names[
                        variable_name] = OrderedSet()

        # Update tasks
        for variable_name in variable_names:
            task_name = 'read__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})
            task_name = 'write__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})

    @abstractmethod
    def read(self, **kwargs) -> None:
        """Read data source."""
        ...

    @abstractmethod
    def write(self, **kwargs) -> None:
        """Write data source."""
        ...

    def read_variables(self, variable_component_names: e4tp.VCNType = None,
                       **kwargs) -> None:
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variable_component_names: Names of components per variable.
        """
        if variable_component_names:
            # Update data source set of variables
            self.update_variables(variable_component_names)

            # Read each variable separately
            ds = {}
            variable_names = tools.ensure_collection(
                variable_component_names, OrderedSet)
            for variable_name in variable_names:
                if self.task_mng['read__{}'.format(variable_name)]:
                    ds[variable_name] = self._read_data(
                        variable_name, **kwargs)

                    # Update task manager
                    self.task_mng['read__{}'.format(variable_name)] = False

            # Update dataset
            self.data.update(ds)
        else:
            self.warning('Empty variable-name collection given: no {} '
                         'data read'.format(self.name))

    def write_variables(self, variable_names: e4tp.StrIterableType = None,
                        **kwargs) -> None:
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variable_names: Variable(s) to write. If `None`,
          all variables are written.

        .. warning:: Exististing files are not overwritten.
          Only existing variables (groups) are.
        """
        if variable_names is None:
            variable_names = self.variable_component_names
        else:
            variable_names = tools.ensure_collection(
                variable_names, OrderedSet)

        if variable_names:
            for variable_name in variable_names:
                if self.task_mng.get('write__{}'.format(variable_name)):
                    # Select data
                    data = self.data.get(variable_name)

                    # Write data
                    self._write_data(data, variable_name, **kwargs)

                    # Update task manager
                    self.task_mng['write__{}'.format(variable_name)] = False
        else:
            self.warning('Empty variable-name collection given: no {} '
                         'data written'.format(self.name))

    def _read_data(self, variable_name: str,
                   **kwargs) -> e4tp.FrameArrayType:
        """Write data for variable.

        :param variable_name: Variable name for the data (used to
          for message raised by exception, if needed).

        :returns: Data read.
        """
        filepath = Path(self.get_data_path(
            variable_name=variable_name, makedirs=False, **kwargs))

        if filepath.suffix == '.nc':
            data = self._read_netcdf(filepath, variable_name, **kwargs)
        elif filepath.suffix == '.csv':
            data = self._read_csv(filepath, variable_name, **kwargs)
        else:
            try:
                filepath = filepath.with_suffix('.nc')
                data = self._read_netcdf(filepath, variable_name, **kwargs)
            except FileNotFoundError:
                try:
                    filepath = filepath.with_suffix('.csv')
                    data = self._read_csv(filepath, variable_name, **kwargs)
                except FileNotFoundError:
                    try:
                        # Try as multiple data source
                        self[variable_name].read(
                            self[variable_name].variable_component_names,
                            **kwargs)  # type: ignore
                        data = self[variable_name].data
                    except (KeyError, FileNotFoundError):
                        raise FileNotFoundError(
                            'No such file or directory: "{}", and {} not a '
                            'multiple data source containing {}'.format(
                                filepath, self.name, variable_name))

        return data

    def _read_netcdf(self, filepath: e4tp.PathType, variable_name: str,
                     **kwargs) -> e4tp.DataArrayType:
        """Read NetCDF file.

        :param filepath: Filepath.
        :param variable_name: Variable name.

        :returns: Data read.
        """
        self.info('Reading {} {} from {}'.format(
            self.name, variable_name, filepath))

        try:
            # Try to load as dataarray
            data = xr.load_dataarray(filepath)
        except ValueError:
            # Or else load as dataset
            data = xr.load_dataset(filepath)

        return data

    def _read_csv(self, filepath: e4tp.PathType, variable_name: str,
                  **kwargs) -> pd.core.generic.NDFrame:
        """Read CSV file.

        :param filepath: Filepath.
        :param variable_name: Variable name.

        :returns: Data read.
        """
        self.info('Reading {} {} from {}'.format(
            self.name, variable_name, filepath))

        read_csv_kwargs_safe = self._get_csv_kwargs(variable_name, 'read')

        # Read CSV
        data = pd.read_csv(filepath, **read_csv_kwargs_safe).squeeze(
            'columns')

        return data

    def _write_data(self, data: e4tp.FrameArrayType, variable_name: str,
                    **kwargs) -> None:
        """Write data for variable.

        :param data: Data to write.
        :param variable_name: Variable name for the data (used to
          for message raised by exception, if needed).
        """
        suffix = _get_suffix_from_data(data, **kwargs)

        if suffix is None:
            # Try as multiple data source
            try:
                self[variable_name].write(**kwargs)  # type: ignore
                return
            except (AttributeError, KeyError):
                pass

            # Try to handle unknown data type
            data, suffix = self._try_handle_unknown_datatype(
                data, variable_name, **kwargs)

        # Get file path
        filepath = Path(self.get_data_path(
            variable_name=variable_name, **kwargs)).with_suffix(suffix)
        self.info('Writing {} {} to {}'.format(
            self.name, variable_name, filepath))

        if suffix == '.nc':
            self._write_netcdf(data, filepath)
        elif suffix == '.csv':
            self._write_csv(data, variable_name, filepath, **kwargs)

    def _write_netcdf(self, data: xr.core.common.DataWithCoords,
                      filepath: e4tp.PathType) -> None:
        """Write as NetCDF.

        :param data: Data to write.
        :param filepath: Path of file to write to.

        .. warning:: To avoid `NotImplementedError` multi-indices are
          reset.
        """
        # Ensure that there are no multi-indices
        for index_name, index in data.indexes.items():
            if hasattr(index, 'levels'):
                data = data.reset_index(index_name)

        data.to_netcdf(filepath, mode='w')

    def _write_csv(self, data: pd.core.generic.NDFrame,
                   variable_name: str, filepath: e4tp.PathType, **kwargs) -> None:
        """Write to CSV.

        :param data: Data to write.
        :param variable_name: Variable name for the data (used to
            for message raised by exception, if needed).
        :param filepath: Path of file to write to.
        """
        write_csv_kwargs_safe = self._get_csv_kwargs(variable_name, 'write')

        # Write to CSV
        data.to_csv(filepath, **write_csv_kwargs_safe)

    def _get_csv_kwargs(self, variable_name: str,
                        action: str) -> tp.Dict[str, tp.Any]:
        """Get keyword arguments to read or write CSV for variable.

        :param variable_name: Variable name.
        :param action: `"read"` or `"write"`.

        :returns: Keyword arguments.
        """
        # Get variable-independent keyword arguments
        csv_kwargs: tp.Dict[str, tp.Any] = dict(tools.get_required_mapping_entry(
            self.cfg, '{}_csv_kwargs'.format(action), {}))

        # Add variable-dependent keyword arguments
        variable_csv_kwargs = tools.get_mapping_entry(
            self.cfg, 'variable_{}_csv_kwargs'.format(action), {})
        if variable_csv_kwargs:
            other_variable_csv_kwargs = tools.get_required_mapping_entry(
                variable_csv_kwargs, variable_name, {})
            csv_kwargs.update(
                other_variable_csv_kwargs)

        return csv_kwargs

    def _try_handle_unknown_datatype(
            self, data: e4tp.FrameArrayType, variable_name: str,
            **kwargs) -> tp.Tuple[e4tp.FrameArrayType, str]:
        """Get format of file corresponding to data type.

        :param data: Data to write.
        :param variable_name: Variable name for the data (used to
            for message raised by exception, if needed).

        :returns: Suffix.
        :rtype: str
        """
        try:
            # Try to make a series
            data = pd.Series(data)
            suffix = '.csv'
        except TypeError:
            msg = ("{} {} not pandas nor xarray data and cannot be "
                   "converted to pandas.Series. Can't write.".format(
                       self.name, variable_name))
            raise TypeError(msg)

        return data, suffix

    def __getitem__(self, variable_name: str) -> tp.Union[
            e4tp.DataArrayType, e4tp.DatasetType]:
        """Get variable data from :py:attr:`data`.

        :param variable_name: Variable name.

        :returns: Variable.
        """
        return self.data[variable_name]

    def get(self, variable_name: str, default=None) -> tp.Union[
            tp.Optional[e4tp.DataArrayType],
            tp.Optional[e4tp.DatasetType]]:
        """Get variable data from :py:attr`data`.

        :param variable_name: Variable name.
        :param default: Default value.

        :returns: Variable.
        """
        return self.data.get(variable_name, default)

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
        del self.data[variable_name]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.data)

    def __len__(self) -> int:
        """Number of variables.

        :returns: Number of variables.
        """
        return len(self.variable_component_names)

    def __str__(self) -> str:
        """Get dataset as string.

        :returns: String.
        """
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '{}'.format(self.data)

        return s

    def get_data_path(self, variable_name: str = None,
                      makedirs: bool = True, **kwargs) -> Path:
        """Get data-source filepath.

        :param variable_name: Data variable.
        :param makedirs: Make directories if needed.

        :returns: Filepath.
        """
        # Variable string
        var_pf = '_{}'.format(variable_name) if variable_name else ''

        # Data-postfix string
        data_pf = self.get_data_postfix(
            variable_name=variable_name, **kwargs)

        # Filepath
        filename = '{}{}{}'.format(self.name, var_pf, data_pf)
        data_dir = self.get_data_directory(makedirs=makedirs, **kwargs)
        filepath = Path(data_dir, filename)

        return filepath

    @abstractmethod
    def get_data_postfix(self, **kwargs) -> str: ...


def _get_suffix_from_data(data: e4tp.FrameArrayType,
                          **kwargs) -> tp.Optional[str]:
    """Get suffix of file corresponding to data type.

    :param data: Data to write.

    :returns: Suffix.
    """
    if isinstance(data, pd.core.generic.NDFrame):
        return '.csv'
    elif isinstance(data, xr.core.common.DataWithCoords):
        return '.nc'
    else:
        return None
