"""contains shared functionality used across multiple modules"""

import json


def load_notebook_data(notebook_path: str) -> dict:  # pragma: no cover
    """loads the notebook data from the given path"""
    with open(notebook_path, "r", encoding="UTF-8") as notebook_file:
        notebook_data = json.load(notebook_file)
    return notebook_data


def get_code_cells(notebook_data: dict) -> list:  # pragma: no cover
    """returns a list of code cells from the notebook data"""
    code_cells = []
    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            code_cells.append(cell)
    return code_cells
