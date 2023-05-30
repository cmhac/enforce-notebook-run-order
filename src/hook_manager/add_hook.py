"""adds one of the modules in the src directory as a hook to the current repo"""

from pathlib import Path
from . import common


def add_hook(hook_name: str, command_name: str) -> None:
    """adds the hook to the current repo"""
    common.check_is_valid_hook_name(hook_name)
    common.check_is_valid_hook_command(command_name)

    existing_hook_script = common.get_existing_hook_script(hook_name)
    hook_command = common.get_hook_command(command_name)

    if existing_hook_script:
        if command_name in existing_hook_script:
            print(f"Hook {hook_name} already exists for {command_name}.")
            return

        print(f"Hook {hook_name} already exists. Appending {command_name} to it.")
        hook_script = existing_hook_script + hook_command
    else:
        print(f"Hook {hook_name} does not exist. Creating it.")
        hook_script = "#!/usr/bin/env bash" + hook_command

    hook_path = Path(".git") / "hooks" / hook_name
    hook_path.write_text(hook_script)
    hook_path.chmod(0o755)
