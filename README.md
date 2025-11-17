<p align="left">
 <a href="https://badge.fury.io/py/enforce-notebook-run-order">
   <img src="https://badge.fury.io/py/enforce-notebook-run-order@2x.png" alt="PyPI version" height="20">
 </a>
 <a href="https://codecov.io/gh/christopher-hacker/enforce-notebook-run-order" > 
   <img src="https://codecov.io/gh/christopher-hacker/enforce-notebook-run-order/branch/main/graph/badge.svg?token=019MXVQYN5"/> 
 </a>
  <a href="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/test.yaml">
    <img src="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/test.yaml/badge.svg" alt="Run tests">
  </a>
  <a href="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/publish-pypi.yaml">
    <img src="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/publish-pypi.yaml/badge.svg" alt="Publish to PyPi">
  </a>
  <a href="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/docs.yml">
   <img src="https://github.com/christopher-hacker/enforce-notebook-run-order/actions/workflows/docs.yml/badge.svg" alt="Build docs">
  </a>
</p>

# enforce-notebook-run-order

Enforce the run order of Jupyter notebooks.

Jupyter notebooks are great for interactive data analysis. However, they
can encourage a bad habit: running cells out of order. This can lead to
notebooks being committed to the repository in a state where they don\'t
run from top to bottom, and other collaborators may receive different
results when trying to reproduce the analysis.

`enforce-notebook-run-order` attempts to fix this by raising an
exception before each commit if any cells are run out of order.

## Language Support

This tool works with **all Jupyter notebook kernels**, including:

- **Python** (IPython)
- **R** (IRkernel)
- **Julia**
- **Scala**, **Java**, **C++**, and many others

Any language kernel that produces standard `.ipynb` files with
`execution_count` metadata is supported. The tool is language-agnostic
and only inspects the notebook\'s execution order metadata.

## Validation Requirements

For a notebook to be considered valid, it must meet the following
requirements:

- **All non-empty code cells must be executed**: Each code cell with
  content must have an `execution_count` value (not `None`).
- **Execution must start from 1**: The first non-empty code cell must
  have `execution_count=1`.
- **No gaps in execution sequence**: Execution counts must be strictly
  sequential (1, 2, 3, \...) with no skipped numbers.

**Examples:**

- ✅ **Valid**: Cells with execution counts `1, 2, 3, 4`
- ❌ **Invalid**: Cells starting with `0, 1, 2` (must start from 1)
- ❌ **Invalid**: Cells starting with `2, 3, 4` (must start from 1)
- ❌ **Invalid**: Cells with `1, 2, 4, 5` (gap at 3)
- ❌ **Invalid**: Cells with `1, 3, 2` (not sequential)
- ❌ **Invalid**: Cells with `1, 2, None` (unexecuted cell)

**Note**: Empty code cells (cells with no content) are ignored and do
not need to be executed.

## Usage

`enforce-notebook-run-order` is designed to work primarily as a
[pre-commit hook](https://pre-commit.com/), but can also be used as a
standalone script when needed.

### pre-commit hook (Recommended)

The intended way to use `enforce-notebook-run-order` is as a pre-commit
hook to automatically validate notebook execution order before each
commit.

To set it up, add the following to your `.pre-commit-config.yaml`:

``` yaml
repos:
-   repo: https://github.com/cmhac/enforce-notebook-run-order
    rev: <replace with latest version from https://github.com/cmhac/enforce-notebook-run-order/releases/>
    hooks:
    -   id: enforce-notebook-run-order
```

This will automatically check all notebooks in your repository before
each commit, preventing out-of-order execution from being committed to
your repository.

### Standalone

For manual validation or CI integration, `enforce-notebook-run-order`
can be used as a standalone script.

First, install it the same way you install other Python packages, such
as:

``` bash
pip install enforce-notebook-run-order
```

Run it with the path to the notebook(s) you want to check:

``` bash
nbcheck my_notebook.ipynb my_other_notebook.ipynb
```

Or point it to a directory to check all notebooks in that directory:

``` bash
nbcheck my_notebooks/
```

If no paths are specified, `nbcheck` will check all notebooks in the
current directory.

You can also use the full `enforce-notebook-run-order` command, but the
`nbcheck` command is provided as a convenience.
