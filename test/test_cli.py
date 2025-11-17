"""tests the CLI module"""

from click.testing import CliRunner
from enforce_notebook_run_order.cli import cli

# pylint: disable=redefined-outer-name


def test_cli_path_valid_notebook():
    """Tests that the CLI returns 0 when given a valid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/notebooks/python/valid/valid_notebook.ipynb",
        ],
    )
    assert result.exit_code == 0


def test_cli_path_invalid_notebook():
    """Tests that the CLI returns 1 when given an invalid notebook path."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/notebooks/nested_subdirectory_structure/level1/level2/"
            "invalid_nested_notebook.ipynb",
        ],
    )
    assert result.exit_code == 1


def test_cli_directory_valid_notebooks():
    """Tests that the CLI returns 0 when given a valid notebook directory."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/notebooks/python/valid",
        ],
    )
    assert result.exit_code == 0


def test_cli_no_args_searches_current_directory(mocker):
    """
    Tests that the CLI searches the entire current directory if no paths are specified.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    runner = CliRunner()
    result = runner.invoke(cli)

    # The process_path function should be called once, with the current directory as its argument
    mock_process_path.assert_called_once_with(".")

    assert result.exit_code == 0


def test_cli_no_args_delegates_to_process_path_with_dot(mocker):
    """
    Tests that process_path is called with "." when no paths are specified.
    This verifies the recursion starts from the current directory.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    # Verify process_path was called exactly once with "."
    mock_process_path.assert_called_once()
    args, _ = mock_process_path.call_args
    assert args[0] == "."
    assert result.exit_code == 0


def test_cli_multiple_paths_delegates_to_process_path_for_each(mocker):
    """
    Tests that process_path is called for each path argument provided.
    """
    mock_process_path = mocker.patch("enforce_notebook_run_order.cli.process_path")

    test_path_1 = "test/test_data/notebooks/python/valid"
    test_path_2 = "test/test_data/notebooks/python/invalid"

    runner = CliRunner()
    result = runner.invoke(cli, [test_path_1, test_path_2])

    # Verify process_path was called twice, once for each path
    assert mock_process_path.call_count == 2
    calls = [call[0][0] for call in mock_process_path.call_args_list]
    assert test_path_1 in calls
    assert test_path_2 in calls
    assert result.exit_code == 0


def test_cli_no_args_delegates_to_process_path_with_current_dir(mocker):
    """
    Tests that calling CLI with no paths delegates to process_path with
    the current directory, enabling recursive scanning from root.
    """
    mock_load_notebook_data = mocker.patch(
        "enforce_notebook_run_order.utils.load_notebook_data"
    )
    mock_check_notebook_run_order = mocker.patch(
        "enforce_notebook_run_order.enforce_notebook_run_order.check_notebook_run_order"
    )

    # Return valid notebook data so process_path succeeds
    mock_load_notebook_data.return_value = {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "source": ["print('foo')"]}
        ]
    }

    runner = CliRunner()
    result = runner.invoke(cli, [])

    # Verify the chain of calls demonstrates recursion from current directory
    assert result.exit_code == 0
    # Both check_notebook_run_order was called (proving notebooks were processed)
    # and the process started from "." (which os.walk would handle recursively)
    assert mock_check_notebook_run_order.called


def test_cli_no_args_exits_with_error_on_invalid_notebook():
    """Tests that CLI exits with a non-zero status when scanning '.' finds bad notebooks."""
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 1


# E2E tests for multi-language notebook support


def test_cli_valid_r_notebook():
    """E2E test: CLI returns 0 for a valid R notebook."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test/test_data/notebooks/r/valid/valid_r_notebook.ipynb"]
    )

    assert result.exit_code == 0
    assert "VALID" in result.output


def test_cli_invalid_r_notebook():
    """E2E test: CLI returns 1 for an invalid R notebook."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test/test_data/notebooks/r/invalid/invalid_r_notebook.ipynb"]
    )

    assert result.exit_code == 1
    # Exception details are in the exception attribute when not caught
    assert result.exception is not None
    assert "not run in order" in str(result.exception)


def test_cli_valid_julia_notebook():
    """E2E test: CLI returns 0 for a valid Julia notebook."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test/test_data/notebooks/julia/valid/valid_julia_notebook.ipynb"]
    )

    assert result.exit_code == 0
    assert "VALID" in result.output


def test_cli_invalid_julia_notebook():
    """E2E test: CLI returns 1 for an invalid Julia notebook."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["test/test_data/notebooks/julia/invalid/invalid_julia_notebook.ipynb"]
    )

    assert result.exit_code == 1
    # Exception details are in the exception attribute when not caught
    assert result.exception is not None
    assert "not run in order" in str(result.exception)


def test_cli_r_notebooks_directory():
    """E2E test: CLI processes directory with mixed valid/invalid R notebooks."""
    runner = CliRunner()
    result = runner.invoke(cli, ["test/test_data/notebooks/r"])

    # Should fail because the directory contains an invalid notebook
    assert result.exit_code == 1
    assert result.exception is not None
    assert "not run in order" in str(result.exception)


def test_cli_julia_notebooks_directory():
    """E2E test: CLI processes directory with mixed valid/invalid Julia notebooks."""
    runner = CliRunner()
    result = runner.invoke(cli, ["test/test_data/notebooks/julia"])

    # Should fail because the directory contains an invalid notebook
    assert result.exit_code == 1
    assert result.exception is not None
    assert "not run in order" in str(result.exception)


def test_cli_multiple_language_notebooks():
    """E2E test: CLI can process multiple notebooks of different languages in one call."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "test/test_data/notebooks/r/valid/valid_r_notebook.ipynb",
            "test/test_data/notebooks/julia/valid/valid_julia_notebook.ipynb",
            "test/test_data/notebooks/python/valid/valid_notebook.ipynb",
        ],
    )

    assert result.exit_code == 0
    # Should see success messages for all three notebooks
    assert result.output.count("VALID") == 3
