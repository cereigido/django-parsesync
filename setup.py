#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join
from setuptools import setup

URL = 'https://github.com/cereigido/parsesync/'
VERSION = '1.0.0'

with open(abspath(join(dirname(__file__), 'README.md'))) as fileobj:
    README = fileobj.read().strip()

setup(
    name='parsesync',
    packages=['parsesync'],
    version=VERSION,
    author='Paulo Cereigido',
    author_email='paulocereigido@gmail.com',
    description='A wrapper that persists your data into your Parse.com app',
    long_description=README,
    url=URL,
    download_url='%s/tarball/%s' % (URL, VERSION),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'Django>=1.4',
        'requests>=2.7.0',
    ],
)
