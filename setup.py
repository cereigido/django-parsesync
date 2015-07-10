#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join
from setuptools import setup

with open(abspath(join(dirname(__file__), 'README.md'))) as fileobj:
    README = fileobj.read().strip()

setup(
    name='parsesync',
    description='',
    long_description=README,
    author='Paulo Cereigido',
    url='https://github.com/cereigido/parsesync',
    version='1.0.0',
    zip_safe=False,
    include_package_data=True,
    packages=[
        'parsesync',
    ],
    install_requires=[
        'Django',
        'requests',
    ],
)
