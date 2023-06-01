enforce-notebook-run-order
==========================

A tiny python script to enforce the run order of a Jupyter notebook.

Jupyter notebooks are great for interactive data analysis. However, when
they can encourage a bad habit: running cells out of order. This can lead
to notebooks being committed to the repository in a state where they don't run
from top to bottom, and other collaborators may receive different results
when running the notebook from top to bottom.

This script enforces the run order of a notebook by raising an exception if
any cells are run out of order.