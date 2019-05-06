lib_path
========

|Pypi Status| |pyversion| |license| |maintenance|

|Build Status| |Codecov Status| |Better Code| |code climate| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2019.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/lib_path.svg?branch=master
   :target: https://travis-ci.org/bitranox/lib_path
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/lib-path.svg
   :target: https://badge.fury.io/py/lib_path
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/lib_path/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/lib_path
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_path?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_path
.. |snyk security| image:: https://snyk.io/test/github/bitranox/lib_path/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_path
.. |code climate| image:: https://api.codeclimate.com/v1/badges/eafdc923e24d12513284/maintainability
   :target: https://codeclimate.com/github/bitranox/lib_path/maintainability
   :alt: Maintainability
.. |pyversion| image:: https://img.shields.io/badge/python-%3E%3D3.5-brightgreen.svg
   :target: https://badge.fury.io/py/lib_path
   :alt: Python Version

path related functions - that also work correctly with windows UNC Paths like //server/share/directory/../../directory2

`100% code coverage <https://codecov.io/gh/bitranox/lib_path>`_, mypy static type checking, tested under `Linux, OsX, Windows and Wine <https://travis-ci.org/bitranox/lib_path>`_, automatic daily builds  and monitoring

----

- `Try it Online`_
- `Installation and Upgrade`_
- `Basic Usage`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_platform/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_platform/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_platform/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/bitranox/lib_path/master?filepath=jupyter_test_lib_path.ipynb>`_

Installation and Upgrade
------------------------

From source code:

.. code-block:: bash

    # normal install
    python setup.py install
    # test without installing
    python setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    pip install lib_path

    # test without installing
    pip install lib_path --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    pip install --upgrade https://github.com/bitranox/lib_path/archive/master.zip --upgrade-strategy eager
    # normal install
    pip install --upgrade https://github.com/bitranox/lib_path/archive/master.zip
    # test without installing
    pip install https://github.com/bitranox/lib_path/archive/master.zip --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release:
    lib_path
    # for the latest Development Version :
    https://github.com/bitranox/lib_path/archive/master.zip

    # to install and upgrade all modules mentioned in requirements.txt:
    pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python -m pip install upgrade lib_path

    # for the latest Development Version
    python -m pip install upgrade https://github.com/bitranox/lib_path/archive/master.zip

Basic Usage
-----------

.. code-block:: py

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

    log_and_raise_if_directory_does_not_exist(directory: str) -> None

    log_and_raise_if_file_does_not_exist(file: str) -> None

    log_and_raise_if_path_does_not_exist(path: str) -> None

    path_join_posix(path: str, *paths: str)

    path_remove_trailing_slashes(path: str) -> str

    path_starts_with_windows_drive_letter(path: str) -> bool

    strip_and_replace_backslashes(path: str) -> str

    substract_windows_drive_letter(path: str) -> str

Requirements
------------

following modules will be automatically installed :

.. code-block:: shell

    pytest  # see : https://github.com/pytest-dev/pytest
    typing  # see : https://pypi.org/project/typing/
    lib_platform

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_path/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

