"""Optimizer data sources for multiple cases."""
from abc import ABC
from collections import OrderedDict
from orderedset import OrderedSet
from pathlib import Path
import typing as tp
import e4clim
import e4clim.typing as e4tp
from e4clim.utils import tools
from .optimizer_data_source import (
    OptimizerDataSourceBase, OptimizerSingleDataSourceBase,
    OptimizerInputBase, OptimizerSolutionBase)
from .parsing_multi_data_source import ParsingMultiDataSourceBase


class OptimizerMultiDataSourceBase(
        OptimizerDataSourceBase, ParsingMultiDataSourceBase, ABC):
    """Multiple-case input or solution."""

    #: Data Sources.
    data_sources: tp.MutableMapping[str, OptimizerSingleDataSourceBase]

    #: Parent.
    parent: ('e4clim.context.context_multi_optimizer.'
             'ContextMultiOptimizerDecorator')

    def __init__(
            self, parent:
            'e4clim.context.context_multi_optimizer.'
            'ContextMultiOptimizerDecorator',
            type_name: str, name: str = None, **kwargs) -> None:
        """Initialize multiple-case input or solution.

        :param parent: Optimizer context.
        :param type_name: Data-source type name. Either `'input'`
          or `'solution'`.
        :param name. Name.

        raises AssertionError: if `'optimizer'` attribute of
          :py:obj:`parent` argument is `None`.
        """
        assert parent.optimizer is not None, (
            '"optimizer" attribute of "parent" argument required')

        self.optimizer = parent.optimizer
        self._type_name = type_name

        name = ('{}_multi_{}'.format(self.optimizer.name, self._type_name)
                if name is None else name)

        cfg = (parent.cfg if self._type_name == 'solution'
               else parent.cfg.get(self._type_name))

        super(OptimizerMultiDataSourceBase, self).__init__(
            parent=parent, type_name=type_name, name=name, cfg=cfg, **kwargs)

        # Update case names
        self.update_variables(list(self.parent.cases))

    def __setitem__(self, case_name: str, data: e4tp.DatasetType) -> None:
        """Set items in data sources containing variable.

        :param case_name: Case name.
        :param data: Data of case to set.
        """
        self.data[case_name] = data  # type: ignore
        for variable_name, da in data.items():
            self.data_sources[case_name].data[variable_name] = da

    def get_data(
            self, variable_component_names: e4tp.VCNType = None,
            **kwargs) -> e4tp.MultiDatasetMutableType:
        """Get optimizer multiple data.

        :param variable_component_names: Case names.

        :returns: Dataset.
        """
        data = self.get_data_variables(
            variable_component_names=variable_component_names, **kwargs)

        # Add data to single data sources
        for case_name, ds in data.items():
            self[case_name].data = ds  # type: ignore

        return data

    def parse_finalize(self, variable_component_names:
                       e4tp.VCNStrictType = None, **kwargs) -> e4tp.MultiDatasetType:
        """Parse solution.

        :param variable_component_names: Case names.

        :returns: Result from optimization solver.
        """
        return self.parse(
            variable_component_names=variable_component_names,
            **kwargs)

    def read(self, variable_component_names: e4tp.VCNType = None,
             **kwargs) -> None:
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variable_component_names: Names of components per variable.
        """
        self.read_variables(variable_component_names, **kwargs)

    def write(self, variable_names: e4tp.StrIterableType = None,
              **kwargs) -> None:
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variable_names: Variable(s) to write.
        """
        self.write_variables(variable_names, **kwargs)

    def get_data_postfix(self, with_src_name: bool = False,
                         variable_name: str = None, **kwargs) -> str:
        """Get data postfix for case.

        :param variable_name: Case name.

        :returns: Postfix.
        """
        assert variable_name is not None, (
            '"variable_name" keyword argument required')

        self.parent._prepare_for_case(variable_name)

        return self.data_sources[variable_name].get_data_postfix(**kwargs)

    def get_data_directory(self, makedirs: bool = True, **kwargs) -> Path:
        """Get path to data directory.

        :param makedirs: Make directories if needed.

        :returns: Data directory path.
        """
        return self.med.cfg.get_project_data_directory(
            self.parent._optimizer,
            subdirs=self._type_name, makedirs=makedirs)


