import functools
import pandas as pd
import typing as tp
import xarray as xr
import e4clim
import e4clim.typing as e4tp

TCollection = tp.TypeVar('TCollection', bound=tp.Collection[str])


@tp.overload
def ensure_collection(
    arg: None, collection_type: tp.Type[TCollection]) -> None: ...


@tp.overload
def ensure_collection(
    arg: e4tp.StrIterableType, collection_type:
    tp.Type[TCollection]) -> TCollection: ...


def ensure_collection(
        arg: tp.Optional[e4tp.StrIterableType], collection_type:
        tp.Type[TCollection]) -> tp.Optional[TCollection]:
    """Make a list containing argument or cast collection to list.

    :param arg: Argument from which to make collection.
    :param collection_type: Collection type.

    :returns: Collection containing from argument(s).

    .. note:: If `None` is given, `None` is returned.
    """
    if arg is not None:
        if isinstance(arg, str) or (not isinstance(arg, tp.Collection)):
            new_arg = collection_type([arg])
        else:
            new_arg = collection_type(arg)

        return new_arg
    else:
        return None


class Composer(object):
    """Compose functions."""

    def __init__(self, *args: e4tp.TransformStrictType, **kwargs):
        """Constructor."""
        #: Functions to compose.
        self._functions = args

        #: Composed function.
        self.composed = functools.reduce(
            lambda f, g: lambda ds=None, **kwargs_add: g(
                ds=f(ds=ds, **kwargs, **kwargs_add), **kwargs, **kwargs_add),
            self._functions, lambda ds=None, **kwargs_add: ds)

    def __call__(self, ds: e4tp.DatasetType = None,
                 **kwargs_add) -> xr.Dataset:
        """Caller.

        :param ds: Input dataset.

        :returns: Output dataset.
        """
        return self.composed(ds=ds, **kwargs_add)


def apply_transform(data_src: 'e4clim.container.data_source.DataSourceBase',
                    ds: xr.Dataset, transform: e4tp.TransformType = None,
                    **kwargs) -> xr.Dataset:
    """Apply transformation to dataset.

    :param ds: Dataset.
    :type ds: :py:class:`xarray.Dataset`

    :returns: Dataset.
    :rtype: :py:class:`xarray.Dataset`
    """
    if transform:
        kwargs.update({'ds': ds, 'data_src': data_src})
        ds = transform(**kwargs)

    return ds


def get_years_range_from_cfg(cfg: e4tp.CfgType) -> range:
    """Get safe years range from configuration.

    :param cfg: Configuration.
    :returns: Years range.
    """
    first_year = get_required_int_entry(cfg, 'first_year')
    last_year = get_required_int_entry(cfg, 'last_year')

    return range(first_year, last_year + 1)


def get_bool_entry(d: tp.Any, key: str,
                   default: bool = None) -> tp.Optional[bool]:
    """Get entry from mapping checking that its type is :py:class:`bool`
    or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`bool`,

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        value_safe = default
    else:
        assert (value is None) or isinstance(value, bool), (
            '"{}" entry in "d" argument should be "bool" '
            'or "None"'.format(key))
        value_safe = value

    return value_safe


def get_float_entry(d: tp.Any, key: str,
                    default: float = None) -> tp.Optional[float]:
    """Get entry from mapping checking that its type is :py:class:`float`
    or `None`.
    Type :py:class:`int` is allowed but converted to :py:class:`float`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`float`,

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        value_safe = default
    else:
        assert ((value is None) or isinstance(value, int) or
                isinstance(value, float)), (
                    '"{}" entry in "d" argument should be "int", '
                    '"float" or "None"'.format(key))
        value_safe = value

        # Make sure non-None value is float
        if value is not None:
            value_safe = float(value_safe)

    return value_safe


def get_int_entry(d: tp.Any, key: str,
                  default: int = None) -> tp.Optional[int]:
    """Get entry from mapping checking that its type is :py:class:`int`
    or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`int`,

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        value_safe = default
    else:
        assert (value is None) or isinstance(value, int), (
            '"{}" entry in "d" argument should be "int" '
            'or "None"'.format(key))
        value_safe = value

    return value_safe


def get_str_entry(d: tp.Any, key: str,
                  default: str = None) -> tp.Optional[str]:
    """Get entry from mapping checking that its type is :py:class:`str`
    or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`str`,

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        value_safe = default
    else:
        assert (value is None) or isinstance(value, str), (
            '"{}" entry in "d" argument should be "str" '
            'or "None"'.format(key))
        value_safe = value

    return value_safe


