=================
pyscaffoldext-nox
=================


Nox for pyscaffold.


Usage
=====

Just install this package with ``pip install ${project}`` and note that ``putup -h`` shows a new option ``--nox``. Use this flag to use nox for your next project.

This project was inspired by `SarthakJariwala's pyscaffold nox extension <https://github.com/SarthakJariwala/pyscaffoldext-nox>`_ and their efforts to create a pyscaffoldext-nox plugin. See more info `here <https://github.com/jaustinpage/pyscaffoldext-nox/issues/11>`_.

.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd pyscaffoldext-nox
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.
