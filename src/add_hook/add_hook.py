"""adds one of the modules in the src directory as a hook to the current repo"""

import os
from pathlib import Path
import shutil
import sys


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
