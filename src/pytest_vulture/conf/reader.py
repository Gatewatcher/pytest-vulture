"""The full configuration manager"""
from configparser import ConfigParser
from pathlib import Path

from pytest_vulture.conf.package import PackageConfiguration
from pytest_vulture.conf.vulture import VultureConfiguration


class IniReader:
    """The full configuration parser
     Examples::
        >>> config_file = Path("/tmp/test.ini")
        >>> config_file.write_text("[package]\\nsetup_path = custom.py\\n[vulture]\\nignore-names = test")
        62
        >>> package_config = IniReader(Path("/tmp/test.ini"))
        >>> package_config.read_ini()
        >>> package_config.package_configuration.setup_path
        PosixPath('custom.py')
        >>> package_config.vulture_configuration.ignore_names
        ['test']
    """
    _vulture_configuration: VultureConfiguration
    _package_configuration: PackageConfiguration
    _path_ini: Path

    def __init__(self, path_ini: Path = Path("vulture.ini")):
        self._path_ini = path_ini
        self._vulture_configuration = VultureConfiguration()
        self._package_configuration = PackageConfiguration()

    @property
    def package_configuration(self) -> PackageConfiguration:
        return self._package_configuration

    @property
    def vulture_configuration(self) -> VultureConfiguration:
        return self._vulture_configuration

    def read_ini(self):
        """Read and parse the ini file"""
        if self._path_ini.is_file():
            config = ConfigParser()
            config.read(self._path_ini)
            self._vulture_configuration.read_ini(config)
            self._package_configuration.read_ini(config)
