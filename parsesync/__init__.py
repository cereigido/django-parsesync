# -*- coding=utf-8 -*-

from re import split
from threading import Thread

__version__ = '1.1.3'


class FunctionThread(Thread):
    def __init__(self, fn, *args, **kwargs):
        Thread.__init__(self)
        self.fn = fn
        self.kwargs = kwargs

    def run(self):
        self.fn(**self.kwargs)


class ParseSyncException(Exception):
    pass


def exception_handler(result):
    if 'error' in result:
        raise ParseSyncException('%(error)s (code %(code)s)' % result)


def to_camel_case(var_name):
    parts = var_name.split('_')
    return parts[0] + "".join(x.title() for x in parts[1:])


def to_snake_case(var_name):
    return '_'.join([t.lower() for t in split(r'([A-Z][a-z]*)', var_name) if t])
