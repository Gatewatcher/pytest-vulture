"""tests the setup parser system to find entry points"""
# pylint: disable=redefined-outer-name,use-implicit-booleaness-not-comparison
from unittest.mock import Mock

import pytest

from pytest_vulture.setup_manager import (
    EntryPointFileError,
    EntryPointFunctionError,
    SetupManager,
)
from pytest_vulture.vulture.output_line import VultureOutputLine


@pytest.mark.parametrize(
    "check_entry_points, setup,line,is_entry_point",
    [
        (False, "setup_with_entry_point", "src/test/main.py:8: unused function 'main' (60% confidence)", True),
        (False, "setup_with_entry_point", "src/test/main.py:8: unused function 'test' (60% confidence)", False),
        (False, "setup_with_entry_point", "src/swagger_parser/conf/base.py:8: unused property 'main' (60% confidence)",
         False),
        (True, "setup", "test/main.py:7: unused function 'main' (60% confidence)", True),
        (True, "setup", "src/test/main.py:7: unused function 'main' (60% confidence)", False),
        (False, "setup_broken", "main.py:7: unused function 'main' (60% confidence)", False),
        (False, "setup_no_entry_point", "main.py:7: unused function 'main' (60% confidence)", False),
        (False, "setup_not_found", "main.py:7: unused function 'main' (60% confidence)", False),
    ]
)
def test_is_entry_point(check_entry_points, examples_path, setup, line, is_entry_point):
    """tests the entry point checking system"""
    conf = Mock()
    conf.package_configuration.check_entry_points = check_entry_points
    conf.package_configuration.setup_path = examples_path / "setups" / setup
    setup_entry_point = SetupManager(conf)
    vulture = VultureOutputLine(line)

    assert setup_entry_point.is_entry_point(vulture) == is_entry_point


@pytest.mark.parametrize(
    "path,error",
    [
        ("setup_file_not_found", EntryPointFileError),
        ("setup_entry_p_not_found", EntryPointFunctionError),
    ]
)
def test_errors(examples_path, path, error):
    conf = Mock()
    conf.package_configuration.check_entry_points = True
    not_found_path = examples_path / "setups" / path
    conf.package_configuration.setup_path = not_found_path

    with pytest.raises(error):
        SetupManager(conf)
