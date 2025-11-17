"""tests the enforce_notebook_run_order module"""

import os
from click.testing import CliRunner
import pytest
from enforce_notebook_run_order import enforce_notebook_run_order
from enforce_notebook_run_order.cli import cli

# pylint: disable=redefined-outer-name


@pytest.fixture
def valid_notebook_data():
    """Returns valid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 3, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def out_of_order_notebook_data():
    """Returns invalid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 3, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def notebook_cell_not_run_data():
    """Returns invalid test notebook json."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": 2, "source": ["print('foo')"]},
            {"cell_type": "code", "execution_count": None, "source": ["print('foo')"]},
        ]
    }


@pytest.fixture
def empty_notebook_cells():
    """Returns empty notebook cells."""
    return {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": []},
            {"cell_type": "code", "execution_count": None, "source": []},
            {"cell_type": "code", "execution_count": None, "source": []},
        ]
    }


def test_check_notebook_run_order_valid(valid_notebook_data):
    """Tests that valid notebook data does not raise an error."""
    enforce_notebook_run_order.check_notebook_run_order(valid_notebook_data)


def test_check_notebook_run_order_out_of_order(out_of_order_notebook_data):
    """Tests that out of order notebook data raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(out_of_order_notebook_data)

    expected_error_message = (
        "Cells were not run sequentially. "
        "The cell that caused this error is #3 "
        "and the previous cell was #1. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': 3, "
        "'source': [\"print('foo')\"]}"
    )
    assert str(error.value) == expected_error_message


def test_check_notebook_run_order_cell_not_run(notebook_cell_not_run_data):
    """Tests that a notebook cell not run raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookCodeCellNotRunError) as error:
        enforce_notebook_run_order.check_notebook_run_order(notebook_cell_not_run_data)

    expected_error_message = (
        "Code cell was not run. The previous cell was #2. \n\n"
        "Cell contents: \n\n> {'cell_type': 'code', 'execution_count': None, "
        "'source': [\"print('foo')\"]}"
    )
    assert str(error.value) == expected_error_message


def test_check_notebook_run_order_empty_cells(empty_notebook_cells):
    """Tests that empty notebook cells do not raise an error."""
    enforce_notebook_run_order.check_notebook_run_order(empty_notebook_cells)


def test_process_path_valid(mocker):
    """
    Tests that check_single_notebook is called correctly
    for each notebook in a given folder, including nested subdirectories.
    """
    mock_check_single_notebook = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_single_notebook"
    )

    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_valid"
    )

    enforce_notebook_run_order.process_path(test_data_dir)

    # Should find 2 notebooks: one in the root and one in test_subdirectory
    assert mock_check_single_notebook.call_count == 2
    # Verify that both notebook paths were checked
    called_paths = [call[0][0] for call in mock_check_single_notebook.call_args_list]
    assert any("valid_notebook.ipynb" in path for path in called_paths)
    assert any("valid_subdirectory_notebook.ipynb" in path for path in called_paths)


def test_process_path_invalid():
    """
    Tests that check_notebook_run_order raises InvalidNotebookRunError
    for each notebook in a given folder.
    """
    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_invalid"
    )

    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError):
        enforce_notebook_run_order.process_path(test_data_dir)


def test_process_path_invalid_notebook_path():
    """Tests that the CLI raises an error when given a file that is not an ipynb."""
    with pytest.raises(ValueError):
        enforce_notebook_run_order.process_path("test/test_data/invalid_notebook.py")


def test_cli_valid_notebook_path_valid_notebook():
    """Tests that the CLI returns 0 when given a valid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/enforce_notebook_run_order_valid/valid_notebook.ipynb",
        ],
    )
    assert result.exit_code == 0


def test_cli_valid_notebook_path_invalid_notebook():
    """Tests that the CLI returns 1 when given an invalid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/enforce_notebook_run_order_invalid/test_subdirectory/"
            "invalid_subdirectory_notebook.ipynb",
        ],
    )
    assert result.exit_code == 1


def test_cli_valid_notebook_dir_valid_notebooks():
    """Tests that the CLI returns 0 when given a valid notebook_dir."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/enforce_notebook_run_order_valid",
        ],
    )
    assert result.exit_code == 0


def test_cli_no_paths_searches_entire_dir(mocker):
    """
    Tests that the CLI searches the entire current directory if no paths are specified.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    runner = CliRunner()
    result = runner.invoke(cli)

    # The process_path function should be called once, with the current directory as its argument
    mock_process_path.assert_called_once_with(".")

    assert result.exit_code == 0


def test_cli_no_paths_process_path_called_with_dot_argument(mocker):
    """
    Tests that process_path is called with "." when no paths are specified.
    This verifies the recursion starts from the current directory.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    # Verify process_path was called exactly once with "."
    mock_process_path.assert_called_once()
    args, _ = mock_process_path.call_args
    assert args[0] == "."
    assert result.exit_code == 0


def test_cli_with_multiple_paths_calls_process_path_for_each(mocker):
    """
    Tests that process_path is called for each path argument provided.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    test_path_1 = "test/test_data/enforce_notebook_run_order_valid"
    test_path_2 = "test/test_data/enforce_notebook_run_order_invalid"

    runner = CliRunner()
    result = runner.invoke(cli, [test_path_1, test_path_2])

    # Verify process_path was called twice, once for each path
    assert mock_process_path.call_count == 2
    calls = [call[0][0] for call in mock_process_path.call_args_list]
    assert test_path_1 in calls
    assert test_path_2 in calls
    assert result.exit_code == 0


def test_process_path_recursively_scans_nested_directories(mocker):
    """
    Tests that process_path recursively scans nested directories and finds
    all notebooks at multiple levels of nesting.
    """
    mock_check_single_notebook = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_single_notebook"
    )

    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_valid"
    )

    enforce_notebook_run_order.process_path(test_data_dir)

    # Should be called for each notebook found recursively
    assert mock_check_single_notebook.call_count == 2
    called_notebook_paths = [
        call[0][0] for call in mock_check_single_notebook.call_args_list
    ]

    # Verify both the root-level and nested notebook were found
    assert any("valid_notebook.ipynb" in path for path in called_notebook_paths)
    assert any(
        "test_subdirectory" in path and "valid_subdirectory_notebook.ipynb" in path
        for path in called_notebook_paths
    )


def test_cli_no_paths_delegates_to_process_path_with_current_dir(mocker):
    """
    Tests that calling CLI with no paths delegates to process_path with
    the current directory, enabling recursive scanning from root.
    """
    mock_load_notebook_data = mocker.patch(
        "enforce_notebook_run_order.utils.load_notebook_data"
    )
    mock_check_notebook_run_order = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_notebook_run_order"
    )

    # Return valid notebook data so process_path succeeds
    mock_load_notebook_data.return_value = {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]}
        ]
    }

    runner = CliRunner()
    result = runner.invoke(cli, [])

    # Verify the chain of calls demonstrates recursion from current directory
    assert result.exit_code == 0
    # Both check_notebook_run_order was called (proving notebooks were processed)
    # and the process started from "." (which os.walk would handle recursively)
    assert mock_check_notebook_run_order.called
