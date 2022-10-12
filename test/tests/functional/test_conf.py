"""tests the configuration system"""
# pylint: disable=redefined-outer-name
from pathlib import Path

from pytest_vulture.conf.reader import IniReader


def test_read_full_ini(examples_path):
    """Tests with the full.ini example"""
    reader = IniReader(Path(examples_path / "ini/full.ini"))

    reader.read_ini()
    exclude = reader.vulture_configuration.exclude

    assert len(exclude) == 3 + len(reader.vulture_configuration.EXCLUDE_DEFAULT)
    assert "*/test/*" in exclude
    assert "*/test_2/*" in exclude
    assert "*/test_3/*" in exclude
    assert reader.vulture_configuration.ignore_names == ["clean_"]
    assert reader.vulture_configuration.ignore_decorators == ["@app.route"]
    assert reader.vulture_configuration.ignore == ["src/main.py"]
    assert reader.vulture_configuration.ignore_types == ["attribute"]
    assert reader.package_configuration.setup_path.as_posix() == "src/setup.py"
    assert reader.package_configuration.check_entry_points is False


def test_read_light_ini(examples_path):
    """Tests with the mini.ini example"""
    reader = IniReader(Path(examples_path / "ini/mini.ini"))

    reader.read_ini()

    assert reader.vulture_configuration.exclude == reader.vulture_configuration.EXCLUDE_DEFAULT
    assert reader.vulture_configuration.ignore_names == []
    assert reader.vulture_configuration.ignore_decorators == []
    assert reader.vulture_configuration.ignore == []
    assert reader.vulture_configuration.ignore_types == []
    assert reader.package_configuration.setup_path.as_posix() == "setup.py"
    assert reader.package_configuration.check_entry_points is True
