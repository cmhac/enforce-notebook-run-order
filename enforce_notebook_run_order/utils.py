"""Contains shared functionality used across multiple modules"""

import json
from typing import Dict, List


def load_notebook_data(notebook_path: str) -> Dict:
    """Loads the notebook data from the given path.

    Args:
        notebook_path (str): Path to the notebook file.

    Returns:
        Dict: Notebook data in dictionary format.
    """
    with open(notebook_path, "r", encoding="UTF-8") as notebook_file:
        notebook_data = json.load(notebook_file)
    return notebook_data


def get_code_cells(notebook_data: Dict) -> List[Dict]:
    """Returns a list of code cells from the notebook data.

    Args:
        notebook_data (Dict): Notebook data in dictionary format.

    Returns:
        List[Dict]: List of code cells from the notebook.
    """
    code_cells = []
    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            code_cells.append(cell)
    return code_cells
