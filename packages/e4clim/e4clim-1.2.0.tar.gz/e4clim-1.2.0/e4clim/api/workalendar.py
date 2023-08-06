"""Calendars via workalendar package."""
from collections import OrderedDict
import numpy as np
import pandas as pd
import typing as tp
import xarray as xr
from workalendar.registry import registry
import e4clim
from e4clim.container.parsing_single_data_source import (
    ParsingSingleDataSourceBase)
from e4clim.container.geo_data_source import get_country_code
import e4clim.typing as e4tp
from e4clim.utils import tools

#: Default data-source name;
DEFAULT_SRC_NAME: tp.Final[str] = 'calendar'

#: Default variable name.
VARIABLE_NAME: tp.Final[str] = 'calendar'

#: Daytype name-index.
DAYTYPE_NAME_IDX: tp.MutableMapping[str, int] = OrderedDict({
    'work': 0, 'sat': 1, 'off': 2})


class DataSource(ParsingSingleDataSourceBase):
    """Generic calendars."""

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None, **kwargs):
        """Initialize calendar data source.

        :param med: Mediator.
        :param name: Data-source name.
        :param cfg: Data-source configuration.
        """
        name = name or DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs) -> tp.MutableSet[str]:
        """Convenience function to warn that not calendar data needs to be
        downloaded.

        :returns: Names of downloaded variable.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        self.warning('{} data need not be downloaded'.format(self.name))

        return {VARIABLE_NAME}

    def parse(self, variable_component_names: e4tp.VCNType = None,
              dates: pd.DatetimeIndex = None, area: str = None,
              **kwargs) -> xr.Dataset:
        """Get array of working days, holidays and saturdays for Italy,
        and store it to member :py:attr::`data`.

        :param dates: Dates.
        :param variable_component_names: Names of variables to download.
        :param area: Area for component context.

        :returns: Calendar dataset.

        :raises AssertionError: if

            * "dates" argument not given,
            * "daytypes" values in configuration not :py:class:`str`.

        .. warning:: Does not take summer holidays and other school holidays
          into account.
        """
        assert dates is not None, '"dates" argument required'
        assert area is not None, '"area" argument required'

        # Create day type coordinate
        daytype_names = tools.get_required_iterable_str_entry(
            self.cfg, 'daytypes', list, list(DAYTYPE_NAME_IDX))
        daytype_index = [DAYTYPE_NAME_IDX[n] for n in daytype_names]
        daytype_coord = ('daytype_index', daytype_index)

        # Create array
        da = xr.DataArray(np.empty((len(dates),), dtype=int),
                          coords=[('time', dates)])

        if 'off' in daytype_names:
            # Sundays
            off = (dates.dayofweek == 6)

            # Holidays
            country_code = get_country_code(area, code='alpha-2')
            calendar = registry.get(country_code)()
            holidays = np.array([calendar.is_holiday(d) for d in dates])
            off = off | holidays

            da[off] = DAYTYPE_NAME_IDX['off']
        else:
            off = np.zeros(len(dates), dtype=bool)

        if 'sat' in daytype_names:
            sat = (dates.dayofweek == 5) & ~off
            da[sat] = DAYTYPE_NAME_IDX['sat']
        else:
            sat = np.zeros(len(dates), dtype=bool)

        # Working Days
        if 'work' in daytype_names:
            da[~sat & ~off] = DAYTYPE_NAME_IDX['work']

        # Create dataset with daytype coordinate
        ds = xr.Dataset({VARIABLE_NAME: da})
        ds = ds.assign_coords(daytype=xr.DataArray(
            daytype_names, coords=[daytype_coord]))

        return ds
