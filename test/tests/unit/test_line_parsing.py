"""tests the vulture line parsing"""
#  pylint: disable=protected-access
from pathlib import Path

import pytest

from vulture.core import Item

from pytest_vulture.setup_manager import SetupManager


@pytest.mark.parametrize(
    "vulture_message,path",
    [
        (Item("test", "function", Path("src/test.py"), 15, 15, "unused function 'main'", 60), "src.test:main"),
        (Item("test", "function", Path("src/tutu.py"), 15, 15, "unused function 'tata'", 60), "src.tutu:tata"),
    ]
)
def test_python_path(vulture_message, path):

    assert SetupManager._python_path(vulture_message) == path
