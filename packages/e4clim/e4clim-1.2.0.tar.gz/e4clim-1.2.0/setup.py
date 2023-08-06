import versioneer
from pathlib import Path
import sys
from setuptools import setup, find_packages
sys.path.insert(0, Path.cwd())


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(Path(Path(__file__).parent, fname)).read()


name = 'e4clim'
long_name = 'Energy for CLimate Integrated Model'
maintainer = 'alexis.tantet'
version = versioneer.get_version()
description = 'The {} for climate-aware renewable energy mixes'.format(
    long_name)
host = 'in2p3.fr'
gitlab_project = 'energy4climate'
home = 'https://gitlab.{}/{}/{}/{}'.format(host, gitlab_project, name, name)
doc_url = 'https://{}.pages.{}/{}/{}/'.format(gitlab_project, host, name, name)
license = 'GPLv3'
license_file = 'LICENSE.txt'

setup(
    name=name,
    long_name=long_name,
    version=version,
    cmdclass=versioneer.get_cmdclass(),
    author="{} developpers".format(long_name),
    author_email="{}@lmd.polytechnique.fr".format(maintainer),
    maintainer=maintainer,
    description=description,
    license=license,
    license_file=license_file,
    url=home,
    doc_url=doc_url,
    project_urls={"Documentation": doc_url},
    packages=find_packages(),
    long_description=read('README.md'),
    command_options={
        'build_sphinx': {}
    },
    install_requires=[
        'oyaml', 'numpy', 'scipy', 'pandas', 'xarray', 'dask', 'netcdf4',
        'netCDF4', 'h5netcdf', 'scikit-learn', 'matplotlib', 'python-dateutil',
        'requests', 'geopandas', 'descartes', 'entsoe-py'
    ],
    package_data={name: ['data/*', 'data/**/*', 'data/**/**/*',
                         'cfg/*', 'cfg/**/*']},
    entry_points={
        'console_scripts': [
            '{}-create-project = {}.bin.init:create_project'.format(
                name, name),
        ],
    }
)
