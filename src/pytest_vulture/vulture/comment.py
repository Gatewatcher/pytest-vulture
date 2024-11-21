"""Manages vulture: ignore in source code."""

import ast
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from vulture.core import Item


if TYPE_CHECKING:
    from _ast import AST


class CommentFinder:
    """Parse python code to find vulture: ignore comments."""

    _tree = None
    _content: str = ""
    _ignored_lines: List[int]
    _path: Path
    _VULTURE_IGNORE = "vulture: ignore"

    def __init__(self) -> None:
        self._path = Path()
        self._ignored_lines = []

    def check_comment(self, vulture: Item) -> bool:
        """Check if the vulture output line is ignored with a # vulture: ignore comment
        Examples::
           >>> Path("/tmp/test.py").write_text("def test():pass")
           15
           >>> finder = CommentFinder()
           >>> finder.check_comment(Item("test", "function", Path("/tmp/test.py"), 1, 1, "unused function 'test'", 50))
           False
           >>> Path("/tmp/test.py").write_text('def test():  # vulture: ignore\\n     pass')
           40
           >>> finder = CommentFinder()  # the file has changed, must recreate the instance
           >>> finder.check_comment(Item("test", "function", Path("/tmp/test.py"), 1, 1, "unused function 'test'", 50))
           True
           >>> finder.check_comment(Item("test", "function", Path("/tmp/test.py"), 3, 3, "unused function 'test'", 50))
           False
        """
        line_number = vulture.first_lineno
        if line_number is None:  # pragma: no cover
            return False
        # Check if is the same file as before, if not, reload
        if vulture.filename.as_posix() != self._path.as_posix():
            self.__reset(vulture.filename)
        return self.__find_rec(vulture)

    def __find_rec(self, vulture: Item, tree: "Optional[AST]" = None, *, ignore_mode: bool = False) -> bool:
        """Find comments recursively."""
        if tree is None:
            tree = self._tree
        if tree is None:  # pragma: no cover
            return False
        with suppress(AttributeError):
            line_nb: int = getattr(tree, "lineno")  # noqa: B009
            if not ignore_mode and line_nb in self._ignored_lines:
                ignore_mode = True
            if ignore_mode and vulture.first_lineno in [
                line_nb,
                line_nb - self.__get_decorators(tree),
            ]:
                return True
        with suppress(AttributeError):
            for new_tree in tree.body:  # type: ignore[attr-defined]
                if self.__find_rec(vulture, tree=new_tree, ignore_mode=ignore_mode):
                    return True
        with suppress(AttributeError):
            for new_tree in tree.orelse:  # type: ignore[attr-defined]
                if self.__find_rec(vulture, tree=new_tree, ignore_mode=ignore_mode):
                    return True
        return False

    @staticmethod
    def __get_decorators(tree: "Optional[AST]") -> int:
        if tree is None:  # pragma: no cover
            return 0
        try:
            return len(tree.decorator_list)  # type: ignore[attr-defined]
        except AttributeError:
            return 0

    def __reset(self, path: Path) -> None:
        self._path = path
        self._ignored_lines = []
        try:
            self._content = self._path.read_text(encoding="utf-8-sig")
            self._tree = ast.parse(self._content)
            content_split = self._content.split("\n")
            for index_line, elem in enumerate(content_split):
                if self._VULTURE_IGNORE in elem:
                    self._ignored_lines.append(index_line + 1)

        except OSError as err:  # pragma: no cover
            print(f"warning : unable to read : {self._path.as_posix()} : {err}")  # noqa: T201
            self._content = ""
