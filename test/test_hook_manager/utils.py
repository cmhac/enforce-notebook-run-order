import os
import subprocess
import tempfile


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
