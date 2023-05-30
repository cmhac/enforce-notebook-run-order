"""tests common hook manager functions"""

import os
import pytest
from hook_manager.common import (
    check_is_valid_hook_name,
    check_is_valid_hook_command,
    get_existing_hook_script,
    get_hook_command,
)
from .utils import TempGitRepo


def test_is_valid_hook_name_valid():
    """tests that valid hook names are valid"""
    try:
        check_is_valid_hook_name("pre-commit")
        check_is_valid_hook_name("pre-push")
        check_is_valid_hook_name("pre-rebase")
    except ValueError:
        pytest.fail("is_valid_hook_name raised ValueError unexpectedly")


def test_is_valid_hook_name_invalid():
    """test that unsupported hook names are not valid"""
    # assert is_valid_hook_name("pre-merge-commit") is False
    # assert is_valid_hook_name("pre-receive") is False
    # assert is_valid_hook_name("update") is False
    with pytest.raises(ValueError):
        check_is_valid_hook_name("pre-merge-commit")
    with pytest.raises(ValueError):
        check_is_valid_hook_name("pre-receive")
    with pytest.raises(ValueError):
        check_is_valid_hook_name("update")


def test_is_valid_hook_command_valid():
    """tests that valid hook commands are valid"""
    try:
        check_is_valid_hook_command("enforce_notebook_run_order")
    except ValueError:
        pytest.fail("is_valid_hook_command raised ValueError unexpectedly")


def test_is_valid_hook_command_invalid():
    """tests that invalid hook commands are invalid"""
    # assert is_valid_hook_command("not_a_real_command") is False
    with pytest.raises(ValueError):
        check_is_valid_hook_command("not_a_real_command")


def test_get_existing_hook_script_hook_not_exists():
    """tests that get_existing_hook_script returns None when the hook doesn't exist"""
    with TempGitRepo():
        assert get_existing_hook_script("pre-commit") is None


def test_get_existing_hook_script_hook_exists():
    """
    creates a temporary git repo and adds a pre-commit hook
    then tests that get_existing_hook_script returns the correct hook
    """
    hook_contents = "#!/bin/sh\n\nexit 0\n"
    with TempGitRepo():
        hook_path = os.path.join(".git", "hooks", "pre-commit")
        with open(hook_path, "w", encoding="UTF-8") as hook_file:
            hook_file.write(hook_contents)
        assert get_existing_hook_script("pre-commit") == hook_contents


def test_get_hook_command():
    """tests that get_hook_command returns the correct hook command"""
    assert (
        get_hook_command("enforce_notebook_run_order") == "\n\n"
        "### BEGIN AUTOMATICALLY GENERATED - enforce_notebook_run_order ###"
        "\n\n"
        "python -m enforce_notebook_run_order"
        "\n\n"
        "### END AUTOMATICALLY GENERATED ###"
        "\n\n"
    )
