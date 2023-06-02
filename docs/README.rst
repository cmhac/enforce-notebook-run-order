enforce-notebook-run-order
==========================

Enforce the run order of Jupyter notebooks.

Jupyter notebooks are great for interactive data analysis. However, when
they can encourage a bad habit: running cells out of order. This can lead
to notebooks being committed to the repository in a state where they don't run
from top to bottom, and other collaborators may receive different results
when running the notebook from top to bottom.

``enforce-notebook-run-order`` enforces the run order of a notebook by raising an exception if
any cells are run out of order.

Installation
------------

``enforce-notebook-run-order`` can be installed via pip:

.. code-block:: bash

    pip install enforce-notebook-run-order

It can also be set up as a `pre-commit hook <https://pre-commit.com/>`__. See the
`pre-commit hook <#pre-commit-hook>`__ section for more details.

Usage
-----

``enforce-notebook-run-order`` can be used as a standalone script, or as a `pre-commit hook <https://pre-commit.com/>`__.

Standalone
^^^^^^^^^^

To use ``enforce-notebook-run-order`` as a standalone script, simply run it with the path to the
notebook you want to check:

.. code-block:: bash

    enforce-notebook-run-order my_notebook.ipynb

Or point it to a directory to check all notebooks in that directory:

.. code-block:: bash

    enforce-notebook-run-order my_notebooks/

pre-commit hook
^^^^^^^^^^^^^^^

To use ``enforce_notebook_run_order`` as a pre-commit hook, add the following to your ``.pre-commit-config.yaml``:

.. code-block:: yaml

    - repo: https://github.com/christopher-hacker/enforce-notebook-run-order
        rev: 0.1.5
        hooks:
        - id: enforce-notebook-run-order
            name: enforce-notebook-run-order
            entry: enforce-notebook-run-order
            types: [jupyter]