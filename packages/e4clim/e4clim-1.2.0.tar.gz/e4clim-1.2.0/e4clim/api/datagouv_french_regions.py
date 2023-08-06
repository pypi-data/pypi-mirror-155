"""data.gouv.fr API for French regions."""
from io import BytesIO
from pathlib import Path
import requests
import typing as tp
import zipfile
import e4clim
from e4clim.container.geo_data_source import (
    GeoParsingDataSourceDefault, GEO_VARIABLE_NAME)
import e4clim.typing as e4tp
from e4clim.utils import tools

#: Available resources.
AVAILABLE_RESOURCES: tp.Final[tp.List[str]] = ['regions', 'departements']

#: Default resource.
DEFAULT_RESOURCE: tp.Final[str] = 'regions'

#: Host.
HOST: tp.Final[str] = 'https://www.data.gouv.fr/'

#: Regions file format
FILEFORMAT: tp.Final[str] = 'shp'

#: Child column.
RESOURCE_CHILD_COLUMNS: tp.Final[tp.Dict[str, str]] = {
    'regions': 'RégION',
    'departements': 'nom'
}

#: Keyword arguments for :py:func:`geopandas.read_file`.
READ_FILE_KWARGS = None

#: File types.
RESOURCE_FILETYPES: tp.Final[tp.Dict[str, tp.List[str]]] = {
    'regions': ['dbf', 'prj', 'shp', 'shx'],
    'departements': ['zip']
}

#: File type-ID.
RESOURCE_FILETYPE_IDS: tp.Final[tp.Dict[str, tp.Dict[str, str]]] = {
    'regions': {
        'dbf': 'f61cd689-9850-48f4-b7b1-751d60c5d669',
        'prj': 'd629b370-699a-46d6-bc05-86196fbf3f35',
        'shp': '69fc7722-3e40-43fc-be67-17cb335545f7',
        'shx': 'b114a44c-30f8-44de-a88b-2c7ca7842f87'
    },
    'departements': {
        'zip': 'eb36371a-761d-44a8-93ec-3d728bec17ce'
    }
}

#: Used to replace Lambert II Carto with Lambert II Etendu.
WKT: tp.Final[str] = 'PROJCS["France_II_Etendu",GEOGCS["GCS_NTF",DATUM["D_NTF",SPHEROID["Clarke_1880_IGN",6378249.2,293.46602]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",600000.0],PARAMETER["False_Northing",2200000.0],PARAMETER["Central_Meridian",2.3372291667],PARAMETER["Standard_Parallel_1",45.8989188889],PARAMETER["Standard_Parallel_2",47.6960144444],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",46.8],UNIT["Meter",1.0]]'


class DataSource(GeoParsingDataSourceDefault):
    #: Default source name.
    DEFAULT_SRC_NAME: tp.Final[str] = 'datagouv_french_regions'

    #: Area.
    AREA: tp.Final[str] = 'France'

    #: Resource.
    resource: str

    def __init__(self, parent: 'e4clim.context.base.ContextBase',
                 name: str = None, cfg: e4tp.CfgType = None,
                 **kwargs) -> None:
        """Initialize geographic data source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration.

        :raise AssertionError: if :py:obj:`resource` not in
          :py:obj:`AVAILABLE_RESOURCES`.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(parent, name, cfg=cfg, **kwargs)

        # Add configuration for
        # :py:func:`e4clim.container.geo_data_source.GeoParsingDataSourceDefault.read_file`
        self.cfg['read_file_kwargs'] = READ_FILE_KWARGS

        # Get resource from configuration
        self.resource = tools.get_required_str_entry(
            self.cfg, 'resource', DEFAULT_RESOURCE)
        assert self.resource in AVAILABLE_RESOURCES, (
            '"resource" attribute should be in {}'.format(AVAILABLE_RESOURCES))

        # Add configuration for
        # :py:func:`e4clim.container.geo_data_source.GeoParsingDataSourceDefault`
        self.cfg['child_column'] = RESOURCE_CHILD_COLUMNS[self.resource]

    def download(self, variable_component_names: e4tp.VCNType = None,
                 **kwargs) -> e4tp.VCNType:
        """Download shapefile defining regions and
        store geographical data to :py:attr::`data` member.

        :returns: Names of downloaded variables.
        """
        # Make source dir
        src_dir = self.med.cfg.get_external_data_directory(self, **kwargs)

        # Get downloaded-file name
        filename_shp = self.get_filename(**kwargs)

        # Download
        root_url = '{}/fr/datasets/r/'.format(HOST)
        self.info('Downloading shapefile from {}'.format(root_url))
        for filetype in RESOURCE_FILETYPES[self.resource]:
            filename = '{}.{}'.format(filename_shp[:-4], filetype)
            filepath = Path(src_dir, filename)
            if filetype == 'prj':
                with open(filepath, 'w') as f:
                    # Replace Lambert II Carto with Lambert II Etendu
                    f.write(WKT)
            else:
                url = '{}{}'.format(root_url, RESOURCE_FILETYPE_IDS[
                    self.resource][filetype])

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                if filetype == 'zip':
                    # Open zip
                    zip_ref = zipfile.ZipFile(BytesIO(response.content))

                    # Write all files in zip
                    for f_sub in zip_ref.filelist:
                        extension = Path(f_sub.filename).suffix
                        filename_sub = '{}{}'.format(
                            filename_shp[:-4], extension)
                        filepath_sub = Path(src_dir, filename_sub)

                        # Unzip single file
                        f_sub.filename = filepath_sub.name
                        zip_ref.extract(f_sub, filepath_sub.parent)
                    zip_ref.close()

                else:
                    # Write file
                    with open(filepath, 'wb') as fb:
                        for chunk in response:
                            fb.write(chunk)

        return {GEO_VARIABLE_NAME}

    def get_filename(self, *args, **kwargs) -> str:
        """Get filename of geographical data for a given region.

        :returns: Shapefile filename.
        """
        return '{}.{}'.format(self.resource, FILEFORMAT)
