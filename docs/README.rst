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
notebook(s) you want to check:

.. code-block:: bash

    nbcheck my_notebook.ipynb my_other_notebook.ipynb

Or point it to a directory to check all notebooks in that directory:

.. code-block:: bash

    nbcheck my_notebooks/

You can also use the full ``enforce-notebook-run-order`` command, but the ``nbcheck`` command is
provided as a convenience.

For information on the command line interface, please refer to the `CLI documentation <module_enforce_notebook_run_order.html#command-line-interface>`__.

pre-commit hook
^^^^^^^^^^^^^^^

To use ``enforce_notebook_run_order`` as a pre-commit hook, add the following to your ``.pre-commit-config.yaml``:

.. code-block:: yaml

    repos:
    -   repo: https://github.com/christopher-hacker/enforce_notebook_run_order
        rev: 1.0.0
        hooks:
        -   id: enforce-notebook-run-order