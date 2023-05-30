"""adds one of the modules in the src directory as a hook to the current repo"""

import os
from pathlib import Path
import shutil
import sys
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


def add_hook(hook_name: str, command_name: str) -> None:
    """adds the hook to the current repo"""
    if not is_valid_hook_name(hook_name):
        raise ValueError(
            f"Invalid hook name: {hook_name}. "
            f"Valid hook names are: {', '.join(VALID_HOOKS)}"
        )

    if not is_valid_hook_command(command_name):
        raise ValueError(
            f"Invalid command name: {command_name}. "
            "Please check that it is installed correctly."
        )

    existing_hook_script = get_existing_hook_script(hook_name)

    if existing_hook_script:
        if command_name in existing_hook_script:
            print(f"Hook {hook_name} already exists for {command_name}.")
            return

        print(f"Hook {hook_name} already exists. Appending {command_name} to it.")
        hook_script = existing_hook_script + "\n" + command_name
    else:
        print(f"Hook {hook_name} does not exist. Creating it.")
        hook_script = command_name

    hook_path = Path(".git") / "hooks" / hook_name
    hook_path.write_text(hook_script)
    hook_path.chmod(0o755)
