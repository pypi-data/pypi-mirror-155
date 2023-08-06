"""Modifier to resample."""
from typing import cast, Hashable, Mapping
from e4clim.container.strategy import ExtractorBase
from e4clim.typing import DatasetType, StrToDataArrayType


class Strategy(ExtractorBase):

    def __init__(self, parent, name, cfg=None, **kwargs):
        """Naming constructor.

        :param parent: Parent.
        :param name: Strategy name.
        :param cfg: Strategy configuration.
        :type parent: :py:class:`ContextResult`
        :type name: str
        :type cfg: mapping
        """
        super(Strategy, self).__init__(parent=parent, name=name, cfg=cfg,
                                       **kwargs)

    def transform(self, ds: StrToDataArrayType = None,
                  **kwargs) -> DatasetType:
        """Apply modifier to data source.

        :param ds: Dataset to transform.

        :returns: Modified dataset.
        """
        assert ds is not None, '"ds" argument should be given here'

        indexer = cast(Mapping[Hashable, str], self.cfg['indexer'])
        coord = list(indexer)[0]

        ds_new = ds.copy()
        for da_name, da in ds.items():
            # Resample array
            gp = da.resample(indexer)

            # Apply reduction
            ds_new[da_name] = getattr(gp, str(self.cfg['apply']))(coord)

        return ds_new

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '_{}{}{}'.format(
            *list(self.cfg['indexer'].items())[0], self.cfg['apply'])

        return '{}{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs), postfix)
