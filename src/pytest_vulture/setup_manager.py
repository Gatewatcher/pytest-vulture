"""Manages the setup.py to get the entrypoint (and ignore then for vulture)"""
# pylint: disable=eval-used
import re

from contextlib import suppress
from pathlib import Path
from typing import (
    List,
    Tuple,
)

from vulture.core import Item

from pytest_vulture import VultureError
from pytest_vulture.conf.reader import IniReader


class EntryPointFileError(VultureError):
    _name = "an entry point file is missing in the setup.py file"


class EntryPointFunctionError(VultureError):
    _name = "an entry point function is missing in the setup.py file"


class SetupManager:
    """The setup.py parser"""
    _entry_points: List[str]
    _config: IniReader
    _UNUSED_FUNCTION_MESSAGE = "unused function"
    _PY_PROJECT = "[project.scripts]"

    def __init__(self, config: IniReader):
        self._entry_points = []
        self._config = config
        try:
            content = self._config.package_configuration.setup_path.read_text("utf-8").replace("\n", "")
        except (OSError, ValueError):
            return
        self._generate_entry_points(content)

    def is_entry_point(self, vulture: Item) -> bool:
        """Check if the vulture output is an entry point
        Examples::
            >>> config_file = Path("/tmp/test.ini")
            >>> config_file.write_text("[package]\\nsetup_path = /tmp/setup.py")
            36
            >>> ini = IniReader(config_file)
            >>> ini.read_ini()
            >>> Path("/tmp/setup.py").write_text("entry_points={'console_scripts': ('test=test:main', )}")
            54
            >>> Path("/tmp/test.py").write_text("def main():pass")
            15
            >>> finder = SetupManager(ini)
            >>> finder.is_entry_point(Item("test", "function", Path("toto.py"), 1, 1, "unused function 'test'", 50))
            False
            >>> finder.is_entry_point(Item("test", "function", Path("test.py"), 1, 1, "unused function 'main'", 50))
            True
        """
        for entry_point in self._entry_points:
            if entry_point.replace(".__init__", "") == self._python_path(vulture).replace(".__init__", ""):
                return True
        return False

    def _python_path(self, vulture: Item):
        try:
            relative_path = vulture.filename.relative_to(self._get_dir_path().absolute())
        except ValueError:
            relative_path = vulture.filename

        python_path = relative_path.as_posix().replace("/", ".").replace(".py", "")
        dots_message = f"{self._UNUSED_FUNCTION_MESSAGE} '"
        find = re.findall(f"(?={dots_message}).*(?<=')", vulture.message)
        if find:
            function_name = find[0].replace(dots_message, "")
            python_path += ":" + function_name[:-1]
        return python_path

    def _find_py_project_toml(self, content: str):
        """We do not want to add a toml dependency for now."""
        entry_points  = content.split(self._PY_PROJECT, 1)[1].split("[", 1)[0].split("\n")
        entry_points = [entry_point for entry_point in entry_points if  entry_point]
        for entry_point in entry_points:
            self.__parse_entry_point_line(entry_point.replace(" ", "").replace('"', ""), [])
        return ""

    def _generate_entry_points(self, content: str):
        """Parse the setup.pu file to get the entry points"""
        if self._PY_PROJECT in content:
            self._find_py_project_toml(content)
            return
        root_paths = self.__generate_root_paths(content)
        entry_points = {}
        find = re.findall("(?=entry_points={).*(?<=})", content.replace("\n", ""))
        if find:
            element = find[0]
            element = element[:element.find("}") + 1]
            with suppress(SyntaxError):
                entry_points = eval(element.replace("entry_points=", ""))
        for values in entry_points.values():
            for equality in values:
                self.__parse_entry_point_line(equality, root_paths)

    def __parse_entry_point_line(self, equality: str, root_paths: List[Tuple[str, str]]):
        """Parse an entry point value to get the entry point path"""
        equality_split = equality.split("=")
        if len(equality_split) != 2:
            value = equality
        else:
            value = equality_split[1]
        if not root_paths:
            self._entry_points.append(value)
        else:
            for target, destination in root_paths:
                if len(value) > len(target) and value[:len(target)] == target:
                    self._entry_points.append(
                        destination + "." + value[len(target):]
                    )
                else:  # pragma: no cover
                    self._entry_points.append(value)
        self.__check_entry_points()

    def _get_dir_path(self) -> Path:
        source_path = self._config.package_configuration.source_path
        dir_path = self._config.package_configuration.setup_path.absolute().parent
        return dir_path / source_path

    def __check_entry_points(self):
        """Checks if the entry points exists"""
        if not self._config.package_configuration.check_entry_points:
            return
        for entry_points in self._entry_points:
            try:
                split_points = entry_points.split(":")
                function_name = split_points[1]
                path_dots = split_points[0]
            except IndexError:
                continue
            dir_path = self._get_dir_path()
            new_path = Path(path_dots.replace(".", "/"))
            if (dir_path / new_path).is_dir():  # pragma: no cover
                path = (dir_path / new_path / "__init__.py").absolute()
            else:
                path = (dir_path / (str(new_path) + ".py")).absolute()
            if not path.exists():
                raise EntryPointFileError(
                    message=f"{path.as_posix()} can not be found."
                )
            with path.open() as file:
                content = file.read()
                if f"def{function_name}(" not in content.replace(" ", ""):
                    raise EntryPointFunctionError(
                        message=f"{entry_points} can not be found."
                    )

    @staticmethod
    def __generate_root_paths(content: str) -> List[Tuple[str, str]]:
        """Parse the setup.py to get the source root paths"""
        root_paths: List[Tuple[str, str]] = []
        package_dir = {}
        find = re.findall("(?=package_dir={).*(?<=})", content.replace("\n", ""))
        if find:
            element = find[0]
            element = element[:element.find("}") + 1]
            with suppress(SyntaxError):
                package_dir = eval(element.replace("package_dir=", ""))
        for key, value in package_dir.items():
            root_paths.append((key, value))
        return root_paths
