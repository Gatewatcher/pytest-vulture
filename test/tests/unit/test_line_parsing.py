"""tests the vulture line parsing."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from vulture.core import Item

from pytest_vulture.setup_manager import SetupManager


@pytest.mark.parametrize(
    ("vulture_message", "path"),
    [
        (
            Item(
                "test",
                "function",
                Path("src/test.py"),
                15,
                15,
                "unused function 'main'",
                60,
            ),
            "src.test:main",
        ),
        (
            Item(
                "test",
                "function",
                Path("src/tutu.py"),
                15,
                15,
                "unused function 'tata'",
                60,
            ),
            "src.tutu:tata",
        ),
    ],
)
def test_python_path(vulture_message, path, tmp_path):
    mock = Mock()
    mock.package_configuration.source_path = Path()
    mock.package_configuration.setup_path = tmp_path
    assert SetupManager(mock)._python_path(vulture_message) == path
