enforce-notebook-run-order
==========================

Enforce the run order of Jupyter notebooks.

Jupyter notebooks are great for interactive data analysis. However, they
can encourage a bad habit: running cells out of order. This can lead
to notebooks being committed to the repository in a state where they don't run
from top to bottom, and other collaborators may receive different results
when running the notebook from top to bottom.

``enforce-notebook-run-order`` enforces the run order of a notebook by raising an exception if
any cells are run out of order.

Language Support
----------------

This tool works with **all Jupyter notebook kernels**, including:

* **Python** (IPython)
* **R** (IRkernel)
* **Julia**
* **Scala**, **Java**, **C++**, and many others

Any language kernel that produces standard ``.ipynb`` files with ``execution_count`` metadata
is supported. The tool is completely language-agnostic and only inspects the notebook's
execution order metadata.

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

If no paths are specified, ``nbcheck`` will check all notebooks in the current directory.

You can also use the full ``enforce-notebook-run-order`` command, but the ``nbcheck`` command is
provided as a convenience.

pre-commit hook
^^^^^^^^^^^^^^^

To use ``enforce_notebook_run_order`` as a pre-commit hook, add the following to your ``.pre-commit-config.yaml``:

.. code-block:: yaml

    repos:
    -   repo: https://github.com/cmhac/enforce-notebook-run-order
        rev: <replace with latest version from https://github.com/cmhac/enforce-notebook-run-order/releases/>
        hooks:
        -   id: enforce-notebook-run-order

Limitations
^^^^^^^^^^^

``enforce-notebook-run-order`` now focuses solely on verifying that non-empty code cells were
executed sequentially according to their ``execution_count`` values.

* Does not execute notebooks; it only inspects existing metadata.
* Ignores markdown and raw cells.
* Empty code cells are ignored.
* A non-empty code cell with ``execution_count`` set to ``None`` fails the check.
* Does not validate or compare cell outputs.
* Manual editing of ``execution_count`` values can circumvent checks.

Exit Codes
^^^^^^^^^^

* Exit code ``0``: All notebooks passed run-order validation.
* Exit code ``1``: At least one notebook failed; execution stops at first failure.

Use these exit codes in CI to enforce reproducible, sequentially executed notebooks.
