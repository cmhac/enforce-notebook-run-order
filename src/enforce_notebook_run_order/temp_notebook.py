"""Creates and runs a temporary notebook to verify outputs"""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from . import utils


class NotebookRunFailedError(Exception):
    """
    raised when a notebook fails to run because the provided json is not a valid notebook
    """


class CellOutputMismatchError(Exception):
    """
    raised when the output of a code cell does not match the expected output
    """


class TempNotebook:
    """Creates and runs a temporary notebook to verify outputs"""

    def __init__(self, notebook_path: str):
        """
        Args:
            notebook_path (Union[str, pathlib.Path]): Path to the notebook file.
        """
        self.original_notebook_path = Path(notebook_path)
        with open(self.original_notebook_path, "r", encoding="UTF-8") as notebook_file:
            self.notebook_data = json.load(notebook_file)
        self.temp_dir = Path(tempfile.mkdtemp())
        self.temp_notebook_path = self.temp_dir / "temp_notebook.ipynb"
        self.create_temp_file()

    def create_temp_file(self):
        """Creates a temporary notebook file with the given notebook data"""

        with open(self.temp_notebook_path, "w", encoding="UTF-8") as notebook_file:
            json.dump(self.notebook_data, notebook_file)

    def run(self):
        """Runs the temporary notebook

        Raises:
            NotebookRunFailedError: if the notebook fails to run because
                the provided json is not a valid notebook
        """
        try:
            subprocess.run(
                [
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    self.temp_notebook_path,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as error:
            raise NotebookRunFailedError(
                f"Notebook {self.temp_notebook_path} failed to run.\n\n"
                f"Error message: {error}\n\n"
            ) from error

        # get the json data from the saved notebook
        # file will be at filename.nbconvert.ipynb
        output_file_path = self.temp_notebook_path.with_suffix(".nbconvert.ipynb")
        output_data = utils.load_notebook_data(output_file_path)
        return output_data

    def compare_outputs(self, output_data: dict):
        """
        compares the outputs of cells of the temporary notebook to the cells
        of the output notebook

        Args:
            output_data (dict): the output notebook data

        Raises:
            CellOutputMismatchError: if the output of a cell does not match the expected output
        """
        code_cells = utils.get_code_cells(output_data)
        # if the first cell has the no-run comment, exit early
        if utils.cell_has_no_run_comment(code_cells[0]):
            return

        for cell_index, cell_data in enumerate(code_cells):
            # if the cell has a no-check-output comment, skip checking it
            if utils.cell_has_no_check_output_comment(cell_data):
                continue

            # check that the output cell matches the input cell
            if (
                cell_data["outputs"]
                != self.notebook_data["cells"][cell_index]["outputs"]
            ):
                raise CellOutputMismatchError(
                    f"Cell #{cell_index} output does not match the expected output.\n\n"
                    f"Cell contents: \n\n> {cell_data}"
                    "Expected output: \n\n> "
                    f"{self.notebook_data['cells'][cell_index]['outputs']}"
                )

    def check_notebook(self):
        """Runs the temporary notebook and compares the outputs"""
        output_data = self.run()
        self.compare_outputs(output_data)

    def __del__(self):
        """Deletes the temporary directory"""
        shutil.rmtree(self.temp_dir)

    def __enter__(self):
        """Returns the path to the temporary notebook"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Deletes the temporary directory"""
        del self
