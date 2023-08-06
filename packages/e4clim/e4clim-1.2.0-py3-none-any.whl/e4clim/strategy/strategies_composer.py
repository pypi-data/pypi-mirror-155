"""Extractor composing multiple extractors.

  .. todo:: add_strategy moved somewhere in build
"""
from collections import OrderedDict
from e4clim.container.strategy import ExtractorBase
from e4clim.typing import DatasetType
from e4clim.utils import tools


class Strategy(ExtractorBase):

    def __init__(self, parent, name, cfg=None, **kwargs):
        """Naming constructor.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        :type parent: :py:class:`ContextResult`
        :type name: str
        :type cfg: mapping

        .. note:: Strategies to compose must be provided as a dictionary
          from the `extractors` entry of the configuration.
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

        # Initialize strategies from configuration
        self.strategies = OrderedDict()
        for strategy_name in self.cfg['extractors']:
            # Get strategy
            strategy = add_strategy(
                self.parent, strategy_name=strategy_name,
                cfg=self.cfg['extractors'], **kwargs)

            # Reference strategy in strategies set
            self.strategies[strategy_name] = strategy

        #: Functions composed to define :py:meth:`transform` method.
        self._functions = None

        # Add transform of each strategies in the right order
        self._functions = [self.strategies[strategy_name].transform
                           for strategy_name in self.cfg['extractors']]

        # Define :py:meth:`transform` method by composing functions
        self.transform = tools.Composer(*self._functions)

        # Add data sources
        for strategy in self.strategies.values():
            if 'data' in strategy.cfg:
                if self.data_sources is None:
                    self.data_sources = OrderedDict()
                self.build_data_sources(cfg=strategy.cfg, **kwargs)

    def transform(self, **kwargs) -> DatasetType:
        """Empty concrete definition of transform method replaced
        by composed functions during construction."""
        pass

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        # Get default postfix
        postfix0 = super(Strategy, self).get_extractor_postfix(**kwargs)

        # Add postfixes of every strategy
        return ''.join([postfix0] + [
            self.strategies[strategy_name].get_extractor_postfix(**kwargs)
            for strategy_name in self.cfg['extractors']])
