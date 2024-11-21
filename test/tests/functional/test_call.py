"""tests the configuration system."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from pytest_vulture.vulture.manager import VultureManager


@pytest.mark.parametrize(
    ("folder_path", "results"),
    [
        ("vulture_tests/comments", 0),
        ("vulture_tests/bug_18_2020", 0),
        ("vulture_tests/easy", 1),
    ],
)
def test_with_comments(examples_path, folder_path, results):
    """Tests the call function with comments to see if the vulture ignore disables the outputs."""
    ini = Mock()
    ini.package_configuration.setup_path = Path("not_found.py")
    ini.vulture_configuration.exclude = []
    ini.vulture_configuration.ignore_names = []
    ini.vulture_configuration.ignore_decorators = []
    ini.vulture_configuration.ignore = []
    ini.vulture_configuration.ignore_types = []
    manager = VultureManager(examples_path / folder_path, ini)

    manager.call()

    assert len(manager._results) == results


@pytest.mark.parametrize(
    ("exclude", "ignore", "ignore_names", "ignore_decorators", "ignore_types", "results", "answer"),
    [
        ([], [], [], [], [], 1, "unused property 'main'"),
        ([".py"], [], [], [], [], 0, []),
        (["main.py"], [], [], [], [], 1, "unused function 'other'"),
        ([], ["main.py"], [], [], [], 0, []),
        ([], ["*.py"], [], [], [], 0, []),
        ([], ["easy/main.py"], [], [], [], 1, "unused property 'main'"),
        ([], [], ["main"], [], [], 0, []),
        ([], [], [], ["@property"], [], 0, []),
        ([], [], [], [], ["property"], 0, []),
    ],
)
def test_call(
    examples_path,
    exclude,
    ignore,
    ignore_names,
    ignore_decorators,
    ignore_types,
    results,
    answer,
):
    """Tests the call option with vulture with the easy example."""
    ini = Mock()
    ini.package_configuration.setup_path = Path("not_found.py")
    ini.vulture_configuration.exclude = exclude
    ini.vulture_configuration.ignore_names = ignore_names
    ini.vulture_configuration.ignore_decorators = ignore_decorators
    ini.vulture_configuration.ignore = ignore
    ini.vulture_configuration.ignore_types = ignore_types
    manager = VultureManager(examples_path / "vulture_tests/easy", ini)

    manager.call()

    assert len(manager._results) == results
    if results:
        assert manager._results[0].message == answer
