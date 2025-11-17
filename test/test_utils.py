"""tests certain functions from the utils module"""

import os
import pytest
from enforce_notebook_run_order import utils


def test_load_notebook_data_valid_notebook():
    """Tests that load_notebook_data successfully loads a valid notebook file"""
    notebook_path = os.path.join(
        "test", "test_data", "enforce_notebook_run_order_valid", "valid_notebook.ipynb"
    )
    notebook_data = utils.load_notebook_data(notebook_path)

    assert isinstance(notebook_data, dict)
    assert "cells" in notebook_data
    assert isinstance(notebook_data["cells"], list)
    assert len(notebook_data["cells"]) > 0


def test_load_notebook_data_nonexistent_file():
    """Tests that load_notebook_data raises FileNotFoundError for nonexistent file"""
    with pytest.raises(FileNotFoundError):
        utils.load_notebook_data("nonexistent_notebook.ipynb")


def test_get_code_cells_mixed_cells(notebook_data_with_mixed_cells):
    """Tests that get_code_cells returns only code cells from mixed cell types"""
    code_cells = utils.get_code_cells(notebook_data_with_mixed_cells)

    assert len(code_cells) == 3
    assert all(cell["cell_type"] == "code" for cell in code_cells)
    assert code_cells[0]["execution_count"] == 1
    assert code_cells[1]["execution_count"] == 2
    assert code_cells[2]["execution_count"] == 3


def test_get_code_cells_only_code_cells(notebook_data_only_code_cells):
    """Tests that get_code_cells returns all cells when notebook has only code cells"""
    code_cells = utils.get_code_cells(notebook_data_only_code_cells)

    assert len(code_cells) == 2
    assert all(cell["cell_type"] == "code" for cell in code_cells)


def test_get_code_cells_no_code_cells(notebook_data_no_code_cells):
    """Tests that get_code_cells returns empty list when notebook has no code cells"""
    code_cells = utils.get_code_cells(notebook_data_no_code_cells)

    assert len(code_cells) == 0
    assert isinstance(code_cells, list)


def test_get_code_cells_empty_notebook(notebook_data_empty):
    """Tests that get_code_cells returns empty list for notebook with no cells"""
    code_cells = utils.get_code_cells(notebook_data_empty)

    assert len(code_cells) == 0
    assert isinstance(code_cells, list)


def test_get_code_cells_preserves_cell_data(notebook_data_with_mixed_cells):
    """Tests that get_code_cells preserves all cell data"""
    code_cells = utils.get_code_cells(notebook_data_with_mixed_cells)

    # Verify first code cell has all expected fields
    assert "cell_type" in code_cells[0]
    assert "execution_count" in code_cells[0]
    assert "source" in code_cells[0]
    assert code_cells[0]["source"] == ["print('cell 1')"]
