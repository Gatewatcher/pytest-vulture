"""The full configuration manager."""

import sys
from configparser import ConfigParser
from pathlib import Path


if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

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

    _is_pyproject: bool

    _vulture_configuration: VultureConfiguration
    _package_configuration: PackageConfiguration
    _path_ini: Path

    def __init__(self, path_ini: Path = Path("vulture.ini"), *, is_pyproject: bool = False) -> None:
        self._path_ini = path_ini
        self._vulture_configuration = VultureConfiguration(is_pyproject=is_pyproject)
        self._package_configuration = PackageConfiguration(is_pyproject=is_pyproject)
        self._is_pyproject = is_pyproject

    @property
    def package_configuration(self) -> PackageConfiguration:
        return self._package_configuration

    @property
    def vulture_configuration(self) -> VultureConfiguration:
        return self._vulture_configuration

    def read_ini(self) -> None:
        """Read and parse the ini file."""
        if self._path_ini.is_file():
            if self._is_pyproject:
                with self._path_ini.open("rb") as file:
                    pyproject_data = tomllib.load(file)
                self._vulture_configuration.read_tomli(pyproject_data)
                self._package_configuration.setup_path = self._path_ini
                self._package_configuration.read_tomli(pyproject_data)

            else:
                config = ConfigParser()
                config.read(self._path_ini)
                self._vulture_configuration.read_ini(config)
                self._package_configuration.read_ini(config)
