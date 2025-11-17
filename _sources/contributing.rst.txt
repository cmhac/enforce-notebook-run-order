Contributing to enforce-notebook-run-order
===========================================

Thank you for your interest in contributing! This document provides an overview of the project's infrastructure, CI/CD workflows, and development guidelines.

Development Setup
-----------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.9 or higher
- Poetry 1.4 or higher

Installation
~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/cmhac/enforce-notebook-run-order.git
      cd enforce-notebook-run-order

2. Install dependencies:

   .. code-block:: bash

      poetry install --with dev

3. Run tests to verify setup:

   .. code-block:: bash

      poetry run pytest

CI/CD Workflow Overview
-----------------------

The project uses GitHub Actions with a multi-stage automated workflow triggered by pull requests and merges to the ``main`` branch.

Workflow Stages
~~~~~~~~~~~~~~~

::

   Pull Request → Test → Merge → Auto-Tag → Publish & Docs

1. Test Stage (``.github/workflows/test.yaml``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Trigger**: Automatically runs on all pull requests targeting the ``main`` branch.

**Purpose**: Validates code quality and functionality across multiple Python versions.

**Steps**:

- **Linting**: Runs ``pylint`` on all Python files
- **Testing**: Executes the full test suite with ``pytest``
- **Coverage**: Generates coverage reports and uploads to Codecov

**Python Version Matrix**:
The test workflow runs against Python version 3.9-3.14. As more `versions enter bugfix/security stages of their lifecycle <https://devguide.python.org/versions/>`_, we should continue to add those to the matrix and to the required status checks (see `Branch Protection Rules`_ below for details.)

**Key Configuration**:

.. code-block:: yaml

   strategy:
     fail-fast: false
     matrix:
       python-version: ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]

The ``fail-fast: false`` setting ensures all Python versions are tested even if one fails, providing complete visibility into compatibility issues.

