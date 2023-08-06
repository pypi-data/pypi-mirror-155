"""Italian calendar."""
from collections import OrderedDict
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
import e4clim
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
import e4clim.typing as e4tp

#: Default data-source name;
DEFAULT_SRC_NAME: tp.Final[str] = 'calendar'

#: Default variable name.
VARIABLE_NAME: tp.Final[str] = 'calendar'


class DataSource(ParsingSingleDataSourceBase):
    """Calendar for Italy."""

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None, **kwargs):
        """Initialize calendar data source.

        :param med: Mediator.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        name = name or DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs) -> tp.Set[str]:
        """Convenience function to warn that not calendar data needs to be
        downloaded.

        :returns: Names of downloaded variable.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        self.warning('{} data need not be downloaded'.format(self.name))

        return {VARIABLE_NAME}

    def parse(self, variable_component_names: e4tp.VCNType = None,
              dates: pd.DatetimeIndex = None, **kwargs) -> xr.Dataset:
        """Get array of working days, holidays and saturdays for Italy,
        and store it to member :py:attr::`data`.

        :param dates: Dates.
        :param variable_componentnames: Names of variables to download.

        :returns: Calendar dataset.

        :raises AssertionError: if "dates" argument not given.

        .. warning:: Does not take summer holidays and other school holidays
          into account.
        """
        assert dates is not None, '"dates" argument required.'

        # Create day type coordinate
        daytype_name_idx = OrderedDict({'work': 0, 'sat': 1, 'off': 2})
        daytype_coord = ('daytype_index', list(daytype_name_idx.values()))

        # Create array
        da = xr.DataArray(np.empty((dates.shape[0],), dtype=int),
                          coords=[('time', dates)])

        # Sundays
        off = (dates.dayofweek == 6)
        # Public holidays + Winter and Summer holidays
        # 1st of January: new year day
        a = (dates.dayofyear == 1)
        # 25th of April: liberation day
        b = ((dates.month == 4) & (dates.day == 25))
        # 1st of May: May Day
        c = ((dates.month == 5) & (dates.day == 1))
        # 8th to 21st of August: summer holidays
        d = ((dates.month == 8) & (dates.day > 6)
             & (dates.day < 22))
        # 1st of November: all saints
        e = ((dates.month == 11) & (dates.day == 1))
        # 8th of December: Feast of the Immaculate Conception
        f = ((dates.month == 12) & (dates.day == 8))
        # 25th to 31st of December: Christmas holidays
        g = ((dates.month == 12) & (dates.day >= 25))

        # Concatenate off days
        off = (off | a | b | c | d | e | f | g)
        da[off] = daytype_name_idx['off']

        # Saturdays
        sat = (dates.dayofweek == 5) & ~off
        da[sat] = daytype_name_idx['sat']

        # Working Days
        da[~sat & ~off] = daytype_name_idx['work']

        # Create dataset with daytype coordinate
        ds = xr.Dataset({VARIABLE_NAME: da})
        ds = ds.assign_coords(daytype=xr.DataArray(
            list(daytype_name_idx.keys()), coords=[daytype_coord]))

        return ds
