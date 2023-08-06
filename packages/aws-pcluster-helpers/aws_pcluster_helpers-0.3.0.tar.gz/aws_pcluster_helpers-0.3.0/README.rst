====================
AWS PCluster Helpers
====================


.. image:: https://img.shields.io/pypi/v/aws_pcluster_helpers.svg
        :target: https://pypi.python.org/pypi/aws_pcluster_helpers

.. image:: https://img.shields.io/travis/dabble-of-devops-bioanalyze/aws_pcluster_helpers.svg
        :target: https://travis-ci.com/dabble-of-devops-bioanalyze/aws_pcluster_helpers

.. image:: https://readthedocs.org/projects/aws-pcluster-helpers/badge/?version=latest
        :target: https://aws-pcluster-helpers.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Helpers to generate different configurations for PCluster

Installation
--------------

.. code-block:: console

    $ pip install aws_pcluster_helpers

QuickStart
--------------

Print help

.. code-block:: console

    $ pcluster-helper --help

Print sinfo table

.. code-block:: console

    $ pcluster-helper sinfo

Print nextflow slurm config to stdout

.. code-block:: console

    $ pcluster-helper gen-nxf-slurm-config --stdout

* Free software: Apache Software License 2.0
* Documentation: https://aws-pcluster-helpers.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
