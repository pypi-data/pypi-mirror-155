"""Modifier to regrid."""
import xarray as xr
from e4clim.container.strategy import ExtractorBase


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

    def transform(self, ds: xr.Dataset = None, **kwargs) -> xr.Dataset:
        """Apply modifier to data source.

        :param ds: Dataset to transform.

        :returns: Modified dataset.
        """
        assert ds is not None, '"ds" argument should be given here'

        if self.cfg['method'] == 'coarsen':
            self.info(
                'Coarsening {} {} features'.format(
                    self.parent.parent.name, self.parent.name))
            ds_new = ds.coarsen(**self.cfg['kwargs']).mean()
        elif self.cfg['method'] == 'interp':
            self.info(
                'Interpolating {} {} features'.format(
                    self.parent.parent.name, self.parent.name))
            ds_new = ds.interp(**self.cfg['kwargs'])

        return ds_new

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        skwargs = ''.join(['_{}{}'.format(k, v)
                           for k, v in self.cfg['kwargs'].items()])
        return '{}_{}{}'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs),
            self.cfg['method'], skwargs)
