.. code-block:: sh

    expand_filelist_subdirectories(l_paths: List[pathlib.Path], expand_subdirs: bool = True) -> List[pathlib.Path]

    get_basename_without_extension(path_file: pathlib.Path) -> str

    get_current_dir() -> pathlib.Path

    get_files_and_directories_from_list_of_paths(l_paths: List[pathlib.Path]) -> Tuple[List[pathlib.Path], List[pathlib.Path]]

    get_files_from_directory_recursive(path_base_dir: pathlib.Path) -> List[pathlib.Path]

    is_windows_network_unc(path: str) -> bool

    log_and_raise_if_not_isdir(directory: pathlib.Path) -> None

    log_and_raise_if_not_isfile(file: pathlib.Path) -> None

    log_and_raise_if_path_does_not_exist(path: pathlib.Path) -> None

    path_join_posix(path: str, *paths: str)

    path_remove_trailing_slashes(path: str) -> str

    path_starts_with_windows_drive_letter(path: str) -> bool

    strip_and_replace_backslashes(path: str) -> str

    substract_windows_drive_letter(path: str) -> str
