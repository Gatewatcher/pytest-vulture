"""Manages vulture output lines"""
import re

from pathlib import Path
from typing import Optional


class VultureOutputLine:
    """A vulture output line
        Examples::
            >>> manager = VultureOutputLine("src/test.py:2: unused function 'test' (60% confidence)")
            >>> manager.line_number
            2
            >>> manager.message
            "line 2 :  unused function 'test' (60% confidence)"
            >>> manager.path
            PosixPath('src/test.py')
            >>> manager.python_path
            'src.test:test'
            >>> manager.type
            'function'
    """
    _message: str
    _type: str = ""
    _path: Path
    _line_number: int = -1
    _UNUSED_FUNCTION_MESSAGE = "unused function"
    _python_path: str = ""

    def __init__(self, line: str):
        splitter = line.split(":")
        self._path = Path(splitter[0])
        self._message = splitter[-1]
        try:
            self._line_number = int(splitter[1])
        except (ValueError, IndexError):
            self._line_number = -1

    @property
    def type(self) -> str:
        """get the type : function, attribute, property ...
            Examples::
                >>> VultureOutputLine("src/test.py:2: unused function 'test' (60% confidence)").type
                'function'
        """
        if not self._type:
            elements = re.findall("unused [a-z]*", self._message)
            if elements:
                self._type = elements[0].replace("unused ", "")
        return self._type

    @property
    def line_number(self) -> Optional[int]:
        """Get the vulture message line number
            Examples::
                >>> VultureOutputLine("src/test.py:5: unused function 'test' (60% confidence)").line_number
                5
        """
        if self._line_number == -1:
            return None
        return self._line_number

    @property
    def message(self) -> str:
        """Get the vulture message
             Examples::
                >>> VultureOutputLine("src/test.py:5: unused function 'test' (60% confidence)").message
                "line 5 :  unused function 'test' (60% confidence)"
        """
        if self._line_number == -1:
            return self._message
        return f"line {self._line_number} : {self._message}"

    @property
    def path(self) -> Path:
        """Get file path of the vulture message
             Examples::
                >>> VultureOutputLine("src/test.py:5: unused function 'test' (60% confidence)").path
                PosixPath('src/test.py')
        """
        return self._path

    @property
    def python_path(self) -> str:
        """Get the python path of the vulture message :
            Examples::
                >>> VultureOutputLine("src/test.py:5: unused function 'test' (60% confidence)").python_path
                'src.test:test'
        """
        if not self._python_path:
            try:
                relative_path = self.path.relative_to(Path("").absolute())
            except ValueError:
                relative_path = self.path

            self._python_path = relative_path.as_posix().replace("/", ".").replace(".py", "")
            dots_message = f"{self._UNUSED_FUNCTION_MESSAGE} '"
            find = re.findall(
                f"(?={dots_message}).*(?<=')", self._message
            )
            if find:
                function_name = find[0].replace(dots_message, "")
                self._python_path += ":" + function_name[:-1]
        return self._python_path

    def __str__(self):  # pragma: no cover
        return self.message
