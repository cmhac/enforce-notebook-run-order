"""Creates and runs a temporary notebook to verify outputs"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from . import utils


class NotebookRunFailedError(Exception):
    """
    Raised when a notebook fails to run because the provided JSON is not a valid notebook.
    """


class CellOutputMismatchError(Exception):
    """
    Raised when the output of a code cell does not match the expected output.
    """


class TempNotebook:
    """Creates and runs a temporary notebook to verify outputs"""

    def __init__(self, notebook_path: str):
        """
        Initializes a temporary notebook from the specified path.

        Args:
            notebook_path (str): Path to the notebook file.
        """
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, "r", encoding="UTF-8") as notebook_file:
            self.notebook_data = json.load(notebook_file)
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output_notebook_path = self.temp_dir / "temp_notebook.ipynb"

    def run(self) -> dict:
        """Runs the temporary notebook and captures its output.

        Raises:
            NotebookRunFailedError: If the notebook fails to run because the
            provided JSON is not a valid notebook.

        Returns:
            dict: The notebook data of the executed notebook.
        """
        resp = subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--output",
                self.output_notebook_path,
                self.notebook_path,
            ],
            capture_output=True,
            check=False,
            encoding="utf-8",
            universal_newlines=True,
        )
        if resp.returncode != 0:
            stderr_without_ansi = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", resp.stderr)
            raise NotebookRunFailedError(
                f"Notebook {self.output_notebook_path} failed to run.\n\n"
                f"Error message: {stderr_without_ansi}\n\n"
            )

        # get the json data from the saved notebook
        # file will be at filename.nbconvert.ipynb
        output_file_path = self.output_notebook_path
        output_data = utils.load_notebook_data(output_file_path)
        return output_data

    def compare_outputs(self, output_data: dict):
        """
        Compares the outputs of code cells between the temporary and original notebook.

        Args:
            output_data (dict): The output notebook data from the executed notebook.

        Raises:
            CellOutputMismatchError: If the output of a cell does not match the expected output.
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
        """Enables use with the with-statement context manager"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Cleans up by deleting the temporary directory"""
        del self
