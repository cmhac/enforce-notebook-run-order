"""contains shared functions for managing hooks"""

from pathlib import Path
from typing import Union


VALID_HOOKS = ["pre-commit", "pre-push", "pre-rebase"]


def is_valid_hook_name(hook_name: str) -> bool:
    """checks that the hook name is valid"""
    return hook_name in VALID_HOOKS


def is_valid_hook_command(command_name: str) -> bool:
    """attempts to import the command and returns True if it succeeds"""
    try:
        __import__(command_name)
        return True
    except ImportError:
        return False


def get_existing_hook_script(hook_name: str) -> Union[str, None]:
    """returns the contents of the existing hook script, if it exists"""
    hook_path = Path(".git") / "hooks" / hook_name
    if hook_path.exists():
        return hook_path.read_text()
    return None
