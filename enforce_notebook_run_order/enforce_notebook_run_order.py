"""Validates notebooks were executed sequentially.

The tool inspects existing ``execution_count`` values of non-empty code cells and
raises an error if:
- Any code cell was not executed (execution_count is None)
- The first non-empty code cell does not start from execution_count=1
- Execution counts are not strictly sequential (must increase by exactly 1)
- There are gaps in the execution sequence (e.g., 1, 2, 4 with 3 missing)

It does not execute notebooks or inspect outputs.
"""

import os
from typing import Dict
from . import utils


class NotebookCodeCellNotRunError(Exception):
    """Raised when a notebook code cell was not run"""


class NotebookRunOrderError(Exception):
    """Raised when a notebook is run out of order"""


class InvalidNotebookRunError(Exception):
    """Raised when any problems were identified with a notebook's run order"""


def check_notebook_run_order(notebook_data: Dict) -> None:
    """Checks that the notebook cells were run sequentially and fails if not.

    Enforces that all non-empty code cells must have been executed (execution_count
    is not None), execution must start from 1 (first non-empty code cell must have
    execution_count=1), and execution must be strictly sequential without gaps
    (1, 2, 3, ... with no skipped numbers).

    Args:
        notebook_data: Notebook data in dictionary format.

    Raises:
        NotebookCodeCellNotRunError: If a code cell in the notebook was not run.
        NotebookRunOrderError: If the cells in the notebook were not run sequentially,
        including if they don't start from 1 or have gaps in the sequence.
    """
    previous_cell_number = 0
    code_cells = utils.get_code_cells(notebook_data)
    for cell in code_cells:
        current_cell_number = cell["execution_count"]
        current_cell_source = cell["source"]
        # ignore empty cells
        if len(current_cell_source) > 0:
            if current_cell_number is None:
                raise NotebookCodeCellNotRunError(
                    f"Code cell was not run. The previous cell was #{previous_cell_number}. \n\n"
                    f"Cell contents: \n\n> {cell}"
                )
            if current_cell_number != previous_cell_number + 1:
                raise NotebookRunOrderError(
                    "Cells were not run sequentially. "
                    f"The cell that caused this error is #{current_cell_number} "
                    f"and the previous cell was #{previous_cell_number}. \n\n"
                    f"Cell contents: \n\n> {cell}"
                )
        previous_cell_number = current_cell_number


def check_single_notebook(notebook_path: str) -> None:
    """Check a single notebook for sequential execution.

    Args:
        notebook_path: Path to the notebook file.

    Raises:
        InvalidNotebookRunError: If any problems were identified with the notebook's run order.
    """
    notebook_data = utils.load_notebook_data(notebook_path)
    try:
        check_notebook_run_order(notebook_data)
    except (
        NotebookCodeCellNotRunError,
        NotebookRunOrderError,
    ) as error:
        raise InvalidNotebookRunError(
            f"Notebook {notebook_path} was not run in order.\n\n{error}\n\n"
        ) from error
    print(f"Notebook {notebook_path} was run correctly.")


def process_path(path: str) -> None:
    """Process a path to a notebook file or directory recursively.

    Args:
        path: Path to a single ``.ipynb`` file or a directory containing notebooks.

    Raises:
        ValueError: If the path is neither a directory nor a ``.ipynb`` file.
    """
    if os.path.isdir(path):
        # Get all .ipynb files in the directory and its subdirectories
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                notebook_path = os.path.join(dirpath, filename)
                if filename.endswith(".ipynb"):
                    check_single_notebook(notebook_path)
    elif path.endswith(".ipynb"):
        check_single_notebook(path)
    else:
        raise ValueError(
            f"Cannot check file {path}. "
            "Must be a path to a notebook file with the .ipynb extension, or a directory."
        )
