#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open
from os import path
from setuptools import setup, find_packages


def read_readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name="pytest-check",
    version="0.3.5",
    author="Brian Okken",
    license="MIT",
    url="https://github.com/okken/pytest-check",
    description="A pytest plugin that allows multiple failures per test.",
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pytest>=3.1.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["check = pytest_check.plugin"]},
)
