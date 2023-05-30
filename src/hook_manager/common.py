"""contains shared functions for managing hooks"""

from pathlib import Path
from typing import Union


VALID_HOOKS = ["pre-commit", "pre-push", "pre-rebase"]


def check_is_valid_hook_name(hook_name: str) -> bool:
    """checks that the hook name is valid"""
    if not hook_name in VALID_HOOKS:
        raise ValueError(
            f"Invalid hook name: {hook_name}. "
            f"Valid hook names are: {', '.join(VALID_HOOKS)}"
        )


def check_is_valid_hook_command(command_name: str) -> bool:
    """attempts to import the command and returns True if it succeeds"""
    try:
        __import__(command_name)
        return True
    except ImportError as exc:
        raise ValueError(
            f"Invalid command name: {command_name}. "
            "Please check that it is installed correctly."
        ) from exc


def get_existing_hook_script(hook_name: str) -> Union[str, None]:
    """returns the contents of the existing hook script, if it exists"""
    hook_path = Path(".git") / "hooks" / hook_name
    if hook_path.exists():
        return hook_path.read_text()
    return None


def get_hook_command(command_name: str) -> str:
    """returns the text of the command to be added to a hook"""
    return (
        "\n\n"
        f"### BEGIN AUTOMATICALLY GENERATED - {command_name} ###"
        "\n\n"
        f"python -m {command_name}"
        "\n\n"
        "### END AUTOMATICALLY GENERATED ###"
        "\n\n"
    )
