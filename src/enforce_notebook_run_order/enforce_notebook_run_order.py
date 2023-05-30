"""forces notebooks to run cells sequentially and fails if cells were run out of order"""

import json
import os
import pathlib


class NotebookCodeCellNotRunError(Exception):
    """raised when a notebook code cell was not run"""


class NotebookRunOrderError(Exception):
    """raised when a notebook is run out of order"""


class InvalidNotebookRunError(Exception):
    """raised when any problems were identified with a notebook's run order"""


def check_notebook_run_order(notebook_data: dict) -> None:
    """checks that the notebook cells were run sequentially and fails if not"""
    previous_cell_number = 0
    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            current_cell_number = cell["execution_count"]
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


def check_all_repo_notebooks(notebook_dir=".") -> None:
    """recursively searches for all jupyter notebooks in the repo and checks their run order"""
    for root, _, files in os.walk(notebook_dir):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = pathlib.Path(root) / file
                print(notebook_path)
                with open(notebook_path, "r", encoding="UTF-8") as notebook_file:
                    notebook_data = json.load(notebook_file)
                try:
                    check_notebook_run_order(notebook_data)
                except ValueError as error:
                    raise NotebookRunOrderError(
                        f"notebook {notebook_path} was run out of order"
                    ) from error


if __name__ == "__main__":
    check_all_repo_notebooks()
