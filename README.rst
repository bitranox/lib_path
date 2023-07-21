lib_path
========


Version v1.0.3 as of 2023-07-21 see `Changelog`_

|build_badge| |codeql| |license| |jupyter| |pypi|
|pypi-downloads| |black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/lib_path/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/lib_path/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/lib_path/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/lib_path/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/lib_path/master?filepath=lib_path.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-path?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_path

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/lib_path
   :target: https://codecov.io/gh/bitranox/lib_path

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_path?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_path/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_path?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_path/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_path?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_path/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/lib_path/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_path

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/lib-path
   :target: https://pypi.org/project/lib-path/
   :alt: PyPI - Downloads

functions to handle string paths, were pathlib is not applicable.
also works correctly with windows UNC Paths like //server/share/directory/../../directory2
deprecated

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12-dev, pypy-3.9, pypy-3.10 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/lib_path/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/lib_path/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_path/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_path/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_path/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_path.ipynb>`_

Usage
-----------

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

Usage from Commandline
------------------------

.. code-block::

   Usage: lib_path [OPTIONS] COMMAND [ARGS]...

     path related function - deprecated

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program informations

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade lib_path


- to install the latest release from PyPi via pip, including test dependencies:

.. code-block::

    python -m pip install --upgrade lib_path[test]

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/lib_path.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_path

    # for the latest development version :
    lib_path @ git+https://github.com/bitranox/lib_path.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/lib_path.git
    $ cd lib_path
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_path.git
    $ cd lib_path

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
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

---

Changelog
=========

v1.0.3
--------
2023-07-21:
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.0.2
--------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

1.0.1
-----
2019-07-13:
    - dropped Python 3.4/3.5 Support
    - strict mypy type checking

1.0.0
-----
2019-04-19: Initial public release, PyPi Release

