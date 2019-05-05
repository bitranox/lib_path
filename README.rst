lib_path
========

|Pypi Status| |license| |maintenance| |jupyter|

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
.. |jupyter| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/bitranox/lib_path/master?filepath=jupyter_test_lib_path.ipynb
.. |code climate| image:: https://api.codeclimate.com/v1/badges/eafdc923e24d12513284/maintainability
   :target: https://codeclimate.com/github/bitranox/lib_path/maintainability
   :alt: Maintainability

path related functions

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


Requirements
------------

following modules will be automatically installed :

.. code-block:: shell

    pytest  # see : https://github.com/pytest-dev/pytest
    typing  # see : https://pypi.org/project/typing/

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

