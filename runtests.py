#!/usr/bin/env python

from django import setup
from django.conf import settings
from nose import run_exit
from sys import argv
from parsesync import client

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'parsesync',
        ]

    )

try:
    setup()
except AttributeError:
    pass

if __name__ == "__main__":
    run_exit(argv=argv)
