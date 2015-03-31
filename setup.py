#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup

setup(
  name = 'pytest-expect',
  packages = ['pytest_expect'], 
  version=__import__('pytest_expect').__version__,
  description = 'A pytest plugin that allows multiple failures per test',
  author = 'Brian Okken',
  author_email = 'brian@pythontesting.net',
  maintainer = 'Brian Okken',
  maintainer_email = 'brian@pythontesting.net',
  url = 'http://pythontesting.net/pytest-expect', 
  license='MIT',
  keywords = ['testing', 'pytest', 'assert'], 
  install_requires=['pytest>=2.7'],
  classifiers = [
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Testing',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 ],
   # the following makes a plugin available to py.test
   entry_points={'pytest11': ['expect = pytest_expect.plugin']}
)


