"""creates and runs a temporary notebook to verify outputs"""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile


class InvalidNotebookJsonError(Exception):
    """
    raised when a notebook fails to run because the provided json is not a valid notebook
    """


class TempNotebook:
    """creates and runs a temporary notebook to verify outputs"""

    def __init__(self, notebook_data: dict):
        """
        Args:
            notebook_path (Union[str, pathlib.Path]): Path to the notebook file.
        """
        self.notebook_data = notebook_data
        self.temp_dir = Path(tempfile.mkdtemp())
        self.notebook_path = self.temp_dir / "temp_notebook.ipynb"
        self.create_temp_file()

    def create_temp_file(self):
        """creates a temporary notebook file with the given notebook data"""

        with open(self.notebook_path, "w", encoding="UTF-8") as notebook_file:
            json.dump(self.notebook_data, notebook_file)

    def run(self):
        """runs the temporary notebook"""
        try:
            subprocess.run(
                [
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    self.notebook_path,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as error:
            raise InvalidNotebookJsonError(
                f"Notebook {self.notebook_path} failed to run.\n\n"
                f"Error message: {error}\n\n"
            ) from error

        # get the json data from the saved notebook
        # file will be at filename.nbconvert.ipynb
        output_file_path = self.notebook_path.with_suffix(".nbconvert.ipynb")
        with open(output_file_path, "r", encoding="UTF-8") as output_file:
            output_data = json.load(output_file)
        return output_data

    def __del__(self):
        """deletes the temporary directory"""
        shutil.rmtree(self.temp_dir)

    def __enter__(self):
        """returns the path to the temporary notebook"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """deletes the temporary directory"""
        del self
