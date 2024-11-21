"""Tests the setup parser."""

from pathlib import Path
from unittest.mock import Mock

from vulture.core import Item

from pytest_vulture.setup_manager import SetupManager


_DATA = """[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools",
]

[project]
name = "test-tools"
version = "2.0.0a0"
requires-python = ">=3.9"
dynamic = [
  "dependencies",
]
[project.scripts]
test_api = "test_tools.cli.test:main"

[tool.setuptools.dynamic]
dependencies = {file = ["requirements/main.txt"]}
"""


def test_py_project(tmp_path):
    setup = tmp_path / "pyproject.toml"
    test_tools = tmp_path / "test_tools/cli"
    test_tools.mkdir(parents=True)
    (test_tools / "test.py").write_text("def main()", encoding="utf-8")
    setup.write_text(_DATA, encoding="utf-8")
    mock = Mock()
    mock.package_configuration.setup_path = setup
    mock.package_configuration.source_path = tmp_path
    setup = SetupManager(mock)

    assert setup._entry_points == ["test_tools.cli.test:main"]
    assert setup.is_entry_point(Item("test", "function", Path("toto.py"), 1, 1, "unused function 'main'", 50)) is False
    assert (
        setup.is_entry_point(
            Item(
                "test",
                "function",
                Path("test_tools/cli/test.py"),
                1,
                1,
                "unused function 'main'",
                50,
            )
        )
        is True
    )
