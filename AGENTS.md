# AGENTS.md

## Project Overview

`enforce-notebook-run-order` is a Python tool that validates Jupyter notebooks were executed sequentially from top to bottom. It prevents notebooks from being committed in a state where cells were run out of order, ensuring reproducibility for collaborators.

The tool can be used as a standalone CLI (`nbcheck`) or as a pre-commit hook.

## Setup Commands

- Install dependencies: `poetry install`
- Run tests: `poetry run pytest`
- Run tests with coverage: `poetry run pytest --cov=enforce_notebook_run_order --cov-report=html`
- Run linter: `poetry run pylint enforce_notebook_run_order`
- Format code: `poetry run black enforce_notebook_run_order`
- Build documentation: `cd docs && make html`

## Testing Instructions

- Tests are located in the `test/` directory
- Test data (sample notebooks) is in `test/test_data/`
- Run all tests before committing: `poetry run pytest`
- CI runs automatically on pull requests via GitHub Actions (`.github/workflows/test.yaml`)
- Aim for maintaining test coverage above current levels (check codecov badge)

## Code Style

- Python 3.9+ required
- Use Black for code formatting
- Follow pylint conventions
- Type hints encouraged but not strictly enforced
- Keep functions focused and well-documented with docstrings

## Project Structure

- `enforce_notebook_run_order/`: Main package
  - `enforce_notebook_run_order.py`: Core validation logic
  - `cli.py`: Command-line interface (Click-based)
  - `utils.py`: Helper functions for notebook parsing
- `test/`: Unit tests using pytest
- `docs/`: Sphinx documentation

## Key Functions

- `check_notebook_run_order()`: Validates cell execution order
- `check_single_notebook()`: Processes a single notebook file
- `process_path()`: Handles files or directories recursively
- CLI entry points: `enforce-notebook-run-order` and `nbcheck` (both equivalent)

## Common Development Tasks

- To test the CLI locally: `poetry run nbcheck <path_to_notebook>`
- To add a new feature, update tests first (TDD approach)
- Documentation updates require rebuilding with `make html` in `docs/`
- Version bumps happen in `pyproject.toml` and trigger auto-tagging via GitHub Actions
