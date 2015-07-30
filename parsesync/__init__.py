# -*- coding=utf-8 -*-

from re import split

__version__ = '1.0.0'


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
