# -*- coding: utf-8 -*-
"""pytest-vulture
=============
Plugin for py.test for doing vulture tests
"""
import os

from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)


IS_TEST = bool(os.environ.get("IS_UNIT_TEST", 0))

install_requires = [
    'vulture <3.0, >2.0 ',
]
if not IS_TEST:
    install_requires.append("pytest >= 7.0.0")

test_requires = [
    'pylint==2.14.5',
    'pytest==7.1.2',
    'pytest-runner==5.2',
    'pytest-cov==2.10.1',
    'pytest-pycodestyle==2.3.0',
    'pytest-pylint==0.18.0',
    'pytest-isort==3.0.0',
    'pytest-mccabe==2.0',
    'pytest-mypy==0.9.1',
]

dev_requires = [
]

# to prevent coverage bugs
ENTRY_POINTS = {
    "pytest11": [
        "vulture = pytest_vulture.plugin",
    ]
} if not IS_TEST else {}

setup(
    name='pytest-vulture',
    version='2.1.0',
    include_package_data=True,
    author='Abadie Moran',
    author_email='moran.abadie@gatewatcher.com',
    maintainer='Abadie Moran',
    maintainer_email='moran.abadie@gatewatcher.com',
    license='MIT',
    url='https://github.com/Gatewatcher/pytest-vulture',
    description='A pytest plugin to checks dead code with vulture',
    long_description=(Path(__file__).parent / "README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/x-rst",
    package_dir={
        '': 'src',
    },
    packages=find_packages(
        'src'
    ),
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require={
        'test': test_requires,
        'dev': test_requires + dev_requires,
    },
    entry_points=ENTRY_POINTS,
    classifiers=["Framework :: Pytest"],
)
