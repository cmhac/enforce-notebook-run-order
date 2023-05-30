"""tests the enforce_run_order script"""

import os
from unittest.mock import patch
import pytest
import enforce_notebook_run_order

# pylint: disable=W0621:redefined-outer-name


@pytest.fixture
def valid_notebook_data():
    """returns valid test notebook json"""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 2},
            {"cell_type": "code", "execution_count": 3},
        ]
    }


@pytest.fixture
def out_of_order_notebook_data():
    """returns invalid test notebook json"""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 3},
            {"cell_type": "code", "execution_count": 2},
        ]
    }


@pytest.fixture
def notebook_cell_not_run_data():
    """returns invalid test notebook json"""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1},
            {"cell_type": "code", "execution_count": 2},
            {"cell_type": "code", "execution_count": None},
        ]
    }


def test_check_notebook_run_order_valid(valid_notebook_data):
    """tests that valid notebook data does not raise an error"""
    try:
        enforce_notebook_run_order.check_notebook_run_order(valid_notebook_data)
    except (
        enforce_notebook_run_order.NotebookCodeCellNotRunError,
        enforce_notebook_run_order.NotebookRunOrderError,
    ):
        pytest.fail("Valid notebook data raised error unexpectedly")


def test_check_notebook_run_order_out_of_order(out_of_order_notebook_data):
    """tests that out of order notebook data raises an error"""
    with pytest.raises(enforce_notebook_run_order.NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(out_of_order_notebook_data)

    expected_error_message = (
        "Cells were not run sequentially. "
        "The cell that caused this error is #3 "
        "and the previous cell was #1. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': 3}"
    )
    assert str(error.value) == expected_error_message


def test_notebook_cell_not_run(notebook_cell_not_run_data):
    """tests that a notebook cell not run raises an error"""
    with pytest.raises(enforce_notebook_run_order.NotebookCodeCellNotRunError) as error:
        enforce_notebook_run_order.check_notebook_run_order(notebook_cell_not_run_data)

    expected_error_message = (
        "Code cell was not run. The previous cell was #2. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': None}"
    )
    assert str(error.value) == expected_error_message


def test_check_all_repo_notebooks(mocker):
    """
    tests that check_notebook_run_order is called correctly
    for each notebook in a given folder
    """
    mock_check_notebook_run_order = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_notebook_run_order"
    )
    test_data_dir = os.path.join("test", "test_data", "enforce_notebook_run_order")
    enforce_notebook_run_order.check_all_repo_notebooks(test_data_dir)

    # check that the function was called 2 times
    assert mock_check_notebook_run_order.call_count == 2
