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
from typing import List, Tuple, Union

# INSTALLED
import lib_platform

logger = logging.getLogger()


def expand_filelist_subdirectories(l_paths: List[pathlib.Path], expand_subdirs: bool = True) -> List[pathlib.Path]:
    """
    takes a mixed list of directories and files, and returns a list of files expanding the subdirectories
    >>> # get test directory
    >>> test_dir = get_test_directory_path('lib_path', 'tests')
    >>> path_test_dir1 = test_dir / 'test_a/test_a_a'
    >>> path_test_dir2 = test_dir / 'test_a/test_a_b'
    >>> path_test_file1 = test_dir / 'test_a/file_test_a_1.txt'
    >>> l_files = expand_filelist_subdirectories([path_test_dir1, path_test_dir2, path_test_dir2, path_test_file1])
    >>> assert len(l_files) > 0

    """

    l_path_files, l_path_dirs = get_files_and_directories_from_list_of_paths(l_paths)
    if expand_subdirs:
        for path_dir in l_path_dirs:
            l_directory_files = get_files_from_directory_recursive(path_dir)
            l_path_files = l_path_files + l_directory_files
    l_path_files = list(set(l_path_files))    # deduplicate
    return l_path_files


def get_files_and_directories_from_list_of_paths(l_paths: List[pathlib.Path]) -> Tuple[List[pathlib.Path], List[pathlib.Path]]:
    """
    returns [files], [directories] absolute Paths

    >>> # SETUP
    >>> test_dir = get_test_directory_path('lib_path', 'tests') / 'test_a'
    >>> l_paths = list(test_dir.glob('**/*'))
    >>> l_paths_error = list(test_dir.glob('**/*'))
    >>> l_paths_error.append(pathlib.Path('non_existing'))

    >>> # TEST OK
    >>> l_files, l_dirs = get_files_and_directories_from_list_of_paths(l_paths)
    >>> assert len(l_files) > 0
    >>> assert len(l_dirs) > 0
    >>> assert len(l_files) > len(l_dirs)

    >>> # Test non Existing
    >>> l_files, l_dirs = get_files_and_directories_from_list_of_paths(l_paths_error)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: path does not exist: ...non_existing

    """

    l_files = list()
    l_dirs = list()

    for path in l_paths:
        path = path.resolve()
        log_and_raise_if_path_does_not_exist(path)
        if path.is_file():
            l_files.append(path)
        else:
            l_dirs.append(path)
    return l_files, l_dirs


def get_files_from_directory_recursive(path_base_dir: pathlib.Path) -> List[pathlib.Path]:
    """
    >>> # get test directory
    >>> test_dir = get_test_directory_path('lib_path', 'tests')
    >>> l_path_result = get_files_from_directory_recursive(test_dir)
    """
    log_and_raise_if_not_isdir(path_base_dir)
    path_base_dir = path_base_dir.resolve()
    l_path = list(path_base_dir.glob('**/*'))
    l_path_result = [path for path in l_path if path.is_file()]
    return l_path_result


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
    >>> log_and_raise_if_path_does_not_exist(test_non_existing)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: path does not exist: does_not_exist
    """
    if not path.exists():
        s_error = 'path does not exist: {path}'.format(path=path)
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
    >>> log_and_raise_if_not_isdir(test_dir_not_exist)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    NotADirectoryError: not a directory : does_not_exist

    >>> # TEST is file
    >>> log_and_raise_if_not_isdir(test_dir_not_exist)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    NotADirectoryError: not a directory : does_not_exist

    """

    if not path_dir.is_dir():
        s_error = 'not a directory : {path_dir}'.format(path_dir=path_dir)
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
    >>> log_and_raise_if_target_directory_within_source_directory(path_source_dir, path_target_dir_err)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileExistsError: target directory: "/test/test2" is within the source directory "/test"

    """
    if is_target_directory_within_source_directory(path_source_dir, path_target_dir):
        s_error = 'target directory: "{}" is within the source directory "{}"'.format(path_target_dir, path_source_dir)
        logger.error(s_error)
        raise FileExistsError(s_error)


def is_target_directory_within_source_directory(path_source_dir: pathlib.Path, path_target_dir: pathlib.Path) -> bool:
    s_source_dir = str(path_source_dir.resolve()) + '/'
    s_target_dir = str(path_target_dir.resolve()) + '/'
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
    >>> log_and_raise_if_not_isfile(path_file_err)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: file does not exist or no permission: does_not_exist
    """
    if not path_file.is_file():
        s_error = 'file does not exist or no permission: {path_file}'.format(path_file=path_file)
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


def is_relative_path(path: str) -> bool:
    """
    >>> is_relative_path('/test/test.txt')
    False
    >>> is_relative_path('//main/install')
    False

    >>> import platform
    >>> is_windows = platform.system().lower() == 'windows'
    >>> result = is_relative_path('c:/test/test.txt')
    >>> if is_windows:
    ...    assert result == False
    ... else:
    ...    assert result == True

    >>> result = is_relative_path('D:/test/test.txt')
    >>> if is_windows:
    ...    assert result == False
    ... else:
    ...    assert result == True

    >>> is_relative_path('.test/test.txt')
    True
    >>> is_relative_path('test/test.txt')
    True
    >>> is_relative_path('./test/test.txt')
    True
    >>> is_relative_path('....../test/test.txt')
    True
    >>> is_relative_path('../../../test/test.txt')
    True

    """
    dirname = strip_and_replace_backslashes(os.path.dirname(path))  # windows : /test
    abspath = strip_and_replace_backslashes(os.path.abspath(dirname))        # windows : C:/test
    if not path_starts_with_windows_drive_letter(dirname):
        abspath = substract_windows_drive_letter(abspath)
    if dirname != abspath:
        return True
    else:
        return False


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


