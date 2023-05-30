"""tests the add_hook module"""

import os
import subprocess
import tempfile
from hook_manager.add_hook import (
    is_valid_hook_name,
    is_valid_hook_command,
    get_existing_hook_script,
    add_hook,
)


def test_is_valid_hook_name_valid():
    """tests that valid hook names are valid"""
    assert is_valid_hook_name("pre-commit")
    assert is_valid_hook_name("pre-push")
    assert is_valid_hook_name("pre-rebase")


def test_is_valid_hook_name_invalid():
    """test that unsupported hook names are not valid"""
    assert is_valid_hook_name("pre-merge-commit") is False
    assert is_valid_hook_name("pre-receive") is False
    assert is_valid_hook_name("update") is False


def test_is_valid_hook_command_valid():
    """tests that valid hook commands are valid"""
    assert is_valid_hook_command("enforce_notebook_run_order")


def test_is_valid_hook_command_invalid():
    """tests that invalid hook commands are invalid"""
    assert is_valid_hook_command("not_a_real_command") is False


class TempGitRepo:
    """creates a temporary git repo for testing purposes"""

    def __init__(self):
        self.start_dir = os.getcwd()
        self.tmpdir = tempfile.TemporaryDirectory()

    def __enter__(self):
        os.chdir(self.tmpdir.name)
        subprocess.check_call(["git", "init"], cwd=self.tmpdir.name)
        return self.tmpdir.name  # Return the temp directory path

    def __exit__(self, exc_type, exc_value, traceback):
        self.tmpdir.cleanup()  # Remove the directory when done
        os.chdir(self.start_dir)


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


def test_add_hook_hook_exists():
    """
    creates a temporary git repo and adds a pre-commit hook
    then tests that the specified command was added to the hook
    """
    hook_contents = "#!/bin/sh\n\nexit 0\n"
    with TempGitRepo():
        # write the existing hook contents
        hook_path = os.path.join(".git", "hooks", "pre-commit")
        with open(hook_path, "w", encoding="UTF-8") as hook_file:
            hook_file.write(hook_contents)

        # add the hook
        add_hook("pre-commit", "enforce_notebook_run_order")

        # check that the hook was updated
        with open(hook_path, "r", encoding="UTF-8") as hook_file:
            new_hook_contents = hook_file.read()
            assert "enforce_notebook_run_order" in new_hook_contents
