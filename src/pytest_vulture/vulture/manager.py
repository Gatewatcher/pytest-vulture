"""Manages vulture"""
import re

from pathlib import Path
from typing import (
    List,
    Optional,
)

from vulture import Vulture
from vulture.core import Item

from pytest_vulture.conf.reader import IniReader
from pytest_vulture.setup_manager import SetupManager
from pytest_vulture.vulture.comment import CommentFinder


class VultureManager:
    """The vulture manager for pytest"""
    _results: List[Item]
    _config: IniReader
    _setup_manager: SetupManager
    _COMMENT_FINDER: CommentFinder = CommentFinder()

    def __init__(self, root_dir, config: IniReader):
        """Type of root_dir can be py._path.local.LocalPath. It depends on the version of pytest."""
        self.__root_dir = root_dir
        self._config = config
        self._results = []
        self.__setup_manager = SetupManager(self._config)

    def call(self):
        """Call vulture on a folder
        Example::
            >>> import py
            >>> from py._path.local import LocalPath
            >>> config = IniReader(path_ini=Path("vulture.ini"))
            >>> config.read_ini()
            >>> manager = VultureManager(LocalPath("/tmp"), config)
            >>> manager.call()
        """
        vulture_configuration = self._config.vulture_configuration
        vulture = Vulture(
            ignore_names=vulture_configuration.ignore_names,
            ignore_decorators=vulture_configuration.ignore_decorators
        )
        vulture.scavenge([str(self.__root_dir)], exclude=vulture_configuration.exclude)
        self._results = [elem for elem in vulture.get_unused_code() if not self.__filter_results(elem)]

    def get_file_errors(self, path) -> Optional[str]:
        """Get file errors
        Example::
            >>> import py
            >>> from pathlib import Path
            >>> from py._path.local import LocalPath
            >>> Path("/tmp/package").mkdir(exist_ok=True)
            >>> Path("/tmp/package/test.py").write_text("def test():pass")
            15
            >>> config = IniReader(path_ini=Path("vulture.ini"))
            >>> config.read_ini()
            >>> manager = VultureManager(LocalPath("/tmp/package"), config)
            >>> manager.call()
            >>> manager.get_file_errors(LocalPath("/tmp/package/test.py"))
            "line 1 : unused function 'test'"
        """
        errors = []
        for error_vulture in self._results:
            if self.__path_equals(path, error_vulture.filename.as_posix(), str(self.__root_dir)):
                errors.append(f"line {error_vulture.first_lineno} : {error_vulture.message}")
        if not errors:
            return None
        return "\n".join(errors)

    def __filter_results(self, vulture_output: Item) -> bool:
        """Check if the vulture output concerns an ignore path, an entry point or a # vulture: ignore"""
        for ignored_path in self._config.vulture_configuration.ignore:
            if self.__check_path(ignored_path, vulture_output.filename):
                return True
        return self.__setup_manager.is_entry_point(
            vulture_output
        ) or self.__check_ignore_type(
            vulture_output
        ) or self._COMMENT_FINDER.check_comment(
            vulture_output
        )

    def __check_path(self, path_exclude: str, path_to_check: Path) -> bool:
        match = re.compile(path_exclude.replace("*", ".*")).match(path_to_check.as_posix())
        if not match:
            return self.__path_equals(
                path_exclude, path_to_check.absolute().as_posix(), str(self.__root_dir)
            )
        return match.group() == path_to_check.as_posix()

    def __check_ignore_type(self, vulture_output: Item):
        return vulture_output.typ in self._config.vulture_configuration.ignore_types

    @classmethod
    def __path_equals(cls, path_1, path_2, root_dir: str) -> bool:
        """Manages tox and pytest weird path usages, to simplify"""
        path_1_full = (Path(root_dir) / Path(str(path_1))).as_posix()
        path_2_full = (Path(root_dir) / Path(str(path_2))).as_posix()
        return path_1_full == path_2_full
