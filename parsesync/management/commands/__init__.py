# -*- coding=utf-8 -*-

from re import split


class ParseSyncException(Exception):
    pass


def to_camel_case(var_name):
    parts = var_name.split('_')
    return parts[0] + "".join(x.title() for x in parts[1:])


def to_snake_case(var_name):
    return '_'.join([t.lower() for t in split(r'([A-Z][a-z]*)', var_name) if t])
