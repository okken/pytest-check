#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-check',
    version='0.2.0',
    author='Brian Okken',
    author_email='brian@pythontesting.net',
    maintainer='Brian Okken',
    maintainer_email='brian@pythontesting.net',
    license='MIT',
    url='https://github.com/okken/pytest-check',
    description='A pytest plugin that allows multiple failures per test.',
    long_description=read('README.rst'),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['pytest>=3.1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'check = pytest_check.plugin',
        ],
    },
)
