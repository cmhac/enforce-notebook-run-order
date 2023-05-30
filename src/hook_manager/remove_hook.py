"""removes one of the modules in the src directory as a hook from the current repo"""

from pathlib import Path
from . import common


def remove_hook(hook_name: str, command_name: str) -> None:
    """removes a command from the hook in the current repo"""
    common.check_is_valid_hook_command(command_name)
    common.check_is_valid_hook_name(hook_name)

    existing_hook_script = common.get_existing_hook_script(hook_name)
    hook_command = common.get_hook_command(command_name)

    if not existing_hook_script:
        raise ValueError(f"Hook {hook_name} does not exist.")

    if hook_command not in existing_hook_script:
        raise ValueError(f"Hook {hook_name} does not contain command {command_name}.")

    hook_script = existing_hook_script.replace(hook_command, "")

    hook_path = Path(".git") / "hooks" / hook_name
    hook_path.write_text(hook_script)