2. Auto-Tag Stage (``.github/workflows/auto-tag.yml``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Trigger**: Runs when a pull request is merged into ``main``.

**Purpose**: Automatically creates Git tags based on version changes in ``pyproject.toml``.

**Process**:

1. Extracts the current version from ``pyproject.toml`` using ``poetry version -s``
2. Checks if a tag for that version already exists
3. If new version detected, creates and pushes a Git tag
4. Skips if version hasn't changed

This automation eliminates manual tagging and ensures releases are properly versioned.

3. Publish Stage (``.github/workflows/publish-pypi.yaml``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Trigger**: Runs after successful completion of the ``auto-tag`` workflow.

**Purpose**: Builds and publishes the package to PyPI.

**Steps**:

1. Runs linting checks (``pylint``)
2. Builds distribution packages with ``poetry build``
3. Determines the latest Git tag
4. Creates a GitHub release with distribution artifacts
5. Publishes to PyPI using the ``PYPI_API_TOKEN`` secret

**Note**: Uses Python 3.12 for building and publishing.

4. Documentation Stage (``.github/workflows/docs.yml``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Trigger**: Runs after successful completion of the ``auto-tag`` workflow (in parallel with publish).

**Purpose**: Builds and deploys Sphinx documentation to GitHub Pages.

**Steps**:

1. Installs dependencies with ``poetry install --with dev``
2. Builds documentation with ``sphinx-build docs _build``
3. Deploys to the ``gh-pages`` branch
4. Uses ``force_orphan: true`` to keep the branch clean

**Note**: Uses Python 3.12 for building documentation.

Documentation
-------------

Writing Documentation
~~~~~~~~~~~~~~~~~~~~~

Documentation is written in reStructuredText (``.rst``) format and built with Sphinx.

**Location**: All documentation source files are in the ``docs/`` directory:

- ``docs/index.rst`` - Main documentation index
- ``docs/cli.rst`` - CLI reference
- ``docs/python_api.rst`` - Python API documentation
- ``docs/README.rst`` - User guide
- ``docs/GITHUB_README.rst`` - GitHub README mirror
- ``docs/contributing.rst`` - This contributor guide

Building Documentation Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build and view documentation on your machine:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in ``docs/_build/html/``. Open ``docs/_build/html/index.html`` in a browser to view.

**Alternatively**, build from the project root:

.. code-block:: bash

   poetry run sphinx-build docs _build

Documentation Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation-related dependencies are included in the ``dev`` group in ``pyproject.toml``:

- ``Sphinx`` - Documentation generator
- ``sphinx-click`` - Automatic CLI documentation from Click
- ``recommonmark`` - Markdown support in Sphinx
- ``pydata-sphinx-theme`` - Modern documentation theme

Auto-Generated Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **CLI documentation** is automatically generated from the Click CLI definitions in ``enforce_notebook_run_order/cli.py``
- **API documentation** uses Sphinx autodoc to extract docstrings from the Python code

Branch Protection Rules
-----------------------

The repository uses GitHub branch protection rules (Rulesets) to maintain code quality and enforce workflow requirements on the ``main`` branch.

Active Ruleset: "Main"
~~~~~~~~~~~~~~~~~~~~~~

**Target Branch**: ``main`` (default branch)

**Enforcement Status**: ✅ Active

Enabled Rules
~~~~~~~~~~~~~

🔒 Restrict deletions
^^^^^^^^^^^^^^^^^^^^^^

Only users with bypass permissions can delete the ``main`` branch, preventing accidental deletion of the primary branch.

🔀 Require a pull request before merging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All commits must be made to a non-target branch and submitted via pull request. Direct pushes to ``main`` are blocked.

✅ Require status checks to pass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All required CI checks must pass before a pull request can be merged.

**Required Status Checks**:

- ``test (3.9, 1.4)`` - Python 3.9
- ``test (3.10, 1.4)`` - Python 3.10
- ``test (3.11, 1.4)`` - Python 3.11
- ``test (3.12, 1.4)`` - Python 3.12
- ``test (3.13, 1.4)`` - Python 3.13
- ``test (3.14, 1.4)`` - Python 3.14

**All six Python versions must pass** before a PR can be merged. This ensures compatibility across the full supported version range.

🚫 Block force pushes
^^^^^^^^^^^^^^^^^^^^^^

Force pushes to the ``main`` branch are prevented to preserve history and prevent accidental overwrites.

Bypass List
~~~~~~~~~~~

The bypass list is currently empty, meaning all contributors (including repository administrators) must follow the same rules.

Development Workflow
--------------------

Making Changes
~~~~~~~~~~~~~~

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature-name

2. **Make your changes** and ensure they follow the code style:

   .. code-block:: bash

      poetry run black enforce_notebook_run_order
      poetry run pylint enforce_notebook_run_order

3. **Write or update tests** for your changes in the ``test/`` directory

4. **Run the test suite**:

   .. code-block:: bash

      poetry run pytest

5. **Check test coverage**:

   .. code-block:: bash

      poetry run pytest --cov=enforce_notebook_run_order --cov-report=html

   Open ``htmlcov/index.html`` to view detailed coverage report.

Submitting a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Push your branch** to GitHub:

   .. code-block:: bash

      git push origin feature-name

2. **Create a pull request** targeting the ``main`` branch

3. **Wait for CI checks**: All 6 Python version tests must pass

4. **Address review feedback** if requested

5. **Merge**: Once approved and all checks pass, the PR can be merged

After Merging
~~~~~~~~~~~~~

After your PR is merged to ``main``:

1. **Auto-tag** workflow checks if the version in ``pyproject.toml`` changed
2. If version changed, a new Git tag is created
3. **Publish** workflow automatically releases to PyPI
4. **Docs** workflow rebuilds and deploys documentation to GitHub Pages

**Important**: To trigger a release, update the version in ``pyproject.toml``:

.. code-block:: bash

   poetry version patch  # or minor, major
   git add pyproject.toml
   git commit -m "Bump version to $(poetry version -s)"

Code Style Guidelines
---------------------

- **Formatting**: Use Black for code formatting (``poetry run black .``)
- **Linting**: Code must pass pylint checks (``poetry run pylint enforce_notebook_run_order``)
- **Type hints**: Encouraged but not strictly enforced
- **Docstrings**: Required for all public functions, classes, and modules
- **Python version**: Code must be compatible with Python 3.9+

Testing Guidelines
------------------

- **Location**: All tests in ``test/`` directory
- **Framework**: pytest with pytest-mock and pytest-cov
- **Test data**: Sample notebooks in ``test/test_data/notebooks/``
- **Coverage**: Maintain or improve existing coverage (check Codecov badge)
- **Test types**:
  
  - Unit tests for core logic (``test_enforce_notebook_run_order.py``)
  - CLI tests (``test_cli.py``)
  - Multi-language notebook tests (``test_multi_language_notebooks.py``)
  - Utility function tests (``test_utils.py``)

Running Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run a specific test file
   poetry run pytest test/test_cli.py

   # Run a specific test function
   poetry run pytest test/test_cli.py::test_cli_single_valid_notebook

   # Run with verbose output
   poetry run pytest -v

   # Run with coverage report
   poetry run pytest --cov=enforce_notebook_run_order --cov-report=term

Questions or Issues?
--------------------

If you have questions about contributing or encounter issues with the development setup, please:

1. Check existing `GitHub Issues <https://github.com/cmhac/enforce-notebook-run-order/issues>`_
2. Review the `documentation <https://cmhac.github.io/enforce-notebook-run-order/>`_
3. Open a new issue with details about your question or problem

Thank you for contributing to enforce-notebook-run-order!
