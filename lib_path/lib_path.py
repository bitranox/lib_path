# STDLIB
import binascii
import ctypes
import getpass
import importlib
import importlib.util
import logging
import os
import pathlib
import subprocess
from typing import List, Union

# INSTALLED
import lib_platform

logger = logging.getLogger()


def log_and_raise_if_path_does_not_exist(path: pathlib.Path) -> None:
    """
    >>> # SETUP
    >>> test_non_existing = pathlib.Path('does_not_exist')
    >>> test_existing_dir = pathlib.Path(__file__).parent
    >>> test_existing_file = pathlib.Path(__file__)

    >>> # Test ok
    >>> log_and_raise_if_path_does_not_exist(test_existing_dir)
    >>> log_and_raise_if_path_does_not_exist(test_existing_file)

    >>> # Test Raise
    >>> log_and_raise_if_path_does_not_exist(test_non_existing)
    Traceback (most recent call last):
    ...
    FileNotFoundError: path does not exist: does_not_exist
    """
    if not path.exists():
        s_error = f'path does not exist: {path}'
        logger.error(s_error)
        raise FileNotFoundError(s_error)


def log_and_raise_if_not_isdir(path_dir: pathlib.Path) -> None:
    """
    >>> # SETUP
    >>> test_dir_not_exist = pathlib.Path('does_not_exist')
    >>> test_dir_exist = pathlib.Path(__file__).parent
    >>> test_dir_is_file = pathlib.Path(__file__)

    >>> # TEST OK
    >>> log_and_raise_if_not_isdir(test_dir_exist)

    >>> # TEST non existent
    >>> log_and_raise_if_not_isdir(test_dir_not_exist)
    Traceback (most recent call last):
    ...
    NotADirectoryError: not a directory : does_not_exist

    >>> # TEST is file
    >>> log_and_raise_if_not_isdir(test_dir_not_exist)
    Traceback (most recent call last):
    ...
    NotADirectoryError: not a directory : does_not_exist

    """

    if not path_dir.is_dir():
        s_error = f'not a directory : {path_dir}'
        logger.error(s_error)
        raise NotADirectoryError(s_error)


def log_and_raise_if_target_directory_within_source_directory(path_source_dir: pathlib.Path, path_target_dir: pathlib.Path) -> None:
    """
    >>> # Setup
    >>> path_source_dir=pathlib.Path('/test')
    >>> path_target_dir_ok=pathlib.Path('/test2/test')
    >>> path_target_dir_err=pathlib.Path('/test/test2')

    >>> # Test OK
    >>> log_and_raise_if_target_directory_within_source_directory(path_source_dir, path_target_dir_ok)

    >>> # Test ERR
    >>> log_and_raise_if_target_directory_within_source_directory(path_source_dir, path_target_dir_err)
    Traceback (most recent call last):
    ...
    FileExistsError: target directory: "..." is within the source directory "..."

    """
    if is_target_directory_within_source_directory(path_source_dir, path_target_dir):
        s_error = f'target directory: "{path_target_dir}" is within the source directory "{path_source_dir}"'
        logger.error(s_error)
        raise FileExistsError(s_error)


def is_target_directory_within_source_directory(path_source_dir: pathlib.Path, path_target_dir: pathlib.Path) -> bool:
    s_source_dir = str(path_source_dir.resolve()).replace('\\', '/') + '/'
    s_target_dir = str(path_target_dir.resolve()).replace('\\', '/') + '/'
    if s_target_dir.startswith(s_source_dir):
        return True
    else:
        return False


def log_and_raise_if_not_isfile(path_file: pathlib.Path) -> None:
    """
    >>> # SETUP
    >>> path_file_ok = pathlib.Path(__file__)
    >>> path_file_err = pathlib.Path('does_not_exist')

    >>> # TEST OK
    >>> log_and_raise_if_not_isfile(path_file_ok)

    >>> # TEST ERR
    >>> log_and_raise_if_not_isfile(path_file_err)
    Traceback (most recent call last):
    ...
    FileNotFoundError: file does not exist or no permission: does_not_exist
    """
    if not path_file.is_file():
        s_error = f'file does not exist or no permission: {path_file}'
        logger.error(s_error)
        raise FileNotFoundError(s_error)


