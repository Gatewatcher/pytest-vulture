"""tests the vulture line parsing"""
import pytest

from pytest_vulture.vulture.output_line import VultureOutputLine


@pytest.mark.parametrize(
    "vulture_message,pytest_message",
    [
        (
            "src/test.py:15: unused function 'main' (60% confidence)",
            "line 15 :  unused function 'main' (60% confidence)",
        ),
        (
            "src/toto.py:14: unused function 'tata' (60% confidence)",
            "line 14 :  unused function 'tata' (60% confidence)",
        ),
        (
            "src/test.py unused function 'main' (60% confidence)",
            "src/test.py unused function 'main' (60% confidence)",
        ),
    ]
)
def test_messages(vulture_message, pytest_message):
    """Tests the message parsing of vulture output"""
    vulture_line = VultureOutputLine(vulture_message)

    assert vulture_line.message == pytest_message


@pytest.mark.parametrize(
    "vulture_message,path",
    [
        ("src/test.py:15: unused function 'main' (60% confidence)", "src/test.py"),
        ("src/tutu.py:15: unused function 'main' (60% confidence)", "src/tutu.py"),
    ]
)
def test_path(vulture_message, path):
    vulture_line = VultureOutputLine(vulture_message)

    assert vulture_line.path.as_posix() == path


@pytest.mark.parametrize(
    "vulture_message,path",
    [
        ("src/test.py:15: unused function 'main' (60% confidence)", "src.test:main"),
        ("src/tutu.py:15: unused function 'tata' (60% confidence)", "src.tutu:tata"),
    ]
)
def test_python_path(vulture_message, path):
    vulture_line = VultureOutputLine(vulture_message)

    assert vulture_line.python_path == path


@pytest.mark.parametrize(
    "vulture_message,type_vulture",
    [
        ("src/test.py:15: unused function 'main' (60% confidence)", "function"),
        ("src/tutu.py:15: error", ""),
    ]
)
def test_type(vulture_message, type_vulture):
    vulture_line = VultureOutputLine(vulture_message)

    assert vulture_line.type == type_vulture
    assert vulture_line.type == type_vulture


@pytest.mark.parametrize(
    "vulture_message,line_number",
    [
        ("src/test.py:1: unused function 'main' (60% confidence)", 1),
        ("src/test.py:15: unused function 'main' (60% confidence)", 15),
        ("error", None),
    ]
)
def test_line_number(vulture_message, line_number):
    vulture_line = VultureOutputLine(vulture_message)

    assert vulture_line.line_number == line_number
