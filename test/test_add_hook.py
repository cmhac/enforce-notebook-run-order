"""tests the add_hook module"""

from add_hook import add_hook


def test_is_valid_hook_name_valid():
    """tests that valid hook names are valid"""
    assert add_hook.is_valid_hook_name("pre-commit")
    assert add_hook.is_valid_hook_name("pre-push")
    assert add_hook.is_valid_hook_name("pre-rebase")


def test_is_valid_hook_name_invalid():
    """test that unsupported hook names are not valid"""
    assert add_hook.is_valid_hook_name("pre-merge-commit") is False
    assert add_hook.is_valid_hook_name("pre-receive") is False
    assert add_hook.is_valid_hook_name("update") is False
