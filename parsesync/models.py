# -*- coding=utf-8 -*-

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from json import dumps, loads
from parsesync import ParseSyncException, exception_handler, to_camel_case, to_snake_case
from parsesync.client import ParseClient


class ParseModel(models.Model):
    CREATED_AT_PARSE_FIELD = 'createdAt'
    CREATED_AT_DJANGO_FIELD = to_snake_case(CREATED_AT_PARSE_FIELD)
    OBJECT_ID_PARSE_FIELD = 'objectId'
    OBJECT_ID_DJANGO_FIELD = to_snake_case(OBJECT_ID_PARSE_FIELD)
    UPDATED_AT_PARSE_FIELD = 'updatedAt'
    UPDATED_AT_DJANGO_FIELD = to_snake_case(UPDATED_AT_PARSE_FIELD)
    SYSTEM_FIELDS = (OBJECT_ID_DJANGO_FIELD, CREATED_AT_DJANGO_FIELD, UPDATED_AT_DJANGO_FIELD)

    pc = ParseClient()

    object_id = models.CharField(primary_key=True, max_length=10, editable=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    save_to_parse = True

    def parse_create(self):
        result = self.pc.create(self.__class__.__name__, dumps(self.payload))
        exception_handler(result)

        self.object_id = result[self.OBJECT_ID_PARSE_FIELD]
        self.created_at = self.updated_at = result[self.CREATED_AT_PARSE_FIELD]

    def parse_delete(self):
        result = self.pc.delete(self.__class__.__name__, self.object_id)
        # TODO: Exception may occur if the object we are trying to delete does
        # not exists, we must not raise an exception but send this information to
        # be shown on admin

    def parse_update(self):
        result = self.pc.update(self.__class__.__name__, self.object_id, dumps(self.payload))

        # If update fails with code 101, the objectId provided was not found.
        # which means we should create a new object and get a new objectId
        if result.get('code') == 101:
            self.delete()
            self.parse_create()
        else:
            exception_handler(result)
            self.updated_at = result[self.UPDATED_AT_PARSE_FIELD]

    def save(self):
        if self.save_to_parse:
            self._get_payload()

            if not self.object_id:
                self.parse_create()
            else:
                self.parse_update()

        super(ParseModel, self).save()

    def _get_payload(self):
        self.payload = {}

        for field in self._meta.fields:
            field_class = field.__class__.__name__
            prepare_method = '_prepare_%s' % to_snake_case(field_class)
            parse_field_name = to_camel_case(field.column)

            # TODO: when a field is null, it should be removed from parse
            # ignoring "system" fields
            if field.name not in self.SYSTEM_FIELDS and getattr(self, field.name) is not None:
                if hasattr(self, prepare_method):
                    self.payload[parse_field_name] = getattr(self, prepare_method)(field)
                else:
                    self.payload[parse_field_name] = self._prepare_field(field)

    def _prepare_date_field(self, field):
        return {
            '__type': 'Date',
            'iso': '%sT00:00:00.000' % getattr(self, field.name).isoformat()
        }

    def _prepare_date_time_field(self, field):
        return {
            '__type': 'Date',
            'iso': getattr(self, field.name).isoformat()
        }

    def _prepare_field(self, field):
        return getattr(self, field.name)

    def _prepare_file_field(self, field):
        # Not supported yet
        return None

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

    def _prepare_image_field(self, field):
        # Not supported yet
        return None

    class Meta:
        abstract = True


@receiver(post_delete)
def delete_from_parse(sender, instance, **kwargs):
    if isinstance(instance, ParseModel):
        instance.parse_delete()
