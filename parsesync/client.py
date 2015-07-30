# -*- coding=utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from json import dumps, loads
from urllib import urlencode

from requests import delete, get, post, put


class ParseClient():
    # TODO: Exceptions should be handled and raised here
    APPLICATION_ID_SETTING = 'PARSE_APPLICATION_ID'
    MASTER_API_KEY_SETTING = 'PARSE_MASTER_API_KEY'
    REST_API_KEY_SETTING = 'PARSE_REST_API_KEY'
    SETTING_NOT_FOUND_MSG = 'Setting %s was not found on your project'

    BASE_URL = 'https://api.parse.com/1/'
    QUERY_URL = CREATE_URL = BASE_URL + 'classes/%s'
    GET_URL = UPDATE_URL = DELETE_URL = QUERY_URL + '/%s'
    SCHEMAS_URL = '%sschemas' % BASE_URL

    def create(self, cls, payload):
        r = post(self.CREATE_URL % cls, **self._request_kwargs(payload))
        return loads(r.text)

    def delete(self, cls, objectId):
        r = delete(self.DELETE_URL % (cls, objectId), **self._request_kwargs())
        return loads(r.text)

    def get(self, cls, objectId):
        r = get(self.GET_URL % (cls, objectId), **self._request_kwargs())
        return loads(r.text)

    def query(self, cls, where={}, order='createdAt', limit=100, skip=0):
        payload = {
            'where': dumps(where),
            'order': order,
            'limit': limit,
            'skip': skip,
        }
        r = get('%s?%s' % (self.QUERY_URL % cls, urlencode(payload)), **self._request_kwargs())
        return loads(r.text)

    def schemas(self):
        r = get(self.SCHEMAS_URL, **self._request_kwargs(master_key_required=True))
        return loads(r.text)

    def update(self, cls, object_id, payload):
        r = put(self.UPDATE_URL % (cls, object_id), **self._request_kwargs(payload))
        return loads(r.text)

    def _request_kwargs(self, payload=None, master_key_required=False):
        if not hasattr(settings, self.APPLICATION_ID_SETTING):
            raise ImproperlyConfigured(self.SETTING_NOT_FOUND_MSG % self.APPLICATION_ID_SETTING)
        elif not hasattr(settings, self.REST_API_KEY_SETTING):
            raise ImproperlyConfigured(self.SETTING_NOT_FOUND_MSG % self.REST_API_KEY_SETTING)
        elif not hasattr(settings, self.MASTER_API_KEY_SETTING) and master_key_required:
            raise ImproperlyConfigured(self.SETTING_NOT_FOUND_MSG % self.MASTER_API_KEY_SETTING)

        headers = {
            'X-Parse-Application-Id': getattr(settings, self.APPLICATION_ID_SETTING),
            'X-Parse-REST-API-Key': getattr(settings, self.REST_API_KEY_SETTING),
            'Content-Type': 'application/json'
        }

        return {
            'headers': headers,
            'data': payload
        }
