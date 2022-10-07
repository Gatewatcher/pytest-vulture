"""The client pytest vulture configuration"""
from configparser import ConfigParser
from contextlib import suppress
from typing import List

from pytest_vulture.conf.base import Configuration


class VultureConfiguration(Configuration):
    """The vulture configuration (setup.py options)
    Examples::
        >>> from pathlib import Path
        >>> config_file = Path("/tmp/test.ini")
        >>> config_file.write_text("[vulture]\\nignore-decorators = @test")
        35
        >>> config = ConfigParser()
        >>> config.read(Path(config_file))
        ['/tmp/test.ini']
        >>> package_config = VultureConfiguration()
        >>> package_config.read_ini(config)
        >>> package_config.ignore_decorators
        ['@test']
    """
    EXCLUDE_DEFAULT: List[str] = [
        "*/.tox/*", "*/.git/*", "*/.cache/*", "*/.idea/*", "*/.eggs/*"
    ]
    _exclude: List[str] = EXCLUDE_DEFAULT
    _CONFIG_NAME: str = "vulture"
    _ignore_names: List[str]
    _ignore_decorators: List[str]
    _ignore: List[str]
    _ignore_types: List[str]

    def __init__(self):
        super().__init__()
        self._ignore_names: List[str] = []
        self._ignore_decorators: List[str] = []
        self._ignore: List[str] = []
        self._ignore_types: List[str] = []

    @property
    def ignore_types(self) -> List[str]:
        return self._ignore_types

    @property
    def ignore(self) -> List[str]:
        return self._ignore

    @property
    def ignore_decorators(self) -> List[str]:
        return self._ignore_decorators

    @property
    def ignore_names(self) -> List[str]:
        return self._ignore_names

    @property
    def exclude(self) -> List[str]:
        return self._exclude

    def read_ini(self, config: ConfigParser):
        """Read the ini file"""
        with suppress(KeyError):
            self._exclude = self.EXCLUDE_DEFAULT + self._to_list(
                config[self._CONFIG_NAME]['exclude']
            )

        self.__read_ignore(config)

    def __read_ignore(self, config: ConfigParser):
        with suppress(KeyError):
            self._ignore_names = self._to_list(
                config[self._CONFIG_NAME]['ignore-names']
            )
        with suppress(KeyError):
            self._ignore_decorators = self._to_list(
                config[self._CONFIG_NAME]['ignore-decorators']
            )

        with suppress(KeyError):
            self._ignore = self._to_list(
                config[self._CONFIG_NAME]['ignore']
            )

        with suppress(KeyError):
            self._ignore_types = self._to_list(
                config[self._CONFIG_NAME]['ignore-types']
            )
