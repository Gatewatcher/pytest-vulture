"""tests the setup parser system to find entry points."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from vulture.core import Item

from pytest_vulture.setup_manager import (
    EntryPointFileError,
    EntryPointFunctionError,
    SetupManager,
)


@pytest.mark.parametrize(
    ("check_entry_points", "setup", "message", "file", "first_lineno", "is_entry_point"),
    [
        (
            False,
            "setup_with_entry_point",
            "unused function 'main'",
            "src/test/main.py",
            8,
            True,
        ),
        (
            False,
            "setup_with_entry_point",
            "unused function 'test'",
            "src/test/main.py",
            8,
            False,
        ),
        (
            False,
            "setup_with_entry_point",
            "unused property 'main'",
            "src/swagger_parser/conf/base.py",
            8,
            False,
        ),
        (True, "setup", "unused function 'main'", "test/main.py", 7, True),
        (True, "setup", "unused function 'main'", "src/ttest/main.py", 7, False),
        (False, "setup_broken", "unused function 'main'", "main.py", 7, False),
        (False, "setup_no_entry_point", "unused function 'main'", "main.py", 7, False),
        (False, "setup_not_found", "unused function 'main'", "main.py", 7, False),
    ],
)
def test_is_entry_point(
    check_entry_points,
    examples_path,
    setup,
    message,
    file,
    first_lineno,
    is_entry_point,
):
    """Tests the entry point checking system."""
    conf = Mock()
    conf.package_configuration.check_entry_points = check_entry_points
    conf.package_configuration.setup_path = examples_path / "setups" / setup
    conf.package_configuration.source_path = Path()
    setup_entry_point = SetupManager(conf)
    vulture = Item("test", "function", Path(file), first_lineno, first_lineno, message, 50)

    assert setup_entry_point.is_entry_point(vulture) == is_entry_point


@pytest.mark.parametrize(
    ("path", "error"),
    [
        ("setup_file_not_found", EntryPointFileError),
        ("setup_entry_p_not_found", EntryPointFunctionError),
    ],
)
def test_errors(examples_path, path, error):
    conf = Mock()
    conf.package_configuration.check_entry_points = True
    not_found_path = examples_path / "setups" / path
    conf.package_configuration.source_path = Path()
    conf.package_configuration.setup_path = not_found_path

    with pytest.raises(error):
        SetupManager(conf)
