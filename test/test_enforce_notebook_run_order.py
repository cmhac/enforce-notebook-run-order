"""tests the enforce_notebook_run_order module"""

import os
from click.testing import CliRunner
import pytest
import enforce_notebook_run_order
from enforce_notebook_run_order import (
    InvalidNotebookRunError,
    NotebookCodeCellNotRunError,
    NotebookRunOrderError,
)

# pylint: disable=redefined-outer-name


@pytest.fixture
def valid_notebook_data():
    """Returns valid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 2},
            {"cell_type": "code", "execution_count": 3},
        ]
    }


@pytest.fixture
def out_of_order_notebook_data():
    """Returns invalid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 3},
            {"cell_type": "code", "execution_count": 2},
        ]
    }


@pytest.fixture
def notebook_cell_not_run_data():
    """Returns invalid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 2},
            {"cell_type": "code", "execution_count": None},
        ]
    }


def test_check_notebook_run_order_valid(valid_notebook_data):
    """Tests that valid notebook data does not raise an error."""
    enforce_notebook_run_order.check_notebook_run_order(valid_notebook_data)


def test_check_notebook_run_order_out_of_order(out_of_order_notebook_data):
    """Tests that out of order notebook data raises an error."""
    with pytest.raises(NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(out_of_order_notebook_data)

    expected_error_message = (
        "Cells were not run sequentially. "
        "The cell that caused this error is #3 "
        "and the previous cell was #1. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': 3}"
    )
    assert str(error.value) == expected_error_message


def test_check_notebook_run_order_cell_not_run(notebook_cell_not_run_data):
    """Tests that a notebook cell not run raises an error."""
    with pytest.raises(NotebookCodeCellNotRunError) as error:
        enforce_notebook_run_order.check_notebook_run_order(notebook_cell_not_run_data)

    expected_error_message = (
        "Code cell was not run. The previous cell was #2. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': None}"
    )
    assert str(error.value) == expected_error_message


def test_notebook_is_in_virtualenv():
    """Tests that notebook_is_in_virtualenv returns True when in a virtualenv."""
    assert enforce_notebook_run_order.notebook_is_in_virtualenv(
        ".venv/lib/python3.8/site-packages/nbclient/tests/files/Empty Cell.ipynb"
    )
    assert not enforce_notebook_run_order.notebook_is_in_virtualenv(
        "notebooks/Empty Cell.ipynb"
    )


def test_check_all_repo_notebooks_valid(mocker):
    """
    Tests that check_notebook_run_order is called correctly
    for each notebook in a given folder.
    """
    mock_check_notebook_run_order = mocker.patch(
        "enforce_notebook_run_order.check_notebook_run_order"
    )

    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_valid"
    )

    enforce_notebook_run_order.check_all_repo_notebooks(test_data_dir)

    assert mock_check_notebook_run_order.call_count == 2


def test_check_all_repo_notebooks_invalid():
    """
    Tests that check_notebook_run_order raises InvalidNotebookRunError
    for each notebook in a given folder.
    """
    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_invalid"
    )

    with pytest.raises(InvalidNotebookRunError):
        enforce_notebook_run_order.check_all_repo_notebooks(test_data_dir)


def test_check_all_repo_notebooks_ignores_virtualenv(mocker):
    """
    Tests that check_notebook_run_order is not called for notebooks
    in a virtualenv.
    """
    mock_check_notebook_run_order = mocker.patch(
        "enforce_notebook_run_order.check_notebook_run_order"
    )

    test_data_dir = os.path.join(
        "test",
        "test_data",
        "test_virtual_environment",
        "test_lib",
        "python3.x",
        "site-packages",
        "testpackage",
        "tests",
        "test_data",
    )

    enforce_notebook_run_order.check_all_repo_notebooks(test_data_dir)

    assert mock_check_notebook_run_order.call_count == 0


def test_cli_invalid_notebook_path():
    """Tests that the CLI raises an error when given a file that is not an ipynb."""
    runner = CliRunner()
    result = runner.invoke(enforce_notebook_run_order.cli, ["--path", "python.py"])
    assert result.exit_code == 1
    assert "Must be a path to a notebook file with the .ipynb extension" in str(
        result.exc_info[1]
    )


def test_cli_valid_notebook_path_valid_notebook():
    """Tests that the CLI returns 0 when given a valid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        enforce_notebook_run_order.cli,
        [
            "--path",
            "test/test_data/enforce_notebook_run_order_valid/valid_notebook.ipynb",
        ],
    )
    assert result.exit_code == 0


def test_cli_valid_notebook_path_invalid_notebook():
    """Tests that the CLI returns 1 when given an invalid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        enforce_notebook_run_order.cli,
        [
            "--path",
            "test/test_data/enforce_notebook_run_order_invalid/test_subdirectory/"
            "valid_subdirectory_notebook.ipynb",
        ],
    )
    assert result.exit_code == 1


def test_cli_valid_notebook_dir_valid_notebooks():
    """Tests that the CLI returns 0 when given a valid notebook_dir."""
    runner = CliRunner()
    result = runner.invoke(
        enforce_notebook_run_order.cli,
        [
            "--path",
            "test/test_data/enforce_notebook_run_order_valid",
        ],
    )
    assert result.exit_code == 0
