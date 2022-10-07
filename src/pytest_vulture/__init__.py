"""The vulture pytest plugin code source"""

__all__ = ["VultureError"]


class VultureError(Exception):
    """Any pytest vulture exception"""
    __message: str
    _name = "vulture exception"

    def __init__(self, message: str = "An error occurred"):
        super().__init__(self)
        self.__message = message

    @property
    def message(self) -> str:  # pragma: no cover
        """Get the error message if it has one"""
        return self.__message

    def __str__(self):  # pragma: no cover
        return f"{self._name} : {self.message}"
