======================
cookiecutter-pylibrary
======================

Cookiecutter_ template for a ScanCode Python python library. |travis| |appveyor|

.. |travis| image:: http://img.shields.io/travis/scancode/cookiecutter-pylibrary/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/scancode/cookiecutter-pylibrary

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/scancode/cookiecutter-pylibrary?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/scancode/cookiecutter-pylibrary

*Notes*:

* This template provides a standard layout for new ScanCode libraries

Features
--------

This is an "all inclusive" sort of template.

* Apache 2.0 license with ScanCode specifics.
* Tox_ and Pytest_ for testing Python 2.7, 3.4, PyPy etc.
* *Optional* support for creating a tests matrix out of dependencies and python versions.
* Travis-CI_ and AppVeyor_ for continuous testing.
* Coveralls_ for coverage tracking (using Tox_).
* Documentation with Sphinx_, ready for ReadTheDocs_.
* Configurations for:

  * `isort <https://pypi.python.org/pypi/isort>`_
  * `bumpversion <https://pypi.python.org/pypi/bumpversion>`_

* Support for C extensions (including coverage measurement for the C code).
* Packaging and code quality checks. This template comes with a tox environment (``check``) that will:

  * Check if your ``README.rst`` is valid.
  * Check if the ``MANIFEST.in`` has any issues.
  * Run ``flake8`` (a combo of PEP8, pyflakes and McCabe checks)

Requirements for using this Cookiecutter:
----------------------------------------

To use this template to create new projects, all dependencies have been
included in the template itself, such as:

* Cookiecutter_ - for creating projects.
* Tox_ - for running the tests 
* Setuptools_ Pip_, Virtualenv_- for building the package, wheels etc.

To get quickly started on a new system, just run the configure scripts::

  ./configure

or on Windows::
  configure


Usage
-----

To generate a new project::

  cookiecutter gh:scancode/cookiecutter-pylibrary

You will be asked for these fields:

.. list-table::
    :header-rows: 1

    * - Template variable
      - Default
      - Description
    * - ``project_name``
      - .. code:: python

            "Nameless"
      - Verbose project name, used in headings (docs, readme, etc).
    * - ``repo_name``
      - .. code:: python

            "python-nameless"
      - Repository name on github.
    * - ``package_name``
      - .. code:: python

            "nameless"
      - Python package name (whatever you would import).
    * - ``distribution_name``
      - .. code:: python

            "nameless"
      - PyPI distribution name (what you would ``pip install``).
    * - ``c_extension_support``
      - .. code:: python

            "no"
      - Support C extensions (will slighly change the outputted ``setup.py``)
    * - ``c_extension_optional``
      - .. code:: python

            "yes"
      - Make C extensions optional (will allow your package to install even if extensions can't be compiled)
    * - ``test_matrix_configurator``
      - .. code:: python

            "no"
      - Enable the test matrix generator script. If you don't have a huge number of test environments then probably you
        don't need this.

The testing (``tox.ini`` and ``.travis.yml``) configurations are generated
from templates. 
For your convenience there is an initial bootstrap ``tox.ini`` to get the 
initial generation going just run::

  tox

If you enabled the ``test_matrix_configurator`` option, you can later 
regenerate ``tox.ini`` and ``.travis.yml`` by running::

  tox -e configure

After this you can create the initial repository (make sure you `create <https://github.com/new>`_ an *empty* Github
project)::

  git init .
  git add .
  git commit -m "Initial library skeletton."
  git remote add origin git@github.com:scancode/python-nameless.git
  git push -u origin master

Then:

* `Enable the repository in your Travis CI account <https://travis-ci.org/profile>`_.
* `Enable the repository in your Appveyor account <http://www.appveyor.com/>`_.
* `Enable the repository in your Coveralls account <https://coveralls.io/repos/new>`_.
* `Add the repo to your ReadTheDocs account <https://readthedocs.org/dashboard/import/>`_ + turn on the ReadTheDocs
  service hook. Don't forget to enable virtualenv and specify ``docs/requirements.txt`` as the requirements file in
  `Advanced Settings`.

Optionally 
* `Enable the repository in your Landscape account <https://landscape.io/>`_.
* `Enable the repository in your Scrutinizer account <https://scrutinizer-ci.com/>`_.
* `Enable the repository in your Drone account <https://drone.io/>`_.


Developing the project
``````````````````````

To run all the tests, just run::

  tox

To see all the tox environments::

  tox --listenvs

To only build the docs::

  tox -e docs

To build and verify that the built package is proper and other code QA checks::

  tox -e check

Releasing the project
``````````````````````

Before releasing your package on PyPI you should have all the tox environments passing.

To make a release of the project on PyPI, the most simple usage is::

  python setup.py release

(``release`` is aliased to ``register clean sdist bdist_wheel upload``, see ``setup.cfg``).

If you care about security you can do secure uploads to PyPI using `twine <https://pypi.python.org/pypi/twine>`_.

Questions & answers
-------------------

There's no Makefile?

  Sorry, no ``Makefile`` yet. The Tox_ environments stand for whatever you'd have in a ``Makefile``.

Why is the version stored in several files (``pkg/__init__.py``, ``setup.py``, ``docs/conf.py``)?

  We cannot use a metadata/version file [2]_ because this template is to be used with both distributions of packages (dirs
  with ``__init__.py``) and modules (simple ``.py`` files that go straigh in ``site-packages``). There's no good place
  for that extra file if you're distributing modules.

  But this isn't so bad - `bumpversion <https://pypi.python.org/pypi/bumpversion>`_ manages the version string quite
  neatly.

Not Exactly What You Want?
--------------------------

If you have criticism or suggestions please open up an Issue or Pull Request.

.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _Coveralls: https://coveralls.io/
.. _ReadTheDocs: https://readthedocs.org/
.. _Setuptools: https://pypi.python.org/pypi/setuptools
.. _Pytest: http://pytest.org/
.. _AppVeyor: http://www.appveyor.com/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Cookiecutter-pylibrary: https://github.com/ionelmc/cookiecutter-pylibrary
