"""The package configuration"""
from configparser import ConfigParser
from contextlib import suppress
from pathlib import Path

from pytest_vulture.conf.base import Configuration


class PackageConfiguration(Configuration):
    """The package configuration (setup.py options)
    Examples::
        >>> config_file = Path("/tmp/test.ini")
        >>> config_file.write_text("[package]\\nsetup_path = setup.py\\ncheck_entry_points = true")
        57
        >>> config = ConfigParser()
        >>> config.read(Path(config_file))
        ['/tmp/test.ini']
        >>> package_config = PackageConfiguration()
        >>> package_config.read_ini(config)
        >>> package_config.setup_path
        PosixPath('setup.py')
        >>> package_config.check_entry_points
        True
    """
    _setup_path: Path = Path("setup.py")
    _source_path: Path = Path("")
    _check_entry_points: bool = True
    _NAME = "package"

    @property
    def setup_path(self) -> Path:
        return self._setup_path

    @property
    def source_path(self) -> Path:
        return self._source_path

    @property
    def check_entry_points(self) -> bool:
        return self._check_entry_points

    def read_ini(self, config: ConfigParser):
        """Read the ini file"""
        with suppress(KeyError):
            self._setup_path = Path(config[self._NAME]['setup_path'])
        with suppress(KeyError):
            self._source_path = Path(config[self._NAME]['source_path'])
        with suppress(KeyError):
            self._check_entry_points = self._to_bool(
                config[self._NAME]['check_entry_points']
            )
