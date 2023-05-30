"""tests the remove_hook module"""

from pathlib import Path
import pytest
from hook_manager.add_hook import add_hook
from hook_manager.remove_hook import remove_hook
from hook_manager.common import get_existing_hook_script
from .utils import TempGitRepo


def test_remove_hook_hook_exists():
    """
    creates a temporary git repo and adds a pre-commit hook
    then removes the pre-commit hook
    """
    hook_name = "pre-commit"
    command_name = "enforce_notebook_run_order"
    command_text = f"python -m {command_name}"
    with TempGitRepo():
        assert get_existing_hook_script(hook_name) is None
        add_hook(hook_name, command_name)
        assert command_text in get_existing_hook_script(hook_name)
        remove_hook(hook_name, command_name)
        assert command_text not in get_existing_hook_script(hook_name)


def test_remove_hook_hook_not_exists():
    """
    creates a temporary git repo and adds a pre-commit hook
    then removes the pre-commit hook
    """
    hook_name = "pre-commit"
    command_name = "enforce_notebook_run_order"
    with TempGitRepo():
        # create an empty hook
        hook_path = f".git/hooks/{hook_name}"
        Path(hook_path).touch()
        assert get_existing_hook_script(hook_name) == ""
        with pytest.raises(ValueError):
            remove_hook(hook_name, command_name)
