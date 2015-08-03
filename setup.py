#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join
from setuptools import find_packages, setup

URL = 'https://github.com/cereigido/django-parsesync/'
VERSION = __import__('parsesync').__version__

with open(abspath(join(dirname(__file__), 'README.md'))) as fileobj:
    README = fileobj.read().strip()

setup(
    name='django-parsesync',
    packages=find_packages(),
    version=VERSION,
    author='Paulo Cereigido',
    author_email='paulocereigido@gmail.com',
    description=('A wrapper that persists your data into your Parse.com app'),
    long_description=README,
    url=URL,
    download_url='%s/tarball/%s' % (URL, VERSION),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.4',
        'requests>=2.7.0',
    ],
)
