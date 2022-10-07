"""tests vulture_manager.py"""
# pylint: disable=protected-access,too-many-arguments
from unittest.mock import patch

import pytest

from vulture import Vulture

from pytest_vulture.conf.reader import IniReader
from pytest_vulture.vulture.manager import VultureManager
from pytest_vulture.vulture.output_line import VultureOutputLine
from pytest_vulture.vulture.print_parser import PrintParser


@pytest.mark.parametrize(
    "messages,size,ignore_path",
    [
        ("path.py:8: message", 1, "not_path.py"),
        ("", 0, "path.py"),
        ("path.py:8: message", 0, "path.py"),
    ]
)
@patch.object(Vulture, "report")
@patch.object(Vulture, "scavenge")
def test_call(scavenge, report, monkeypatch, tmp_path, messages, size, ignore_path):
    """Tests the vulture call"""
    config_file = tmp_path / "test"
    config_file.write_text(f"""
[vulture],
ignore = 
    {ignore_path}
    """)
    config = IniReader(config_file)
    config.read_ini()
    manager = VultureManager(tmp_path / "test.py", config)
    monkeypatch.setattr(PrintParser, "messages", messages)

    manager.call()

    assert scavenge.called is True
    assert report.called is True
    assert len(manager._results) == size
    if size:
        assert manager._results[0].message == "line 8 :  message"


@pytest.mark.parametrize(
    "results,file,answer",
    [
        ([], "test.py", None),
        ([VultureOutputLine("src/test.py:8: test")], "not_test.py", None),
        ([VultureOutputLine("src/test.py:8: test")], "test.py", None),
        ([VultureOutputLine("src/test.py:8: test")], "src/test.py", "line 8 :  test"),
    ]
)
def test_get_file_errors(tmp_path, results, file, answer):
    """Tests the getting file"""
    manager = VultureManager(tmp_path / "test2", IniReader(tmp_path / "test"))
    manager._results = results

    assert manager.get_file_errors(file) == answer
