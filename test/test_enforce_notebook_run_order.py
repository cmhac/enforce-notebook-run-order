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


def test_cli():
    """Tests that the CLI command runs successfully."""
    runner = CliRunner()
    result = runner.invoke(
        enforce_notebook_run_order.cli,
        ["--notebook-dir", "test/test_data/enforce_notebook_run_order_valid"],
    )

    # Check if the CLI command was invoked successfully
    assert result.exit_code == 0