def path_join_posix(path: str, *paths: str) -> str:
    """
    liefert beim joinen einen Pfad jedenfalls als posix pfad retour.

    >>> path_join_posix(r'\\\\main','test')
    '//main/test'
    >>> path_join_posix('//main','test','test2')
    '//main/test/test2'
    >>> path_join_posix(r'c:\\test','test')
    'c:/test/test'
    >>> path_join_posix('//main','/test/test2','test2')
    '//main/test/test2/test2'
    >>> path_join_posix('//main','\\\\test\\\\test2','test2')
    '//main/test/test2/test2'
    >>> path_join_posix('//main','\\\\test\\\\test2','test2')
    '//main/test/test2/test2'

    """

    # sonst geht path_join_posix('//main','/test/test2','test2') schief !
    path = str(path)    # cast to string if we pass a path object
    ls_paths = []
    for s_path in paths:
        s_path = s_path.replace('\\', '/')
        s_path = s_path.lstrip('/')
        ls_paths.append(s_path)

    is_windows_unc = is_windows_network_unc(path)
    path = os.path.normpath(path)
    path = strip_and_replace_backslashes(path)
    ret_path = os.path.join(path, *ls_paths)
    ret_path = os.path.normpath(ret_path)
    ret_path = strip_and_replace_backslashes(ret_path)
    if is_windows_unc:
        ret_path = '//' + ret_path.lstrip('/')
    return ret_path


def path_remove_trailing_slashes(path: str) -> str:
    """
    Entfernt "/" am Ende des Pfades

    >>> path_remove_trailing_slashes('//test//')
    '//test'
    >>> path_remove_trailing_slashes('//test')
    '//test'

    """
    path = strip_and_replace_backslashes(path)
    path = path.rstrip('/')
    return path


def get_basename_without_extension(path_file: pathlib.Path) -> str:
    """
    conveniance function - who remembers "stem"
    >>> get_basename_without_extension(pathlib.Path('//main/xyz/test.txt'))
    'test'
    >>> get_basename_without_extension(pathlib.Path('//main/xyz/test'))
    'test'
    >>> get_basename_without_extension(pathlib.Path('//main/xyz/test.txt.back'))
    'test.txt'
    >>> get_basename_without_extension(pathlib.Path('//main/xyz/.test'))
    '.test'
    >>> get_basename_without_extension(pathlib.Path('//main/xyz/.test.txt'))
    '.test'

    """
    basename = path_file.stem
    return basename


def strip_and_replace_backslashes(path: str) -> str:
    """
    >>> strip_and_replace_backslashes('c:\\\\test')
    'c:/test'
    >>> strip_and_replace_backslashes('\\\\\\\\main\\\\install')
    '//main/install'
    """
    path = path.strip().replace('\\', '/')
    return path


def get_current_dir() -> pathlib.Path:
    """
    >>> path = get_current_dir()
    """
    return pathlib.Path.cwd().resolve()


def get_current_dir_and_change_to_home() -> pathlib.Path:
    current_path = get_current_dir()
    os.chdir(str(pathlib.Path.home()))
    return current_path


def is_windows_network_unc(path: str) -> bool:
    """
    >>> is_windows_network_unc('/test')
    False
    >>> is_windows_network_unc('c:/test')
    False
    >>> is_windows_network_unc('//main/install')
    True
    """
    path = strip_and_replace_backslashes(path)
    if path.startswith('//'):
        return True
    else:
        return False


def substract_windows_drive_letter(path: str) -> str:
    """
    >>> substract_windows_drive_letter('//main/install')
    '//main/install'
    >>> substract_windows_drive_letter('/test')
    '/test'
    >>> substract_windows_drive_letter('c:\\\\test')
    '/test'
    """
    path = strip_and_replace_backslashes(path)
    if path_starts_with_windows_drive_letter(path):
        path = path[2:]
    return path


def path_starts_with_windows_drive_letter(path: str) -> bool:
    """
    >>> path_starts_with_windows_drive_letter('//main/install')
    False
    >>> path_starts_with_windows_drive_letter('/test')
    False
    >>> path_starts_with_windows_drive_letter('c:\\\\test')
    True
    """
    path = strip_and_replace_backslashes(path)
    if path[1:].startswith(':/'):
        return True
    else:
        return False


def chdir(path: pathlib.Path) -> None:
    os.chdir(str(path))


def get_l_path_sub_directories(path_base_directory: pathlib.Path) -> List[pathlib.Path]:
    """
    gets the subdirectories of a path (non recursive)

    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent / 'tests'
    >>> path_dir_with_subdirs = path_test_dir / 'dir_with_subdirs'
    >>> path_dir_without_subdirs = path_test_dir / 'dir_without_subdirs'

    >>> get_l_path_sub_directories(path_dir_with_subdirs)
    [...Path('subdir')]
    >>> get_l_path_sub_directories(path_dir_without_subdirs)
    []

    """
    log_and_raise_if_not_isdir(path_base_directory)
    path_base_directory.resolve()

    try:
        l_sub_directories = next(os.walk(str(path_base_directory)))[1]
        l_path_sub_directories = [pathlib.Path(str(subdir)) for subdir in l_sub_directories]
        return l_path_sub_directories
    except StopIteration:
        return []


