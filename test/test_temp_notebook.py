"""tests the temp notebook module"""

import os
import pytest
import temp_notebook

# pylint: disable=redefined-outer-name


@pytest.fixture
def valid_notebook_data():
    """returns the complete json of a jupyter notebook with 1 cell"""
    return {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["hello world\n"],
                    }
                ],
                "source": ['print("hello world")'],
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": ".venv",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }


@pytest.fixture
def invalid_notebook_data():
    """returns json that is not a valid jupyter notebook"""
    return {"not_a_notebook": True}


@pytest.fixture
def output_mismatch_data():
    """
    returns the json of a notebook whose cell output does not match
    the expected output
    """
    return {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": ["var_1 = 2\n"],
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [
                    {"name": "stdout", "output_type": "stream", "text": ["1\n"]}
                ],
                "source": ["print(var_1)\n"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": ".venv",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }


def test_create_temp_file(valid_notebook_data):
    """tests that the temp notebook creates a temporary file"""
    with temp_notebook.TempNotebook(valid_notebook_data) as temp_notebook_obj:
        assert os.path.exists(temp_notebook_obj.notebook_path)


def test_run_valid_json(valid_notebook_data):
    """tests that the temp notebook runs with valid json"""
    with temp_notebook.TempNotebook(valid_notebook_data) as temp_notebook_obj:
        temp_notebook_obj.run()


def test_run_invalid_json(invalid_notebook_data):
    """tests that the temp notebook raises an exception with invalid json"""
    with temp_notebook.TempNotebook(invalid_notebook_data) as temp_notebook_obj:
        with pytest.raises(temp_notebook.InvalidNotebookJsonError):
            temp_notebook_obj.run()


def test_check_notebook_valid(valid_notebook_data):
    """tests that the temp notebook passes with valid json"""
    with temp_notebook.TempNotebook(valid_notebook_data) as temp_notebook_obj:
        temp_notebook_obj.check_notebook()


def test_check_notebook_invalid(output_mismatch_data):
    """tests that the temp notebook fails with invalid json"""
    with temp_notebook.TempNotebook(output_mismatch_data) as temp_notebook_obj:
        with pytest.raises(temp_notebook.CellOutputMismatchError):
            temp_notebook_obj.check_notebook()
