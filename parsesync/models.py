# -*- coding=utf-8 -*-

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from json import dumps, loads
from . import ParseSyncException, to_camel_case, to_snake_case
from .client import ParseClient


class ParseModel(models.Model):
    DJANGO_ID_PARSE_FIELD = 'djangoId'
    CREATED_AT_PARSE_FIELD = 'createdAt'
    CREATED_AT_DJANGO_FIELD = to_snake_case(CREATED_AT_PARSE_FIELD)
    OBJECT_ID_PARSE_FIELD = 'objectId'
    OBJECT_ID_DJANGO_FIELD = to_snake_case(OBJECT_ID_PARSE_FIELD)
    UPDATED_AT_PARSE_FIELD = 'updatedAt'
    UPDATED_AT_DJANGO_FIELD = to_snake_case(UPDATED_AT_PARSE_FIELD)
    SYSTEM_FIELDS = (OBJECT_ID_DJANGO_FIELD, CREATED_AT_DJANGO_FIELD, UPDATED_AT_DJANGO_FIELD)

    pc = ParseClient()

    object_id = models.CharField(max_length=10, editable=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def delete(self):
        result = self.pc.delete(self.__class__.__name__, self.object_id)
        # TODO: Exception may occur if the object we are trying to delete does
        # not exists, we must not raise exception but send this information to
        # be shown on admin

    def save(self):
        self._get_payload()

        # if the object was not synced, it doesn't have an objectId yet and
        # we must create it at Parse
        if not self.object_id:
            self._create()
        else:
            self._update()

        super(ParseModel, self).save()

    def _create(self):
        result = self.pc.create(self.__class__.__name__, dumps(self.payload))
        self._handle_exception(result)

        self.object_id = result[self.OBJECT_ID_PARSE_FIELD]
        self.created_at = self.updated_at = result[self.CREATED_AT_PARSE_FIELD]

    def _get_payload(self):
        self.payload = {}

        for field in self._meta.fields:
            field_class = field.__class__.__name__
            prepare_method = '_prepare_%s' % to_snake_case(field_class)
            parse_field_name = to_camel_case(field.column)

            # ignoring "system" fields
            if field.name not in self.SYSTEM_FIELDS:
                if field.primary_key:
                    self.payload[self.DJANGO_ID_PARSE_FIELD] = self._prepare_field(field)
                elif hasattr(self, prepare_method):
                    self.payload[parse_field_name] = getattr(self, prepare_method)(field)
                else:
                    self.payload[parse_field_name] = self._prepare_field(field)

        print dumps(self.payload)

    def _handle_exception(self, result):
        if 'error' in result:
            raise ParseSyncException('%(error)s (code %(code)s)' % result)

    def _prepare_field(self, field):
        return getattr(self, field.name)

    def _prepare_date_field(self, field):
        return self._prepare_date_time_field(field)

    def _prepare_date_time_field(self, field):
        return {
            '__type': 'Date',
            'iso': getattr(self, field.name).isoformat()
        }

    def _prepare_foreign_key(self, field):
        pointer = getattr(self, field.name)
        model = pointer.__class__.__name__

        if not hasattr(pointer, self.OBJECT_ID_DJANGO_FIELD):
            raise ParseSyncException('Related model %s does not extend ParseModel, fix it and try again' % model)

        return {
            '__type': 'Pointer',
            'className': model,
            'objectId': pointer.object_id
        }

    def _update(self):
        result = self.pc.update(self.__class__.__name__, self.object_id, dumps(self.payload))

        # If update fails with code 101, the objectId provided was not found.
        # which means we should create a new object and get a new objectId
        if result.get('code') == 101:
            self._create()

        self._handle_exception(result)
        self.updated_at = result[self.UPDATED_AT_PARSE_FIELD]

    class Meta:
        abstract = True


@receiver(post_delete)
def delete_from_parse(sender, instance, **kwargs):
    if isinstance(instance, ParseModel):
        instance.delete()
