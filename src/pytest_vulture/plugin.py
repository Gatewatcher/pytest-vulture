# -*- coding: utf-8 -*-
"""Pytest vulture plugins"""
# pylint: disable=subclassed-final-class
from pathlib import Path

import pytest

from _pytest.main import Session

from pytest_vulture import VultureError
from pytest_vulture.conf.reader import IniReader
from pytest_vulture.vulture.manager import VultureManager


def pytest_addoption(parser):
    """Add all the pytest vulture command line options"""
    group = parser.getgroup("general")
    # Set the --vulture option in the setup.py
    group.addoption(
        '--vulture', action='store_true', help="run vulture"
    )
    group.addoption(
        '--vulture-cfg-file', help="Defines the vulture config file path",
        default="tox.ini",
    )


def pytest_sessionstart(session):
    """Call vulture only at the start, before entering the run test loop."""
    config = session.config
    if config.option.vulture:
        root_dir = session.startdir
        reader = IniReader(path_ini=Path(config.option.vulture_cfg_file))
        reader.read_ini()
        session.vulture = VultureManager(root_dir, reader)
        session.vulture.call()


def pytest_collect_file(file_path, parent):
    """Search and apply the vulture result (run at the session start) on the python file"""
    config = parent.config
    if config.option.vulture and file_path.suffix == '.py':
        return VulturePinningFile.from_parent(parent=parent, path=file_path)
    return None


class _VultureSession(Session):  # type: ignore
    vulture: VultureManager


class VultureItem(pytest.Item):
    """vulture pytest running class."""
    session: _VultureSession

    def runtest(self):
        """Raise an error if a vulture message occurred in the tested file."""
        error_message = self.session.vulture.get_file_errors(self.fspath)
        if error_message:
            raise VultureError(message=error_message)

    def repr_failure(self, excinfo, *args, **kwargs):  # pylint: disable=signature-differs
        """If VultureError is raised, it means that a vulture message occurred in the tested file."""
        if excinfo.errisinstance(VultureError):
            return excinfo.value.message
        return super().repr_failure(excinfo, *args, **kwargs)

    def reportinfo(self):
        """Generate the vulture test report"""
        return self.path, None, f"[vulture] {self.path}"

class VulturePinningFile(pytest.File):
    """File that is tested by pytest"""

    def collect(self):
        yield VultureItem.from_parent(parent=self, name="vulture")
