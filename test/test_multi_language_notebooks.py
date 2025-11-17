"""Integration tests for non-Python Jupyter notebooks (R, Julia, etc.)"""

import os
import pytest
from enforce_notebook_run_order import enforce_notebook_run_order, utils


def test_valid_r_notebook():
    """Tests that a valid R notebook passes validation."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "r", "valid", "valid_r_notebook.ipynb"
    )

    # Should not raise any exception
    enforce_notebook_run_order.check_single_notebook(notebook_path)


def test_invalid_r_notebook():
    """Tests that an invalid R notebook (out of order) fails validation."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "r", "invalid", "invalid_r_notebook.ipynb"
    )

    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError) as error:
        enforce_notebook_run_order.check_single_notebook(notebook_path)

    # Verify the error message mentions the out-of-order execution
    assert "not run in order" in str(error.value).lower()


def test_valid_julia_notebook():
    """Tests that a valid Julia notebook passes validation."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "julia", "valid", "valid_julia_notebook.ipynb"
    )

    # Should not raise any exception
    enforce_notebook_run_order.check_single_notebook(notebook_path)


def test_invalid_julia_notebook():
    """Tests that an invalid Julia notebook (out of order) fails validation."""
    notebook_path = os.path.join(
        "test",
        "test_data",
        "notebooks",
        "julia",
        "invalid",
        "invalid_julia_notebook.ipynb",
    )

    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError) as error:
        enforce_notebook_run_order.check_single_notebook(notebook_path)

    # Verify the error message mentions the out-of-order execution
    assert "not run in order" in str(error.value).lower()


def test_r_notebook_has_correct_kernel_metadata():
    """Tests that R notebook metadata is correctly preserved."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "r", "valid", "valid_r_notebook.ipynb"
    )
    notebook_data = utils.load_notebook_data(notebook_path)

    # Verify it has R kernel metadata
    assert "metadata" in notebook_data
    assert "kernelspec" in notebook_data["metadata"]
    assert notebook_data["metadata"]["kernelspec"]["language"] == "R"
    assert notebook_data["metadata"]["kernelspec"]["name"] == "ir"


def test_julia_notebook_has_correct_kernel_metadata():
    """Tests that Julia notebook metadata is correctly preserved."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "julia", "valid", "valid_julia_notebook.ipynb"
    )
    notebook_data = utils.load_notebook_data(notebook_path)

    # Verify it has Julia kernel metadata
    assert "metadata" in notebook_data
    assert "kernelspec" in notebook_data["metadata"]
    assert notebook_data["metadata"]["kernelspec"]["language"] == "julia"
    assert notebook_data["metadata"]["kernelspec"]["name"] == "julia-1.6"


def test_r_notebook_code_cells_extracted_correctly():
    """Tests that code cells are correctly extracted from R notebooks."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "r", "valid", "valid_r_notebook.ipynb"
    )
    notebook_data = utils.load_notebook_data(notebook_path)
    code_cells = utils.get_code_cells(notebook_data)

    assert len(code_cells) == 3
    assert all(cell["cell_type"] == "code" for cell in code_cells)
    # Verify R syntax is preserved
    assert "x <- 5" in code_cells[0]["source"][0]
    assert "y <- x * 2" in code_cells[1]["source"][0]


def test_julia_notebook_code_cells_extracted_correctly():
    """Tests that code cells are correctly extracted from Julia notebooks."""
    notebook_path = os.path.join(
        "test", "test_data", "notebooks", "julia", "valid", "valid_julia_notebook.ipynb"
    )
    notebook_data = utils.load_notebook_data(notebook_path)
    code_cells = utils.get_code_cells(notebook_data)

    assert len(code_cells) == 3
    assert all(cell["cell_type"] == "code" for cell in code_cells)
    # Verify Julia syntax is preserved
    assert "a = 10" in code_cells[0]["source"][0]
    assert "arr = [1, 2, 3]" in code_cells[1]["source"][0]


def test_process_path_with_r_notebooks_directory():
    """Tests that process_path works with a directory of R notebooks."""
    test_data_dir = os.path.join("test", "test_data", "notebooks", "r")

    # This should process all notebooks in the directory
    # The valid one will pass, but the invalid one will raise an error
    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError):
        enforce_notebook_run_order.process_path(test_data_dir)


def test_process_path_with_julia_notebooks_directory():
    """Tests that process_path works with a directory of Julia notebooks."""
    test_data_dir = os.path.join("test", "test_data", "notebooks", "julia")

    # This should process all notebooks in the directory
    # The valid one will pass, but the invalid one will raise an error
    with pytest.raises(enforce_notebook_run_order.InvalidNotebookRunError):
        enforce_notebook_run_order.process_path(test_data_dir)
