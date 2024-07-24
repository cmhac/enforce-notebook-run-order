"""Command-line interface for enforce_notebook_run_order"""

from typing import Tuple
import click
from .enforce_notebook_run_order import process_path


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True), required=False)
def cli(paths: Tuple[str, ...] = None):
    """
    Checks the run order of notebooks in the specified paths,
    or the entire repo if no paths are specified

    Args:
        paths: The paths to check. If no paths are specified, the current directory is checked.
        no_run: If True, the notebooks will not be run. This may miss some errors, but is useful
    """
    if paths:
        for path in paths:
            process_path(path)
    else:
        # If no paths are provided, check the current directory
        process_path(".")
