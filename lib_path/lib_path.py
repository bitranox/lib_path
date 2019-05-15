import ctypes
import lib_platform
import logging
import os
from typing import List, Tuple

logger = logging.getLogger()


def expand_filelist_subdirectories(l_paths: List[str], expand_subdirs: bool = True, follow_links: bool = True) -> List[str]:
    """
    takes a mixed list of directories and files, and returns a list of files expanding the subdirectories
    >>> # get test directory
    >>> test_dir1 = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/test_a_a'
    >>> test_dir2 = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/test_a_b'
    >>> test_file1 = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/file_test_a_1.txt'
    >>> l_files = sorted(expand_filelist_subdirectories([test_dir1, test_dir2, test_file1]))
    >>> assert l_files[0].endswith('/tests/test_a/file_test_a_1.txt')
    >>> assert l_files[1].endswith('/tests/test_a/test_a_a/.file_test_a_a_1.txt')
    >>> assert l_files[2].endswith('/tests/test_a/test_a_a/.file_test_a_a_2.txt')
    >>> assert l_files[3].endswith('/tests/test_a/test_a_a/file_test_a_a_1.txt')
    >>> assert l_files[4].endswith('/tests/test_a/test_a_a/file_test_a_a_2.txt')
    >>> assert l_files[5].endswith('/tests/test_a/test_a_b/.file_test_a_b_1.txt')
    >>> assert l_files[6].endswith('/tests/test_a/test_a_b/.file_test_a_b_2.txt')
    >>> assert l_files[7].endswith('/tests/test_a/test_a_b/file_test_a_b_1.txt')
    >>> assert l_files[8].endswith('/tests/test_a/test_a_b/file_test_a_b_2.txt')
    >>> assert len(l_files) == 9

    """

    l_files, l_dirs = get_files_and_directories_from_list_of_paths(l_paths)
    if expand_subdirs:
        for directory in l_dirs:
            l_directory_files = get_files_from_directory_recursive(directory, follow_links)
            l_files = l_files + l_directory_files
    l_files = list(set(l_files))    # deduplicate
    return l_files


def get_files_and_directories_from_list_of_paths(l_paths: List[str]) -> Tuple[List[str], List[str]]:
    """
    returns [files], [directories] absolute Paths

    >>> # get test directory
    >>> test_dir = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a'
    >>> l_content_of_test_dir = os.listdir(test_dir)
    >>> # get content of test directory
    >>> item = ''
    >>> l_content_of_test_dir_absolute = [ path_join_posix(test_dir, item) for item in l_content_of_test_dir]
    >>> # test
    >>> l_files, l_dirs = get_files_and_directories_from_list_of_paths(l_content_of_test_dir_absolute)
    >>> l_files = sorted(l_files)
    >>> assert len(l_files) == 6
    >>> assert l_files[0].endswith('/test_a/.file_test_a_1.txt')
    >>> assert l_files[1].endswith('/test_a/.file_test_a_2.txt')
    >>> assert l_files[2].endswith('/test_a/.gitignore')
    >>> assert l_files[3].endswith('/test_a/.rotekignore')
    >>> assert l_files[4].endswith('/test_a/file_test_a_1.txt')
    >>> assert l_files[5].endswith('/test_a/file_test_a_2.txt')
    >>> l_dirs = sorted(l_dirs)
    >>> assert len(l_dirs) == 4
    >>> assert l_dirs[0].endswith('/tests/test_a/.test_a_a')
    >>> assert l_dirs[1].endswith('/tests/test_a/.test_a_b')
    >>> assert l_dirs[2].endswith('/tests/test_a/test_a_a')
    >>> assert l_dirs[3].endswith('/tests/test_a/test_a_b')

    >>> # test not a file or directory
    >>> l_files, l_dirs = get_files_and_directories_from_list_of_paths(['something'])  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: path does not exist: .../something

    """

    l_files = list()
    l_dirs = list()

    for path in l_paths:
        path = strip_and_replace_backslashes(path)
        path = format_abs_norm_path(path)
        log_and_raise_if_path_does_not_exist(path)
        if os.path.isfile(path):
            l_files.append(path)
        else:
            path = path_remove_trailing_slashes(path)
            l_dirs.append(path)
    return l_files, l_dirs


