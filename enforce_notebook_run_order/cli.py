"""Command-line interface for enforce_notebook_run_order.

Checks run order of notebooks by inspecting existing execution counts.
Does not execute notebooks or validate outputs.
"""

import sys
from typing import Tuple
import click
from .enforce_notebook_run_order import process_path, InvalidNotebookRunError


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True), required=False)
def cli(paths: Tuple[str, ...] = None):
    """
    Checks the run order of notebooks in the specified paths,
    or recursively in the current directory if no paths are specified.

    Args:
        paths: Zero or more paths to notebook files or directories.
            Directories are traversed recursively. If omitted, ``.`` is used.
    """
    try:
        if paths:
            for path in paths:
                process_path(path)
        else:
            # If no paths are provided, check the current directory
            process_path(".")
    except InvalidNotebookRunError:
        # Error message already printed by check_single_notebook
        sys.exit(1)
