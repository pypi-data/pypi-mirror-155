"""Data source with parsing methods."""
from abc import ABC, abstractmethod
from collections import OrderedDict
from orderedset import OrderedSet
import typing as tp
import e4clim.typing as e4tp
from e4clim.utils import tools
from .data_source import DataSourceBase


class ParsingDataSourceBase(DataSourceBase, ABC):

    def update_variables(
            self, variable_component_names: e4tp.VCNType,
            **kwargs) -> None:
        """Add variables to data source.

        :param variable_component_names: Names of components per variable.
        """
        # Update variables using super method
        super(ParsingDataSourceBase, self).update_variables(
            variable_component_names, **kwargs)

        # Update tasks
        variable_names = tools.ensure_collection(
            variable_component_names, OrderedSet)
        for variable_name in variable_names:
            task_name = 'download__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})
            task_name = 'parse__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})

    @abstractmethod
    def parse(self, variable_component_names: e4tp.VCNStrictType = None,
              **kwargs) -> tp.Union[
                  e4tp.DatasetType, e4tp.MultiDatasetType]:
        """Parse data from the input source and return dataset."""
        ...

    @abstractmethod
    def parse_finalize(self, variable_component_names:
                       e4tp.VCNStrictType = None, **kwargs) -> tp.Union[
            e4tp.DatasetType, e4tp.MultiDatasetType]:
        """Parse data from the input source and finalize dataset.

        :param variable_component_names: Names of components per variable.

        :returns: Dataset.
        """
        ...

    def _finalize_dataset(self, ds: e4tp.DatasetMutableType,
                          **kwargs) -> e4tp.DatasetMutableType:
        """Finalize arrays for all variables in mutable dataset.

        :param ds: Dataset.

        :returns: Finalized dataset.
        """
        for variable_name, da in ds.items():
            ds[variable_name] = self.finalize_array(
                da, variable_name, **kwargs)

        return ds

    def download(self, variable_component_names: e4tp.VCNStrictType = None,
                 **kwargs) -> tp.Optional[e4tp.VCNType]:
        """Download data."""
        self.warning('{} download not implemented'.format(self.name))

        return None

    @abstractmethod
    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> tp.Union[
                     e4tp.DatasetType, e4tp.MultiDatasetType]:
        """Read or parse data from a given source and store it in
        :py:attr:`data` member.

        :param variable_component_names: Names of components per variable.

        :returns: Dataset :py:attr:`data`.
        """
        ...

    def get_data_variables(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> e4tp.DatasetType:
        """Read or parse data from a given source and store it in
        :py:attr:`data` member.

        :param variable_component_names: Names of components per variable.
          If `None`, in all variables in :py:attr:`variable_component_names`
          are taken.

        :returns: Dataset :py:attr:`data`.
        """
        # Get list of variables to parse
        vcn_safe = self.get_vcn_safe(variable_component_names)
        vcn_to_do = self.get_vcn_to_do_safe(vcn_safe, 'parse')

        # Get list of variables to read
        vcn_to_read = self.get_vcn_to_read_safe(vcn_safe, vcn_to_do)

        if vcn_to_do:
            # Download data if needed
            self.manage_download(variable_component_names=vcn_to_do, **kwargs)
            svar = ', '.join(str(variable_name) for variable_name in vcn_to_do)
            self.info('Parsing {} {}'.format(self.name, svar))

            # Parse data
            data = self.parse_finalize(
                variable_component_names=vcn_to_do,
                **kwargs)
            for variable_name_data, ds in data.items():
                self[variable_name_data] = ds

            # Write data (all components, in case more than one)
            kwargs_write = kwargs.copy()
            kwargs_write['variable_names'] = vcn_to_do
            self.write(**kwargs_write)

            # Update task manager with all parsed variables
            # (even the ones that were not requested)
            for variable_name_data in data:
                self.task_mng['parse__{}'.format(variable_name_data)] = False

        if vcn_to_read:
            # Read variables
            svar = ', '.join(str(variable_name)
                             for variable_name in vcn_to_read)
            self.read(variable_component_names=vcn_to_read, **kwargs)

        self.get_data_callback(
            variable_component_names=vcn_safe, **kwargs)

        return self.data

    def get_data_callback(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> None:
        """Method called by :py:meth:`get_data` after data is parsed or read.
        Does nothing by default.

        :param variable_component_names: Names of components per variable.
        """
        return

    @abstractmethod
    def manage_download(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> None:
        """Manage data download.

        :param variable_component_names: Names of components per variable.
        """
        ...

    def get_vcn_to_do_safe(self, vcn: e4tp.VCNStrictMutableType,
                           action: str) -> e4tp.VCNStrictType:
        """Get variable-component names to do ensuring type.

        :param vcn: Variable-component names.
        :param action: Action to do.

        :returns: Type-checked variable-component names.
        """
        return OrderedDict([
            (variable_name, OrderedSet(component_names))
            for variable_name, component_names in vcn.items()
            if self.task_mng.get('{}__{}'.format(action, variable_name))])

    def get_vcn_to_read_safe(
            self, vcn: e4tp.VCNStrictMutableType,
            vcn_to_do: e4tp.VCNStrictType) -> e4tp.VCNStrictType:
        """Get variable-component names to read ensuring type.

        :param vcn: Variable-component names.
        :param vcn_to_do: Variable-component names to do.

        :returns: Type-checked variable-component names.
        """
        vcn_to_read = set(vcn) - set(vcn_to_do)

        return OrderedDict([
            (variable_name, set(vcn[variable_name]))
            for variable_name in vcn_to_read])

    @tp.no_type_check
    def finalize_array(self, da: e4tp.VT, variable_name: str,
                       **kwargs) -> e4tp.VT:
        """Finalize array adding/converting units if possible,
          transposing, naming. Used by APIs.

        :param da: Data array or dataset.
        :param variable_name: Variable name.
        """
        # Convert units if possible
        try:
            da = da * float(self.cfg['unit_conversions'][variable_name])
        except (KeyError, TypeError):
            pass

        if hasattr(da, 'attrs'):
            # Add units if possible
            try:
                da.attrs['units'] = str(self.cfg['units'][variable_name])
            except KeyError:
                da.attrs['units'] = 'Unknown'

        if hasattr(da, 'dims'):
            # Transpose
            dims = [d for d in ['time', 'component', 'region'] if d in da.dims]
            if len(dims) > 1:
                try:
                    da = da.transpose(*dims)
                except ValueError:
                    pass

        if hasattr(da, 'name'):
            # Name array as variable
            da.name = variable_name

        return da
