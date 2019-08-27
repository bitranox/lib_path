import pathlib
from .lib_path import *


def get_version() -> str:
    with open(pathlib.Path(__file__).parent / 'version.txt', mode='r') as version_file:
        version = version_file.readline()
    return version


__title__ = 'lib_path'
__version__ = get_version()
__name__ = 'lib_path'