def get_absolute_path(path: str) -> str:
    """
    >>> get_absolute_path('./test.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../test.py'
    """
    path = format_abs_norm_path(path)
    return path


def get_absolute_dirname(path: str) -> str:
    """
    >>> get_absolute_dirname('//main/test/../test2/lib_path.py')
    '//main/test2'
    """
    absolute_filename = format_abs_norm_path(path)
    absolute_dirname = os.path.dirname(absolute_filename)
    absolute_dirname = strip_and_replace_backslashes(absolute_dirname)
    absolute_dirname = path_remove_trailing_slashes(absolute_dirname)
    return absolute_dirname


def chdir(path: pathlib.Path):
    os.chdir(str(path))


def chdir_to_path_of_file(path_file: pathlib.Path) -> None:
    """
    >>> # SETUP
    >>> save_dir = get_current_dir()
    >>> test_file = pathlib.Path(__file__).parent.parent / 'tests/test_a/file_test_a_1.txt'

    >>> # Change Dir
    >>> chdir_to_path_of_file(test_file)
    >>> cur_dir = get_current_dir()
    >>> assert str(cur_dir).endswith('/lib_path/tests/test_a')

    >>> # Teardown
    >>> os.chdir(str(save_dir))
    """

    if path_file:
        path_file = path_file.resolve()
        path_file_dir = path_file.parent
        os.chdir(str(path_file_dir))


def get_absolute_path_relative_from_path(path: str, path2: str) -> str:
    """
    if the first path is relative, on windows the drive will be the current drive.
    this is necessary because WINE gives drive "Z" back !

    >>> # path1 absolut, path2 relativ
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> # path1 relativ, path2 relativ
    >>> get_absolute_path_relative_from_path('./a/b/c/some-file.txt', './d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/c/d/test.txt'
    >>> # path1 absolut, path2 absolut
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', 'c:/d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../d/test.txt'
    >>> # path1 relativ, path2 absolut
    >>> get_absolute_path_relative_from_path('./a/b/c/some-file.txt', 'c:/d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../d/test.txt'
    >>> # path one level back
    >>> get_absolute_path_relative_from_path('c:/a/b/c/some-file.txt', '../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/b/d/test.txt'
    >>> # path two levels back
    >>> get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '../../d/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../a/d/test.txt'
    >>> result = get_absolute_path_relative_from_path('./a/b/c/some_file.txt', '/f/test.txt')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> result = substract_windows_drive_letter(result)
    >>> assert result.lower() == '/f/test.txt'

    """

    if is_relative_path(path2):
        base_path = get_absolute_dirname(path)
        result_path = format_abs_norm_path(base_path + '/' + path2)
    else:
        result_path = format_abs_norm_path(path2)
    return result_path


def format_abs_norm_path(path: str) -> str:
    """
    >>> format_abs_norm_path(r'\\\\main')
    '//main'
    >>> # get test file
    >>> test_file = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/file_test_a_1.txt'
    >>> result = format_abs_norm_path(test_file)
    >>> assert result.endswith('/tests/test_a/file_test_a_1.txt')
    >>> format_abs_norm_path('//main/test')
    '//main/test'
    >>> format_abs_norm_path('//main/test/../test2')
    '//main/test2'
    >>> format_abs_norm_path('main/test/../test2')     # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../main/test2'
    >>> format_abs_norm_path('//main')
    '//main'
    >>> format_norm_path('c:/test/../test2/test.txt')
    'c:/test2/test.txt'

    """

    path = strip_and_replace_backslashes(path)

    if lib_platform.is_platform_windows and is_windows_network_unc(path):   # type: ignore
        path = '/' + path.lstrip('/')
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        path = '/' + substract_windows_drive_letter(path)
    else:
        path = os.path.normpath(path)
        path = os.path.abspath(path)
    path = strip_and_replace_backslashes(path)
    return path


def format_norm_path(path: str) -> str:
    """
    >>> format_norm_path(r'\\\\main')
    '//main'
    >>> # get test file
    >>> test_file = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/file_test_a_1.txt'
    >>> result = format_abs_norm_path(test_file)
    >>> assert result.endswith('/tests/test_a/file_test_a_1.txt')
    >>> format_norm_path('//main/test')
    '//main/test'
    >>> format_norm_path('//main/test/../test2')
    '//main/test2'
    >>> format_norm_path('main/test/../test2')
    'main/test2'
    >>> format_norm_path('//main')
    '//main'
    >>> format_norm_path('c:/test/../test2/test.txt')
    'c:/test2/test.txt'

    """
    path = strip_and_replace_backslashes(path)

    if lib_platform.is_platform_windows and is_windows_network_unc(path):    # type: ignore
        path = '/' + path.lstrip('/')
        path = os.path.normpath(path)
        path = '/' + substract_windows_drive_letter(path)
    else:
        path = os.path.normpath(path)
    path = strip_and_replace_backslashes(path)
    return path


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
            raise FileNotFoundError('test directory "{test_directory_name}" not found'.format(test_directory_name=test_directory_name))
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
        proc_chown = subprocess.run(['sudo', 'chown', '-R', getpass.getuser() + '.' + getpass.getuser(), path_directory_name], check=True)
        proc_chmod = subprocess.run(['sudo', 'chmod', '-R', '777', path_directory_name], check=True)