def get_mapping_entry(
        d: tp.Any, key: str,
        default: tp.Mapping[str, tp.Any] = None) -> tp.Optional[
            tp.Mapping[str, tp.Any]]:
    """Get entry from mapping checking that its type is
    :py:class:`typing.Mapping` or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`typing.Mapping`.

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        value_safe = default
    else:
        assert (value is None) or isinstance(value, tp.Mapping), (
            '"{}" entry in "d" argument should be a mapping '
            'or "None"'.format(key))
        value_safe = value

    return value_safe


class GetEntryType(tp.Generic[e4tp.VT], tp.Protocol):
    """Get-entry function type with optional return."""

    def __call__(self, d: tp.Any, key: str,
                 default: e4tp.VT = None) -> tp.Optional[e4tp.VT]: ...


class GetRequiredEntryType(tp.Generic[e4tp.VT], tp.Protocol):
    """Get-entry function type."""

    def __call__(self, d: tp.Any, key: str,
                 default: e4tp.VT = None) -> e4tp.VT: ...


def assert_not_none_decorator(
        func: GetEntryType[e4tp.VT]) -> GetRequiredEntryType[e4tp.VT]:
    """Decorator to asserts that returned value is not `None`.

    :param func: Function to decorate.

    :returns: Decorated function.
    """
    def f(d: tp.Any, key: str, default: e4tp.VT = None) -> e4tp.VT:
        value = func(d, key, default=default)

        assert value is not None, 'Entry value should not be "None"'

        return value

    return f


#: Get entry from mapping checking that its type is :py:class:`bool`.
get_required_bool_entry = assert_not_none_decorator(get_bool_entry)
#: Get entry from mapping checking that its type is :py:class:`float`.
get_required_float_entry = assert_not_none_decorator(get_float_entry)
#: Get entry from mapping checking that its type is :py:class:`int`.
get_required_int_entry = assert_not_none_decorator(get_int_entry)
#: Get entry from mapping checking that its type is :py:class:`str`.
get_required_str_entry = assert_not_none_decorator(get_str_entry)
#: Get entry from mapping checking that its type is :py:class:`typing.Mapping`.
get_required_mapping_entry = assert_not_none_decorator(get_mapping_entry)


def get_iterable_str_entry(
        d: tp.Any, key: str, collection_type: tp.Type[TCollection],
        default: TCollection = None) -> TCollection:
    """Get iterable from mapping and check that its type is
    :py:class:`str`, :py:class:`typing.Iterable` or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`str` or :py:class:`typing.Iterable`.

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        assert default is not None, (
            'Either entry or "default" argument required')
        value_safe = default
    else:
        assert (value is None) or isinstance(value, str) or isinstance(
            value, tp.Iterable), (
            '"{}" entry in "d" argument should be "str"'.format(key))
        value_safe = ensure_collection(value, collection_type)

    return value_safe


def get_required_iterable_str_entry(
        d: tp.Any, key: str, collection_type: tp.Type[TCollection],
        default: TCollection = None) -> TCollection:
    """Get iterable from mapping and check that its type is
    :py:class:`str`, :py:class:`typing.Iterable`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if returned value is `None`.
    """
    value = get_iterable_str_entry(d, key, collection_type, default=default)

    assert value is not None, 'Entry value should not be "None"'

    return value


def get_iterable_float_entry(
        d: tp.Any, key: str, collection_type: tp.Type[TCollection],
        default: TCollection = None) -> TCollection:
    """Get iterable from mapping and check that its type is
    :py:class:`float`, :py:class:`typing.Iterable` or `None`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if

        * :py:obj:`d` argument is not a mapping,
        * entry is not :py:class:`float` or :py:class:`typing.Iterable`.

    """
    assert isinstance(d, tp.Mapping), (
        '"d" argument should be a mapping')

    value = d.get(key)
    if value is None:
        assert default is not None, (
            'Either entry or "default" argument required')
        value_safe = default
    else:
        assert (value is None) or isinstance(value, float) or isinstance(
            value, tp.Iterable), (
            '"{}" entry in "d" argument should be "float"'.format(key))
        value_safe = ensure_collection(value, collection_type)

    return value_safe


def get_required_iterable_float_entry(
        d: tp.Any, key: str, collection_type: tp.Type[TCollection],
        default: TCollection = None) -> TCollection:
    """Get iterable from mapping and check that its type is
    :py:class:`float`, :py:class:`typing.Iterable`.

    :param d: Mapping.
    :param key: Key.
    :param default: Default value in case entry is `None`.

    :returns: Type-safe value.

    :raises AssertionError: if returned value is `None`.
    """
    value = get_iterable_float_entry(d, key, collection_type, default=default)

    assert value is not None, 'Entry value should not be "None"'

    return value


def get_frame_safe(ds: e4tp.DatasetType, key: str) -> pd.core.generic.NDFrame:
    """Get data frame from data source.

    :param key: Key.

    :returns: Data frame.

    :raises AssertionError: if input entry is not
      :py:class:`pandas.core.generic.NDFrame`.
    """
    df = ds[key]

    assert isinstance(df, pd.core.generic.NDFrame), (
        '"{}" input should be "pandas.DataFrame"'.format(key))

    return df


def get_array_safe(ds: e4tp.DatasetType, key: str) -> xr.DataArray:
    """Get data array from data source.

    :param key: Key.

    :returns: Data array.

    :raises AssertionError: if input entry is not
      :py:class:`xarray.DataArray`.
    """
    da = ds[key]

    assert isinstance(da, xr.DataArray), (
        '"{}" input should be "xarray.DataArray"'.format(key))

    return da
