"""Parsing methods for single data source."""
from abc import ABC, abstractmethod
from orderedset import OrderedSet
import xarray as xr
import e4clim.context
import e4clim.typing as e4tp
from e4clim.utils import tools
from .parsing_data_source import ParsingDataSourceBase
from .single_data_source import SingleDataSourceBase


class ParsingSingleDataSourceBase(
        ParsingDataSourceBase, SingleDataSourceBase, ABC):

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str, cfg: e4tp.CfgType = None,
                 variable_component_names: e4tp.VCNType = None,
                 task_names=None, **kwargs):
        """Build data source with downloading and parsing capabilities.

        :param parent: Data-sources context.
        :param name: Data-source name.
        :param med: Mediator.
        :param cfg: Data-source configuration.
        :param variable_component_names: Names of components per variable.
        :param parent: Parent container.
        :param task_names: Names of potential tasks for container to perform.
        """
        # Add download and parse tasks per variable
        if variable_component_names is not None:
            variable_names = tools.ensure_collection(
                variable_component_names, OrderedSet)
            if task_names is None:
                task_names = OrderedSet()
            for variable_name in variable_names:
                task_names.add('parse__{}'.format(variable_name))
                task_names.add('download__{}'.format(variable_name))

        super(ParsingSingleDataSourceBase, self).__init__(
            parent, name, cfg=cfg,
            variable_component_names=variable_component_names,
            task_names=task_names, **kwargs)

    @abstractmethod
    def parse(self, variable_component_names: e4tp.VCNType = None,
              **kwargs) -> e4tp.DatasetType:
        """Parse data from the input source and return dataset."""
        ...

    def parse_finalize(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> e4tp.DatasetType:
        """Parse data from the input source and finalize dataset.

        :param variable_component_names: Names of components per variable.

        :returns: Dataset.

        .. seealso:: :py:meth:`finalize_array`
        """
        # Call function to get dataset
        ds_im = self.parse(
            variable_component_names=variable_component_names, **kwargs)

        # Make mutable
        if isinstance(ds_im, xr.Dataset):
            return self._finalize_dataset(ds_im, **kwargs)
        else:
            return self._finalize_dataset(dict(ds_im), **kwargs)

    def get_data(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.DatasetType:
        """Read or parse data from a given source and store it in
        :py:attr:`data` member.

        :param variable_component_names: Names of components per variable.
          If `None`, in all variables in :py:attr:`variable_component_names`
          are taken.

        :returns: Dataset :py:attr:`data`.
        """
        return self.get_data_variables(
            variable_component_names=variable_component_names, **kwargs)

    def manage_download(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> None:
        """Manage data download.

        :param variable_component_names: Names of components per variable.
          If `None`, all variables in :py:attr:`variable_component_names`
          are downloaded.
        """
        # Get list of variables to download
        variable_component_names_safe = self.get_vcn_safe(
            variable_component_names)
        variable_component_to_do_names = self.get_vcn_to_do_safe(
            variable_component_names_safe, 'download')

        # Download variables
        if variable_component_to_do_names:
            svar = ', '.join(
                str(variable_name) for variable_name in
                variable_component_to_do_names)
            self.info('Downloading {} {}'.format(
                ', '.join(self.name.split('__')), svar))

            # Download
            downloaded_variable_component_names = self.download(
                variable_component_names=variable_component_to_do_names,
                **kwargs)

            # Update task manager with all downloaded variables
            # (even the ones that were not requested)
            if downloaded_variable_component_names is not None:
                for variable_name in downloaded_variable_component_names:
                    self.task_mng['download__{}'.format(
                        variable_name)] = False
