"""Types definitions."""
import geopandas as gpd
from mypy_extensions import KwArg
from pathlib import Path
import pandas as pd
import typing as tp
import xarray as xr
import e4clim

VT = tp.TypeVar('VT')

CfgValueType = tp.Union[bool, int, float, str]

#: Configuration mapping type.
CfgMappingType = tp.Union[CfgValueType, tp.MutableMapping[str, tp.Union[
    CfgValueType, tp.MutableMapping[str, tp.Union[
        CfgValueType, tp.MutableMapping[str, tp.Union[
            CfgValueType, tp.MutableMapping[str, CfgValueType]]]]]]]]

#: Generic configuration type.
CfgType = tp.Union['e4clim.config.Config', CfgMappingType]


#: Dataset or mapping from string to data array.
StrToDataArrayType = tp.Union[xr.Dataset, tp.MutableMapping[str, xr.DataArray]]

#: Xarray dataset or dataarray.
XArrayDataType = tp.Union[xr.DataArray, xr.Dataset]

#: Generic dataarray type.
DataArrayType = tp.Union[xr.DataArray, pd.DataFrame, gpd.GeoDataFrame]

#: Generic dataset type.
DatasetType = tp.Union[xr.Dataset, tp.Mapping[str, DataArrayType]]

#: Generic dataset mutable type.
DatasetMutableType = tp.Union[xr.Dataset,
                              tp.MutableMapping[str, DataArrayType]]

#: Mapping of multiple datasets
MultiDatasetType = tp.Mapping[str, DatasetType]

#: Mapping of multiple datasets
MultiDatasetMutableType = tp.MutableMapping[str, DatasetMutableType]

#: Dataset or dataarray type.
DatasetArrayType = tp.Union[DataArrayType, DatasetType]

#: Dataset or dataarray mutable type.
DatasetArrayMutableType = tp.Union[DataArrayType, DatasetMutableType]

#: Mutable mapping from string to geographic dataframe.
GeoDatasetMutableType = tp.MutableMapping[str, gpd.GeoDataFrame]

#: Float or array (sequence) type.
FloatArrayType = tp.Union[float, tp.MutableSequence[VT]]

#: String or Path type.
PathType = tp.Union[str, Path]

#: String or collection of strings type.
StrIterableType = tp.Union[str, tp.Iterable[str]]

#: Mapping from string to container type.
StrToContainerType = tp.MutableMapping[str,
                                       'e4clim.container.base.ContainerBase']

#: Container children mutable type.
ChildrenMutableType = tp.MutableMapping[
    str, 'e4clim.container.base.ContainerBase']

#: Container children type.
ChildrenType = tp.Mapping[str, 'e4clim.container.base.ContainerBase']

#: Mapping from string to mapping from string to container type.
StrToStrToContainerType = tp.MutableMapping[str, StrToContainerType]

#: Mapping type used from data-sources names to data sources.
SingleDataSourcesType = tp.Mapping[
    str, 'e4clim.container.single_data_source.SingleDataSourceBase']

#: Mutable mapping type used from data-sources names to data sources.
SingleDataSourcesMutableType = tp.MutableMapping[
    str, 'e4clim.container.single_data_source.SingleDataSourceBase']

#: Mapping type used from data-sources names to data sources.
DataSourcesType = tp.MutableMapping[
    str, tp.Union['e4clim.container.single_data_source.SingleDataSourceBase',
                  'e4clim.container.multi_data_source.MultiDataSourceBase']]

#: Mapping type used from data-sources names to parsing data sources.
ParsingSingleDataSourcesType = tp.Mapping[
    str,
    'e4clim.container.parsing_single_data_source.ParsingSingleDataSourceBase']

#: Mapping type used from data-sources names to data sources.
ParsingDataSourcesType = tp.MutableMapping[
    str, tp.Union[
        'e4clim.container.parsing_single_data_source.ParsingSingleDataSourceBase',
        'e4clim.container.parsing_multi_data_source.ParsingMultiDataSourceBase']]

#: Mapping type used from data-sources names to data sources.
GeoSingleDataSourcesType = tp.Mapping[
    str, 'e4clim.container.geo_data_source.GeoParsingSingleDataSourceBase']

#: Mapping type used from variable names to component names.
VCNStrictType = tp.Mapping[str, tp.Set[str]]

#: Loose version of mapping type used from variable names to component names.
VCNType = tp.Union[tp.Iterable[str], tp.Mapping[str, tp.Union[
    tp.Set[str], tp.Mapping[str, str], VCNStrictType]]]

#: Mapping from string `VCNType`.
StrToVCNType = tp.Mapping[str, VCNType]

#: Mapping from string `VCNStrictType`.
StrToVCNStrictType = tp.Mapping[str, VCNStrictType]

#: Mapping type used from stages to `VCNStrictTypes`.
StageToVCNType = tp.Mapping[str, VCNStrictType]

#: Mutable mapping type used from variable names to component names.
VCNStrictMutableType = tp.MutableMapping[str, tp.MutableSet[str]]

#: Mutable mapping type used from variable names to component names.
VCNMutableType = tp.Union[tp.MutableSet[str],
                          tp.MutableMapping[str, str], VCNStrictType]

#: Mutable mapping from string `VCNType`.
StrToVCNMutableType = tp.Mapping[str, VCNMutableType]

#: Mutable mapping from string `VCNStrictType`.
StrToVCNStrictMutableType = tp.Mapping[str, VCNStrictType]

#: Mutable mapping type used from stages to `VCNStrictMutableTypes`.
StageToVCNMutableType = tp.MutableMapping[str, VCNStrictMutableType]

#: Mutable set or VCNType.
SetVCNType = tp.Union[tp.MutableSet[str], VCNType]

# Dataframes or dataarray like type.
FrameArrayType = tp.Union[pd.core.generic.NDFrame,
                          xr.core.common.DataWithCoords]

#: Place names type.
PlaceNamesType = tp.List[str]

#: Coordinates type.
CoordsType = tp.Union[xr.core.coordinates.Coordinates,
                      tp.Mapping[str, tp.Sequence[float]]]

#: Transform function type.
TransformType = tp.Union[tp.Callable[..., xr.Dataset],
                         'e4clim.utils.tools.Composer']

#: Transform function strict type.
TransformStrictType = tp.Callable[[KwArg(tp.Any)], DatasetType]