class OptimizerMultiInput(OptimizerMultiDataSourceBase):
    """Multiple-case input."""

    #: Data Sources.
    data_sources: tp.MutableMapping[str, OptimizerInputBase]  # type: ignore

    def __init__(
            self, parent:
            'e4clim.context.context_multi_optimizer.'
            'ContextMultiOptimizerDecorator', **kwargs) -> None:
        """Initialize multiple-case input.

        :param parent: Optimizer context.
        """
        super(OptimizerMultiInput, self).__init__(
            parent, 'input', **kwargs)

    def __getitem__(self, case_name: str) -> OptimizerInputBase:
        """Get case input data source.

        :param case_name: Case name.

        :returns: Data source.
        """
        return self.data_sources[case_name]

    def get(self, case_name: str, default=None) -> tp.Optional[
            OptimizerInputBase]:
        """Get case input data source.

        :param case_name: Case name.

        :returns: Data source.
        """
        return self.data_sources.get(case_name, default)

    def parse(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> e4tp.MultiDatasetType:
        """Parse solution.

        :param variable_component_names: Case names.

        :returns: Input dataset.
        """
        cases = (self.parent.cases
                 if variable_component_names is None else
                 tools.ensure_collection(variable_component_names, OrderedSet))

        ds = OrderedDict()
        for case_name in cases:
            self.parent._prepare_configuration_for_case(case_name)
            self.parent._prepare_input_for_case(case_name)
            ds[case_name] = self.optimizer.input.parse(**kwargs)

        return ds

    # def read(self, variable_component_names: e4tp.VCNType = None,
    #          **kwargs) -> None:
    #     """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

    #     :param variable_component_names: Names of components per variable.
    #     """
    #     self.read_each_data_source(
    #         variable_component_names=variable_component_names, **kwargs)

    # def write(self, variable_names: e4tp.StrIterableType = None,
    #           **kwargs) -> None:
    #     """Write :py:class:`xarray.DataArray` of each variable in netcdf.

    #     :param variable_names: Variable(s) to write.
    #     """
    #     self.write_each_data_source(**kwargs)


class OptimizerMultiSolution(OptimizerMultiDataSourceBase):
    """Multiple-case solution."""

    #: Data Sources.
    data_sources: tp.MutableMapping[str, OptimizerSolutionBase]  # type: ignore

    #: Associated input.
    _input: OptimizerMultiInput

    def __init__(
            self, parent:
            'e4clim.context.context_multi_optimizer.'
            'ContextMultiOptimizerDecorator', **kwargs) -> None:
        """Initialize multiple-case solution.

        :param parent: Optimizer context.
        """
        super(OptimizerMultiSolution, self).__init__(
            parent, 'solution', **kwargs)

    @property
    def input(self) -> OptimizerMultiInput:
        return self._input

    def __getitem__(self, case_name: str) -> OptimizerSolutionBase:
        """Get case solution data source.

        :param case_name: Case name.

        :returns: Data source.
        """
        return self.data_sources[case_name]

    def get(self, case_name: str, default=None) -> tp.Optional[
            OptimizerSolutionBase]:
        """Get case solution data source.

        :param case_name: Case name.

        :returns: Data source.
        """
        return self.data_sources.get(case_name, default)

    def parse(
            self, variable_component_names: e4tp.VCNStrictType = None,
            **kwargs) -> e4tp.MultiDatasetType:
        """Parse solution.

        :param variable_component_names: Case names.

        :returns: Result from optimization solver.
        """
        self.parent.input.get_data(
            variable_component_names=variable_component_names, **kwargs)

        return self.parent.solve(
            case_names=variable_component_names, **kwargs)
