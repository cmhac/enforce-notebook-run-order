"""tests certain functions from the utils module"""

import pytest
from enforce_notebook_run_order import utils

# pylint: disable=redefined-outer-name


@pytest.fixture
def cell_json_with_comment():
    """Returns a cell json with a comment"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["# this is a comment"],
    }


@pytest.fixture
def cell_json_with_comment_extra_spaces():
    """Returns a cell json with a comment and extra spaces"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["#     this is a comment    "],
    }


@pytest.fixture
def cell_json_with_comment_no_space():
    """Returns a cell json with a comment and no space"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["#this is a comment"],
    }


@pytest.fixture
def cell_json_without_comment():
    """Returns a cell json without a comment"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["print('hello world')"],
    }


@pytest.fixture
def cell_with_no_run_comment():
    """Returns a cell json with a no-run comment"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["# no-run"],
    }


@pytest.fixture
def cell_with_no_check_output_comment():
    """Returns a cell json with a no-check-output comment"""
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": ["# no-check-output"],
    }


def test_parse_cell_comment(
    cell_json_with_comment,
    cell_json_with_comment_extra_spaces,
    cell_json_with_comment_no_space,
):
    """
    tests that parse_cell_comment returns the comment
    from the first line of the cell, if present
    """
    assert utils.parse_cell_comment(cell_json_with_comment) == "this is a comment"
    assert (
        utils.parse_cell_comment(cell_json_with_comment_extra_spaces)
        == "this is a comment"
    )
    assert (
        utils.parse_cell_comment(cell_json_with_comment_no_space) == "this is a comment"
    )


def test_parse_cell_comment_returns_none_when_no_comment(cell_json_without_comment):
    """tests that parse_cell_comment returns None if there is no comment"""
    assert utils.parse_cell_comment(cell_json_without_comment) is None


def test_cell_has_no_run_comment(cell_with_no_run_comment):
    """tests that cell_has_no_run_comment returns True if the cell has a no-run comment"""
    assert utils.cell_has_no_run_comment(cell_with_no_run_comment)


def test_cell_has_no_run_comment_returns_false_when_no_comment(
    cell_json_without_comment,
):
    """tests that cell_has_no_run_comment returns False if the cell has no comment"""
    assert not utils.cell_has_no_run_comment(cell_json_without_comment)


def test_cell_has_no_check_output_comment(cell_with_no_check_output_comment):
    """
    tests that cell_has_no_check_output_comment returns True
    if the cell has a no-check-output comment
    """
    assert utils.cell_has_no_check_output_comment(cell_with_no_check_output_comment)


def test_cell_has_no_check_output_comment_returns_false_when_no_comment(
    cell_json_without_comment,
):
    """tests that cell_has_no_check_output_comment returns False if the cell has no comment"""
    assert not utils.cell_has_no_check_output_comment(cell_json_without_comment)
