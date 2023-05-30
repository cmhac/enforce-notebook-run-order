"""tests the add_hook module"""

import os
import subprocess
import tempfile
from hook_manager.add_hook import add_hook


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
