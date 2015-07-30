# -*- coding=utf-8 -*-

from tempfile import gettempdir, mkstemp
from json import dump, load


class ParseSyncConfig():
    CONFIG_PATH = '%s/parsesync.config' % gettempdir()

    def __init__(self):
        try:
            with open(self.CONFIG_PATH, 'r') as f:
                self.config = load(f)
        except Exception, e:
            self.config = {'from_parse': {}}

    def get_last_updated_item_from_parse(self, model):
        key = self._get_key_from_model(model)
        return self.config['from_parse'].get(key)

    def set_last_updated_item_from_parse(self, model, date):
        key = self._get_key_from_model(model)
        self.config['from_parse'][key] = date

    def _get_key_from_model(self, model):
        return '%s.%s' % (model.__module__, model.__name__)

    def save(self):
        with open(self.CONFIG_PATH, 'w') as f:
            dump(self.config, f)
