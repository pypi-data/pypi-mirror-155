python-angreal
==============

An angreal for python3 projects. 


`init` :
---------

On initialization this angreal will create a python project.

.. code-block:: bash

    angreal init python3



`integration`:
--------------

Run integration/functional tests on the current package. These tests are housed
within `tests/integration` and are for ensuring end to end operation of portions
of software.

.. code-block:: bash

    Usage: angreal integration [OPTIONS]

      run package tests

    Options:
      --help  Show this message and exit.

`setup`:
--------

Setup the package environment. Currently creates

.. code-block:: bash

    Usage: angreal setup [OPTIONS]

      update/create the package_name environment.
      install and initialize pre-commit hooks

    Options:
      --no_dev  Don't setup a development environment.
      --help    Show this message and exit.


`tests`:
---------

Run tests on the current package.

.. code-block:: bash

    Usage: angreal tests [OPTIONS]

      run package unit tests

    Options:
      --html TEXT  generate an html report and open in a browser
      --help       Show this message and exit.
