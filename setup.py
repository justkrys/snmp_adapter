#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.1",
    "pysnmp>=4.4",
    "psycopg2>=2.8",
    "sqlalchemy>=1.3",
    "yattag>=1.14",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author="Krys Lawrence",
    author_email="krys.lawrence@cbsa-asfc.gc.ca",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    description="Test code for an SNMP adapter for LabView.",
    entry_points={
        "console_scripts": [
            "snmp_adapter=snmp_adapter.__main__:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="snmp_adapter",
    name="snmp_adapter",
    packages=find_packages(include=["snmp_adapter"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/justkrys/snmp_adapter",
    version="0.1.0",
    zip_safe=False,
)
