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
        "and the previous cell was #1.\n\n"
        "To fix this, restart the notebook kernel and run all cells sequentially."
    )
    assert str(error.value) == expected_error_message


def test_check_notebook_run_order_cell_not_run(notebook_cell_not_run_data):
    """Tests that a notebook cell not run raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookCodeCellNotRunError) as error:
        enforce_notebook_run_order.check_notebook_run_order(notebook_cell_not_run_data)

    expected_error_message = (
        "Code cell was not run. The previous cell was #2.\n\n"
        "To fix this, restart the notebook kernel and run all cells sequentially."
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
        "test", "test_data", "notebooks", "nested_subdirectory_structure"
    )

    enforce_notebook_run_order.process_path(test_data_dir)

    # Should find 3 notebooks: 1 at level1/ and 2 at level1/level2/
    assert mock_check_single_notebook.call_count == 3
    # Verify that all three notebook paths were checked
    called_paths = [call[0][0] for call in mock_check_single_notebook.call_args_list]
    assert any("valid_level1_notebook.ipynb" in path for path in called_paths)
    assert any("valid_nested_notebook.ipynb" in path for path in called_paths)
    assert any("invalid_nested_notebook.ipynb" in path for path in called_paths)


def test_process_path_directory_raises_error_when_notebooks_invalid():
    """
    Tests that check_notebook_run_order raises InvalidNotebookRunError
    for notebooks in nested subdirectories.
    """
    test_data_dir = os.path.join(
        "test", "test_data", "notebooks", "nested_subdirectory_structure"
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
        "test", "test_data", "notebooks", "python", "valid", "valid_notebook.ipynb"
    )

    enforce_notebook_run_order.process_path(notebook_path)

    mock_check_single_notebook.assert_called_once_with(notebook_path)


def test_check_notebook_run_order_starts_from_zero(notebook_data_starts_from_zero):
    """Tests that a notebook starting from execution_count 0 raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(
            notebook_data_starts_from_zero
        )

    assert "Cells were not run sequentially" in str(error.value)
    assert "The cell that caused this error is #0" in str(error.value)


def test_check_notebook_run_order_starts_from_two(notebook_data_starts_from_two):
    """Tests that a notebook starting from execution_count 2 raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(
            notebook_data_starts_from_two
        )

    assert "Cells were not run sequentially" in str(error.value)
    assert "The cell that caused this error is #2" in str(error.value)
    assert "the previous cell was #0" in str(error.value)


def test_check_notebook_run_order_with_gap(notebook_data_with_gap):
    """Tests that a notebook with a gap in execution sequence raises an error."""
    with pytest.raises(enforce_notebook_run_order.NotebookRunOrderError) as error:
        enforce_notebook_run_order.check_notebook_run_order(notebook_data_with_gap)

    assert "Cells were not run sequentially" in str(error.value)
    assert "The cell that caused this error is #4" in str(error.value)
    assert "the previous cell was #2" in str(error.value)
