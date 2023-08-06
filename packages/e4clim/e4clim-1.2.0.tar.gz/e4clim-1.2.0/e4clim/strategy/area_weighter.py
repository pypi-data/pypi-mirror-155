"""Modifier to weight dataset by grid area."""
import numpy as np
import xarray as xr
import iris
from e4clim.container.strategy import ExtractorBase
from e4clim.utils import tools


class Strategy(ExtractorBase):
    """Strategy to weight a gridded dataset by grid-boxes areas."""

    def transform(self, ds: xr.Dataset = None, **kwargs) -> xr.Dataset:
        """Apply modifier to data source.

        :param ds: Dataset to transform.

        :returns: Modified dataset.
        """
        assert ds is not None, '"ds" argument should be given here'

        for da_name, da in ds.items():
            self.info('Area weighting {} {}'.format(
                self.parent.parent.name, da_name))

            # Remove standard_name attribute to prevent ValueError
            if 'standard_name' in da.attrs:
                del da.attrs['standard_name']

            # Get cube from array
            cube = da.to_iris()
            try:
                # Try to get area from existing bounds
                area = iris.analysis.cartography.area_weights(cube)
            except ValueError:
                # Get area from guessed bounds
                try:
                    cube.coord('longitude').guess_bounds()
                    cube.coord('latitude').guess_bounds()
                except iris.exceptions.CoordinateNotFoundError:
                    cube.coord('grid_longitude').guess_bounds()
                    cube.coord('grid_latitude').guess_bounds()
                area = iris.analysis.cartography.area_weights(cube)

            # Convert to array
            da_area = xr.DataArray(area, coords=da.coords)

            normalize = tools.get_required_bool_entry(
                self.cfg, 'normalize', default=False)
            if normalize:
                # Normalize by mean area
                da_area /= da_area.sum() / np.prod(da_area.shape)

            # Weight by area
            ds[da_name] *= da_area

        return ds

    def get_extractor_postfix(self, **kwargs) -> str:
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_weighted'.format(
            super(Strategy, self).get_extractor_postfix(**kwargs))

        normalize = tools.get_required_bool_entry(
            self.cfg, 'normalize', default=False)

        postfix += '_norm' * normalize

        return postfix
