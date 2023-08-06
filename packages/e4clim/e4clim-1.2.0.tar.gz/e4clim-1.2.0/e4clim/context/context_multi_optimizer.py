"""Optimization definitions to handle multiple cases."""
from collections import OrderedDict
from copy import deepcopy
from itertools import product
from orderedset import OrderedSet
import typing as tp
from e4clim.container.multi_data_source import _set_data_sources
from e4clim.container.optimizer_multi_data_source import (
    OptimizerMultiInput, OptimizerMultiSolution)
from e4clim.context.context_optimizer import (
    ContextSingleOptimizer, ContextOptimizerDecoratorBase)
import e4clim.typing as e4tp
from e4clim.utils import tools


class ContextMultiOptimizerDecorator(ContextOptimizerDecoratorBase):

    #: Cases to solve.
    cases: tp.MutableMapping[str, tp.Tuple]

    #: Case keys.
    case_keys: tp.List[tp.List[str]]

    _context_optimizer: ContextSingleOptimizer

    _input: tp.Optional[OptimizerMultiInput]
    _solution: tp.Optional[OptimizerMultiSolution]

    def __init__(self, context_optimizer: ContextSingleOptimizer,
                 name: str = 'context_multi_optimizer',
                 **kwargs) -> None:
        """Initialize multiple case optimizer decorator.

        :param context_optimizer: Optimizer context.
        :param name: Optimizer context name.
        """
        super(ContextMultiOptimizerDecorator, self).__init__(
            context_optimizer, name=name, **kwargs)

        #: Cases to solve.
        self.cases = OrderedDict()

        #: Case keys.
        self.case_keys = self.cfg.pop('cases')

        add_cases(self.case_keys, self.cfg, self.cases)

    @property
    def input(self) -> OptimizerMultiInput:
        """Input property.

        :returns: Input.

        :raises AssertionError: if :py:attr:`_input` is `None`.
        """
        assert self._input is not None, '"_input" attribute not set'

        return self._input

    @property
    def solution(self) -> OptimizerMultiSolution:
        """Solution property.

        :returns: Solution.

        :raises AssertionError: if :py:attr:`_solution` is `None`.
        """
        assert self._solution is not None, '"_solution" attribute not set'

        return self._solution

    def get_new_input(self, **kwargs) -> OptimizerMultiInput:
        """Get new multiple-cases input from optimizer and add
        single data sources.

        :returns: Multiple-cases input.
        """
        # Build multiple-cases input
        multi_data_src = OptimizerMultiInput(self)

        # Get single inputs
        data_sources = {}
        for case_name in self.cases:
            self._prepare_configuration_for_case(case_name)
            data_src = self._context_optimizer.get_new_input(**kwargs)
            data_src.name = '{}_{}'.format(data_src.name, case_name)
            data_sources[case_name] = data_src

        # Add single inputs to multiple-cases input data sources
        _set_data_sources(multi_data_src, data_sources, update_variables=False)

        return multi_data_src

    def get_new_solution(self, **kwargs) -> OptimizerMultiSolution:
        """Get new multiple-cases solution from optimizer and add
        single data sources.

        :returns: Multiple-cases solution.

        :raises AssertionError: if :py:attr:`_input` is `None`.
        """
        assert self._input is not None, '"_input" attribute not set'

        # Build multiple-cases solution
        multi_data_src = OptimizerMultiSolution(self)

        # Associate input to solution
        multi_data_src._input = self._input

        # Get single solutions
        data_sources = {}
        for case_name in self.cases:
            self._prepare_configuration_for_case(case_name)
            self._prepare_input_for_case(case_name)
            data_sources[
                case_name] = self._context_optimizer.get_new_solution(**kwargs)

        # Add single inputs to multiple-cases input data sources
        _set_data_sources(multi_data_src, data_sources, update_variables=False)

        return multi_data_src

    def solve(
            self, case_names: tp.Collection = None,
            **kwargs) -> e4tp.MultiDatasetType:
        """Solve optimization problem for all cases.

        :param case_names: Case names.
          in which case all cases are solved.

        :returns: Solution dataset.
        """
        case_names = (self.cases if case_names is None else
                      tools.ensure_collection(case_names, OrderedSet))

        ds_cases = OrderedDict()
        for case_name in case_names:
            self.info('Optimizing case {}:'.format(case_name))

            self._prepare_for_case(case_name)

            ds = self._context_optimizer.solve(**kwargs)

            ds_cases[case_name] = ds

        return ds_cases

    def _prepare_for_case(self, case_name: str) -> None:
        """Prepare optimizer for case.

        :param case_name: Case name.
        """
        self._prepare_configuration_for_case(case_name)
        self._prepare_input_for_case(case_name)
        self._prepare_solution_for_case(case_name)

    def _prepare_configuration_for_case(self, case_name: str) -> None:
        """Prepare optimizer configuration for case.

        :param case_name: Case name.

        :raises AssertionError: if configurations for case are not a
          mapping.
        """
        self._context_optimizer._cfg = deepcopy(self.cfg)
        if self._context_optimizer._optimizer is not None:
            self._context_optimizer._optimizer._cfg = (
                self._context_optimizer._cfg)
        for k, keys_orig in enumerate(self.case_keys):
            # Manage keys tree
            keys_orig = tools.ensure_collection(keys_orig, list)
            keys = keys_orig.copy()

            assert isinstance(self._context_optimizer.cfg._cfg, tp.Mapping), (
                'Optimizer configuration is not a mapping')

            cfg_entry: tp.MutableMapping[
                str, tp.Any] = self._context_optimizer.cfg._cfg
            while len(keys) > 1:
                key = keys.pop(0)
                new_cfg_entry = cfg_entry[key]

                assert isinstance(new_cfg_entry, tp.MutableMapping), (
                    'Optimizer-configuration entry at {} for {} case '
                    'is not a mutable mapping.'.format(key, case_name))

                cfg_entry = new_cfg_entry

            # Set value of each case key
            cfg_entry[keys[0]] = self.cases[case_name][k]

    def _prepare_input_for_case(self, case_name: str) -> None:
        """Prepare optimizer input for case.

        :param case_name: Case name.
        """
        # Set optimizer-context input to case input
        self._context_optimizer._input = self.input[case_name]

        # Update configuration to makes sure it takes potential
        # modifications of the parent configuration into account
        self._context_optimizer._input.cfg._cfg = (
            self._context_optimizer.cfg['input'])

    def _prepare_solution_for_case(self, case_name: str) -> None:
        """Prepare optimizer solution for case.

        :param case_name: Case name.
        """
        # Set optimizer-context solution to case solution
        self._context_optimizer._solution = self.solution[case_name]

        # Update configuration to makes sure it takes potential
        # modifications of the parent configuration into account
        self._context_optimizer._solution._cfg = self._context_optimizer.cfg

    def build_optimizer(self, **kwargs) -> None:
        """Build optimizer via child optimizer context.."""
        # Prepare for any case so that optimizer can get inputs/solutions
        case_name = list(self.cases)[0]
        self._prepare_configuration_for_case(case_name)

        super(ContextMultiOptimizerDecorator, self).build_optimizer(**kwargs)


