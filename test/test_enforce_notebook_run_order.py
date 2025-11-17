"""tests the enforce_notebook_run_order module"""

import os
import pytest
from enforce_notebook_run_order import enforce_notebook_run_order


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


def test_process_path_directory_with_notebooks(mocker):
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


def test_process_path_directory_raises_error_when_notebooks_invalid():
    """
    Tests that check_notebook_run_order raises InvalidNotebookRunError
    for each notebook in a given folder.
    """
    test_data_dir = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_invalid"
    )

    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError):
        enforce_notebook_run_order.process_path(test_data_dir)


def test_process_path_raises_error_for_non_ipynb_file():
    """Tests that process_path raises an error when given a file that is not an ipynb."""
    with pytest.raises(ValueError):
        enforce_notebook_run_order.process_path("test/test_data/invalid_notebook.py")


def test_process_path_single_notebook_file(mocker):
    """Tests that process_path delegates correctly when given a single notebook file."""
    mock_check_single_notebook = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_single_notebook"
    )

    notebook_path = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_valid", "valid_notebook.ipynb"
    )

    enforce_notebook_run_order.process_path(notebook_path)

    mock_check_single_notebook.assert_called_once_with(notebook_path)