def get_files_from_directory_recursive(directory: str, followlinks: bool = True) -> List[str]:
    """
    >>> # get test directory
    >>> test_dir = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a'
    >>> l_files = sorted(get_files_from_directory_recursive(test_dir, followlinks=True))
    >>> assert l_files[0].endswith('/tests/test_a/.file_test_a_1.txt')
    >>> assert l_files[1].endswith('/tests/test_a/.file_test_a_2.txt')
    >>> assert l_files[2].endswith('/tests/test_a/.gitignore')
    >>> assert l_files[3].endswith('/tests/test_a/.rotekignore')
    >>> assert l_files[4].endswith('/tests/test_a/.test_a_a/.file_test_a_a_1.txt')
    >>> assert l_files[5].endswith('/tests/test_a/.test_a_a/.file_test_a_a_2.txt')
    >>> assert l_files[6].endswith('/tests/test_a/.test_a_a/file_test_a_a_1.txt')
    >>> assert l_files[7].endswith('/tests/test_a/.test_a_a/file_test_a_a_2.txt')
    >>> assert l_files[8].endswith('/tests/test_a/.test_a_b/.file_test_a_b_1.txt')
    >>> assert l_files[9].endswith('/tests/test_a/.test_a_b/.file_test_a_b_2.txt')
    >>> assert l_files[10].endswith('/tests/test_a/.test_a_b/file_test_a_b_1.txt')
    >>> assert l_files[11].endswith('/tests/test_a/.test_a_b/file_test_a_b_2.txt')
    >>> assert l_files[12].endswith('/tests/test_a/file_test_a_1.txt')
    >>> assert l_files[13].endswith('/tests/test_a/file_test_a_2.txt')
    >>> assert l_files[14].endswith('/tests/test_a/test_a_a/.file_test_a_a_1.txt')
    >>> assert l_files[15].endswith('/tests/test_a/test_a_a/.file_test_a_a_2.txt')
    >>> assert l_files[16].endswith('/tests/test_a/test_a_a/file_test_a_a_1.txt')
    >>> assert l_files[17].endswith('/tests/test_a/test_a_a/file_test_a_a_2.txt')
    >>> assert l_files[18].endswith('/tests/test_a/test_a_b/.file_test_a_b_1.txt')
    >>> assert l_files[19].endswith('/tests/test_a/test_a_b/.file_test_a_b_2.txt')
    >>> assert l_files[20].endswith('/tests/test_a/test_a_b/file_test_a_b_1.txt')
    >>> assert l_files[21].endswith('/tests/test_a/test_a_b/file_test_a_b_2.txt')
    >>> assert len(l_files) == 22
    """
    log_and_raise_if_not_isdir(directory)
    l_result_files = list()

    for root, l_dir, l_file in os.walk(directory, followlinks=followlinks):
        for file in l_file:
            path = path_join_posix(root, file)
            log_and_raise_if_not_isfile(path)
            path = format_abs_norm_path(path)
            l_result_files.append(path)
    return l_result_files


def log_and_raise_if_path_does_not_exist(path: str) -> None:
    """
    >>> log_and_raise_if_path_does_not_exist('does_not_exist')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: path does not exist: does_not_exist
    """
    if not os.path.exists(path):
        s_error = 'path does not exist: {path}'.format(path=path)
        logger.error(s_error)
        raise FileNotFoundError(s_error)


def log_and_raise_if_not_isdir(directory: str) -> None:
    """
    >>> log_and_raise_if_not_isdir('does_not_exist')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    NotADirectoryError: not a directory : does_not_exist
    """

    if not os.path.isdir(directory):
        s_error = 'not a directory : {directory}'.format(directory=directory)
        logger.error(s_error)
        raise NotADirectoryError(s_error)