def get_windows_system_drive_letter() -> str:
    """
    >>> if lib_platform.is_platform_windows:
    ...   drive = get_windows_system_drive_letter()
    ...   assert drive == 'c:'

    """
    kernel32 = ctypes.windll.kernel32  # type: ignore
    windows_directory = ctypes.create_unicode_buffer(1024)
    if kernel32.GetWindowsDirectoryW(windows_directory, 1024) == 0:
        raise RuntimeError('can not determine Windows System Drive')
    windows_drive = os.path.splitdrive(windows_directory.value)[0].lower()
    return windows_drive


def has_subdirs(path_dir: pathlib.Path) -> bool:

    """
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent / 'tests'
    >>> path_dir_with_subdirs = path_test_dir / 'dir_with_subdirs'
    >>> path_dir_without_subdirs = path_test_dir / 'dir_without_subdirs'

    >>> # Test with subdirs
    >>> assert has_subdirs(path_dir_with_subdirs)

    >>> # Test without subdirs
    >>> assert not has_subdirs(path_dir_without_subdirs)

    """

    if len(get_l_path_sub_directories(path_dir)) > 0:
        return True
    else:
        return False


def is_directory_empty(path_directory: pathlib.Path) -> bool:
    """
    >>> # Setup
    >>> path_test_dir = pathlib.Path(__file__).parent.parent / 'tests'
    >>> path_empty_dir = path_test_dir / 'empty_dir'
    >>> if not path_empty_dir.exists():
    ...     path_empty_dir.mkdir()

    >>> # test Empty
    >>> assert is_directory_empty(path_empty_dir)
    >>> # test not empty
    >>> assert not is_directory_empty(path_test_dir)

    """
    log_and_raise_if_not_isdir(path_directory)
    is_empty = not any(path_directory.iterdir())
    return is_empty


def is_directory_writable(directory: str) -> bool:
    """
    stellt fest ob ein Verzeichnis beschreibbar ist

    >>> if lib_platform.is_platform_windows:
    ...     drive_letter = get_windows_system_drive_letter()
    ...     temp_dir = drive_letter + '/user/public/temp'
    ...     os.makedirs(temp_dir, exist_ok=True)
    ...     assert is_directory_writable(temp_dir) == True
    ... else:
    ...     temp_dir = '/tmp'
    ...     os.makedirs(temp_dir, exist_ok=True)
    ...     assert is_directory_writable(temp_dir) == True

    """
    # noinspection PyBroadException
    try:
        while True:
            # does not work on python 3.4
            # temp_file = os.urandom(16).hex()
            temp_file = binascii.hexlify(os.urandom(16)).decode()
            temp_path = path_join_posix(directory, temp_file)
            if not os.path.exists(temp_path):
                break

        pathlib.Path(temp_path).touch()
        os.remove(temp_path)
        return True

    except Exception:
        pass
        return False


def get_test_directory_path(module_name: str, test_directory_name: str = 'tests') -> pathlib.Path:
    """ Returns the absolute path to the tests directory for a module, specified by name
    this works unter Pycharm Doctest, and pytest

    >>> test_directory = get_test_directory_path('lib_path', test_directory_name='tests')
    >>> assert test_directory.is_dir()
    """
    # ok for pytest:
    path_origin_directory = pathlib.Path(str(importlib.util.find_spec(module_name).origin)).parent  # type: ignore
    path_origin_resolved_directory = path_origin_directory.resolve()
    # for doctest under pycharm, we need to go probably some levels up:
    root_directory = pathlib.Path('/')
    while True:
        if (path_origin_resolved_directory / test_directory_name).is_dir():
            break
        if path_origin_resolved_directory == root_directory:
            raise FileNotFoundError(f'test directory "{test_directory_name}" not found')
        path_origin_resolved_directory = path_origin_resolved_directory.parent
    path_to_test_directory = path_origin_resolved_directory / test_directory_name
    return path_to_test_directory


def make_test_directory_and_subdirs_fully_accessible_by_current_user(path_directory_name: Union[str, pathlib.Path]) -> None:
    """ Linux only, Change Mask to 777 for all Files and change Owner and Group to the current user
    this can be used if we need to write to test directories on travis, etc. - does nothing on windows

    >>> test_directory = get_test_directory_path('lib_path', test_directory_name='tests')
    >>> make_test_directory_and_subdirs_fully_accessible_by_current_user(test_directory)


    """
    if lib_platform.is_platform_linux:
        path_directory_name = str(path_directory_name)
        subprocess.run(['sudo', 'chown', '-R', getpass.getuser() + '.' + getpass.getuser(), path_directory_name], check=True)
        subprocess.run(['sudo', 'chmod', '-R', '777', path_directory_name], check=True)


if __name__ == '__main__':
    print('this is a library only, the executable is named lib_path_cli.py')
