"""A pytest vulture configuration"""
import re

from abc import (
    ABC,
    abstractmethod,
)
from configparser import ConfigParser
from typing import List


class Configuration(ABC):
    """The abstract class of a pytest vulture configuration"""
    _TRUE_VALUES = ["true", "True", "1", "yes"]

    @abstractmethod
    def read_ini(self, config: ConfigParser) -> bool:
        """Read the ini file"""

    @staticmethod
    def _to_list(config_string: str) -> List[str]:
        """Convert a string config element to a list
           Examples::
                >>> Configuration._to_list(" */test/*\\n */test_2/*")
                ['*/test/*', '*/test_2/*']
        """
        list_elements = re.split('[,\n]', config_string)
        return [element.lstrip().rstrip() for element in list_elements if element.lstrip().rstrip()]

    @classmethod
    def _to_bool(cls, config_string: str) -> bool:
        return config_string in cls._TRUE_VALUES
