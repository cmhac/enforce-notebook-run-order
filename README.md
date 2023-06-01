enforce-notebook-run-order
==========================

A tiny python script to enforce the run order of a Jupyter notebook.

Jupyter notebooks are great for interactive data analysis. However, when
they can encourage a bad habit: running cells out of order. This can
lead to notebooks being committed to the repository in a state where
they don\'t run from top to bottom, and other collaborators may receive
different results when running the notebook from top to bottom.

This script enforces the run order of a notebook by raising an exception
if any cells are run out of order.

Usage
-----

This script can be used as a standalone script, or as a pre-commit hook.

### Standalone

To use `enforce-notebook-run-order` as a standalone script, simply run
it with the path to the notebook you want to check:

`enforce-notebook-run-order my_notebook.ipynb`

Or point it to a directory to check all notebooks in that directory:

`enforce-notebook-run-order my_notebooks/`

### Pre-commit hook

To use `enforce_notebook_run_order` as a pre-commit hook, add the
following to your `.pre-commit-config.yaml`:
