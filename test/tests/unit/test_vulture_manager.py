"""tests vulture_manager.py."""

from pathlib import Path

import pytest
from vulture.core import Item

from pytest_vulture.conf.reader import IniReader
from pytest_vulture.vulture.manager import VultureManager


@pytest.mark.parametrize(
    ("results", "file", "answer"),
    [
        ([], "test.py", None),
        (
            [
                Item(
                    "test",
                    "function",
                    Path("src/test.py"),
                    8,
                    8,
                    "unused function 'test'",
                    50,
                )
            ],
            "not_test.py",
            None,
        ),
        (
            [
                Item(
                    "test",
                    "function",
                    Path("src/test.py"),
                    8,
                    8,
                    "unused function 'test'",
                    50,
                )
            ],
            "test.py",
            None,
        ),
        (
            [
                Item(
                    "test",
                    "function",
                    Path("src/test.py"),
                    8,
                    8,
                    "unused function 'test'",
                    50,
                )
            ],
            "src/test.py",
            "line 8 : unused function 'test'",
        ),
        (
            [
                Item(
                    "test",
                    "function",
                    Path("src/test.py"),
                    9,
                    9,
                    "unused function 'toto'",
                    50,
                )
            ],
            "src/test.py",
            "line 9 : unused function 'toto'",
        ),
    ],
)
def test_get_file_errors(tmp_path, results, file, answer):
    """Test the getting file."""
    manager = VultureManager(tmp_path / "test2", IniReader(tmp_path / "test", is_pyproject=False))
    manager._results = results

    assert manager.get_file_errors(file) == answer
