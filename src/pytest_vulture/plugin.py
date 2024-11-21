"""Pytest vulture plugins."""

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Optional, Tuple, Union

import pytest
from _pytest.main import Session

from pytest_vulture import VultureError
from pytest_vulture.conf.reader import IniReader
from pytest_vulture.conf.vulture import VultureConfiguration
from pytest_vulture.vulture.manager import VultureManager


if TYPE_CHECKING:
    from _pytest.config.argparsing import Parser
    from _pytest.nodes import Collector, Item
    from _pytest.python import Package
    from py._code.code import ExceptionInfo, TerminalRepr


def pytest_addoption(parser: "Parser") -> None:
    """Add all the pytest vulture command line options."""
    group = parser.getgroup("general")
    # Set the --vulture option in the setup.py
    group.addoption("--vulture", action="store_true", help="run vulture")
    group.addoption(
        "--vulture-cfg-file",
        help="Defines the vulture config file path",
        default="",
    )


def pytest_sessionstart(session: "_VultureSession") -> None:
    """Call vulture only at the start, before entering the run test loop."""
    config = session.config
    if config.option.vulture:
        root_dir: Path = session.startdir
        vulture_cfg_file = config.option.vulture_cfg_file
        config_path, is_py = (Path(vulture_cfg_file), False) if vulture_cfg_file else _find_cfg_path()
        reader = IniReader(path_ini=config_path, is_pyproject=is_py)
        reader.read_ini()
        session.vulture = VultureManager(root_dir, reader)
        session.vulture.call()


def pytest_collect_file(file_path: Path, parent: "Package") -> "Optional[VulturePinningFile]":
    """Search and apply the vulture result (run at the session start) on the python file."""
    config = parent.config
    if config.option.vulture and file_path.suffix == ".py":
        answer: VulturePinningFile = VulturePinningFile.from_parent(parent=parent, path=file_path)
        return answer
    return None


class _VultureSession(Session):  # type: ignore[misc]
    vulture: VultureManager
    startdir: Path


class VultureItem(pytest.Item):
    """vulture pytest running class."""

    session: _VultureSession

    def runtest(self) -> None:
        """Raise an error if a vulture message occurred in the tested file."""
        error_message = self.session.vulture.get_file_errors(str(self.fspath))
        if error_message:
            raise VultureError(message=error_message)

    def repr_failure(self, excinfo: "ExceptionInfo", *args, **kwargs) -> "Union[str, TerminalRepr]":
        """If VultureError is raised, it means that a vulture message occurred in the tested file."""
        if excinfo.errisinstance(VultureError):
            answer: str = excinfo.value.message
            return answer
        return super().repr_failure(excinfo, *args, **kwargs)

    def reportinfo(self) -> "Tuple[Path, None, str]":
        """Generate the vulture test report."""
        return self.path, None, f"[vulture] {self.path}"


class VulturePinningFile(pytest.File):
    """File that is tested by pytest."""

    def collect(self) -> "Iterable[Union[Item, Collector]]":
        """Probably useless."""
        yield VultureItem.from_parent(parent=self, name="vulture")


def _find_cfg_path() -> Tuple[Path, bool]:
    with suppress(OSError):
        if VultureConfiguration.CONFIG_PYPROJECT_NAME in Path("pyproject.toml").read_text():
            return Path("pyproject.toml"), True

        for path_str in ("tox.ini", "vulture.ini"):
            path = Path(path_str)
            if path.is_file() and VultureConfiguration.CONFIG_NAME in path.read_text():
                return Path(path_str), False
    return Path("tox.ini"), False