def log_and_raise_if_target_directory_within_source_directory(source_directory: str, target_directory: str) -> None:
    """
    >>> log_and_raise_if_target_directory_within_source_directory('/test', '/test/test2')    # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileExistsError: target directory: "/test/test2" is within the source directory "/test"

    >>> log_and_raise_if_target_directory_within_source_directory('/test', '/test2')
    """
    if is_target_directory_within_source_directory(source_directory, target_directory):
        s_error = 'target directory: "{}" is within the source directory "{}"'.format(target_directory, source_directory)
        logger.error(s_error)
        raise FileExistsError(s_error)


def is_target_directory_within_source_directory(source_directory: str, target_directory: str) -> bool:
    source_directory = format_abs_norm_path(source_directory) + '/'
    target_directory = format_abs_norm_path(target_directory) + '/'
    if target_directory.startswith(source_directory):
        return True
    else:
        return False


def log_and_raise_if_not_isfile(file: str) -> None:
    """
    >>> log_and_raise_if_not_isfile('does_not_exist')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    FileNotFoundError: file does not exist or no permission: does_not_exist
    """

    if not os.path.isfile(file):
        s_error = 'file does not exist or no permission: {file}'.format(file=file)
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


def get_basename_without_extension(path: str) -> str:
    """
    >>> get_basename_without_extension('//main/xyz/test.txt')
    'test'
    >>> get_basename_without_extension('//main/xyz/test')
    'test'
    >>> get_basename_without_extension('//main/xyz/test.txt.back')
    'test.txt'
    """
    basename = os.path.basename(path)
    if '.' in basename:
        basename = basename.rsplit('.', 1)[0]
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


def get_current_dir() -> str:
    """
    >>> path = get_current_dir()
    """
    current_dir = format_abs_norm_path(os.curdir)
    return current_dir


def is_windows_network_unc(path: str) -> bool:
    """
    >>> is_windows_network_unc('/test')
    False
    >>> is_windows_network_unc('c:/test')
    False
    >>> is_windows_network_unc('//install/main')
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
    >>> get_absolute_dirname('./lib_path.py')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '.../lib_path...'
    """
    absolute_filename = format_abs_norm_path(path)
    absolute_dirname = os.path.dirname(absolute_filename)
    absolute_dirname = strip_and_replace_backslashes(absolute_dirname)
    absolute_dirname = path_remove_trailing_slashes(absolute_dirname)
    return absolute_dirname


def chdir_to_path_of_file(path: str) -> None:
    """
    >>> save_dir = get_current_dir()
    >>> test_file = strip_and_replace_backslashes(str(__file__)).rsplit('/lib_path/', 1)[0] + '/tests/test_a/file_test_a_1.txt'
    >>> chdir_to_path_of_file(test_file)
    >>> cur_dir = get_current_dir()
    >>> assert cur_dir.endswith('/lib_path/tests/test_a')
    >>> os.chdir(save_dir)
    """

    if path:
        absolute_dirname = get_absolute_dirname(path)
        os.chdir(absolute_dirname)


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
    '.../lib_path/main/test2'
    >>> format_abs_norm_path('//main')
    '//main'
    >>> format_norm_path('c:/test/../test2/test.txt')
    'c:/test2/test.txt'

    """

    path = strip_and_replace_backslashes(path)

    if lib_platform.is_platform_windows and is_windows_network_unc(path):
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

    if lib_platform.is_platform_windows and is_windows_network_unc(path):
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
    ...   assert drive[1] == ':'

    """
    kernel32 = ctypes.windll.kernel32  # type: ignore
    windows_directory = ctypes.create_unicode_buffer(1024)
    if kernel32.GetWindowsDirectoryW(windows_directory, 1024) == 0:
        raise RuntimeError('can not determine Windows System Drive')
    windows_directory = str(windows_directory)
    windows_drive = os.path.splitdrive(windows_directory)[0].lower()
    return windows_drive
