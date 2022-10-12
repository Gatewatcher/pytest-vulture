"""Manages what functions prints"""
# mypy: ignore-errors
import sys

from typing import List


class PrintParser:
    """A class that get the printing of methods
        Example::
            >>> log = PrintParser()
            >>> log.start()
            >>> print("toto")
            >>> print("tata")
            >>> log.stop()
            >>> print("tutu")
            tutu
            >>> log.messages
            'toto\\ntata\\n'

    """
    stdout = sys.stdout

    _messages: List[str] = []
    message = ""

    def start(self):
        """Starting to save the prints and not show them in the console"""
        self.stdout = sys.stdout
        sys.stdout = self
        self._messages = []

    def stop(self):
        """Stop saving the prints"""
        sys.stdout = self.stdout

    def getvalue(self):
        """hacks"""
        return self.message

    def write(self, text):
        """Does not write the text in the console, but saves it"""
        self._messages.append(text)

    @property
    def messages(self) -> str:
        """Get the printed outputs in a string"""
        return "".join(self._messages)