def add_cases(case_keys: tp.List[tp.List[str]], cfg: e4tp.CfgMappingType,
              cases: tp.MutableMapping[str, tp.Tuple]) -> None:
    """Add cases to solution variables.

    :param case_keys: Case keys.
    :param cfg: Optimizer configuration.
    :param cases: Cases configuration to make.

    :raises AssertionError: if configurations for case are not a mapping.
    """
    cases_values = []
    prop_names = []
    for keys_orig in case_keys:
        keys_orig_safe = tools.ensure_collection(keys_orig, list)
        keys = keys_orig_safe.copy()
        prop_names.append(keys[-1])

        assert isinstance(cfg, tp.Mapping), 'Configuration is not a mapping'

        cfg_entry: tp.Mapping[str, tp.Any] = cfg

        while len(keys) > 0:
            key = keys.pop(0)
            new_cfg_entry = cfg_entry[key]

            if len(keys) > 0:
                assert isinstance(new_cfg_entry, tp.Mapping), (
                    'Optimizer-configuration entry at {} '
                    'is not a mutable mapping.'.format(key))

                cfg_entry = new_cfg_entry
            else:
                values = new_cfg_entry

        cases_values.append(tools.ensure_collection(values, list))

    # Product of cases
    cases_prod = product(*cases_values)
    for values in cases_prod:
        case_name = ''.join([n + str(v).replace('.', 'p')
                             for (n, v) in zip(prop_names, values)])
        cases[case_name] = values
