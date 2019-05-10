.. code-block:: sh

    chdir_to_path_of_file(path: str) -> None

    expand_filelist_subdirectories(l_paths: List[str], expand_subdirs: bool = True, follow_links: bool = True) -> List[str]

    format_abs_norm_path(path: str) -> str

    get_absolute_dirname(path: str) -> str

    get_absolute_path(path: str) -> str

    get_absolute_path_relative_from_path(path: str, path2: str) -> str

    get_basename_without_extension(path: str) -> str

    get_current_dir() -> str

    get_files_and_directories_from_list_of_paths(l_paths: List[str]) -> Tuple[List[str], List[str]]

    get_files_from_directory_recursive(directory: str, followlinks: bool = True) -> List[str]

    is_relative_path(path: str) -> bool

    is_windows_network_unc(path: str) -> bool

    log_and_raise_if_not_isdir(directory: str) -> None

    log_and_raise_if_not_isfile(file: str) -> None

    log_and_raise_if_path_does_not_exist(path: str) -> None

    path_join_posix(path: str, *paths: str)

    path_remove_trailing_slashes(path: str) -> str

    path_starts_with_windows_drive_letter(path: str) -> bool

    strip_and_replace_backslashes(path: str) -> str

    substract_windows_drive_letter(path: str) -> str
