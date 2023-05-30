"""tests the add_hook module"""

import os
from hook_manager.add_hook import add_hook
from .utils import TempGitRepo


def test_add_hook_hook_exists():
    """
    creates a temporary git repo and adds a pre-commit hook
    then tests that the specified command was added to the hook
    """
    hook_contents = "#!/bin/sh\n\nexit 0\n"
    command_name = "enforce_notebook_run_order"
    command_text = f"python -m {command_name}"
    with TempGitRepo():
        # write the existing hook contents
        hook_path = os.path.join(".git", "hooks", "pre-commit")
        with open(hook_path, "w", encoding="UTF-8") as hook_file:
            hook_file.write(hook_contents)

        assert command_text not in hook_contents

        # add the hook
        add_hook("pre-commit", command_name)

        # check that the hook was updated
        with open(hook_path, "r", encoding="UTF-8") as hook_file:
            new_hook_contents = hook_file.read()
            assert command_text in new_hook_contents


def test_add_hook_hook_not_exists():
    """
    creates a temporary git repo and tests that the specified command was added to the hook
    """
    command_name = "enforce_notebook_run_order"
    command_text = f"python -m {command_name}"
    with TempGitRepo():
        # check that the hook doesn't exist
        hook_path = os.path.join(".git", "hooks", "pre-commit")
        assert not os.path.exists(hook_path)

        # add the hook
        add_hook("pre-commit", command_name)

        # check that the hook was created
        assert os.path.exists(hook_path)

        # check that the hook was updated
        with open(hook_path, "r", encoding="UTF-8") as hook_file:
            new_hook_contents = hook_file.read()
            assert command_text in new_hook_contents
