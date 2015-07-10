# from nose import with_setup

from parsesync import ParseSyncException, to_camel_case, to_snake_case
from parsesync.admin import ParseAdmin
from parsesync.models import ParseModel
from unittest import main, TestCase


class ParseSyncTest(TestCase):
    def test_string_is_converted_to_camel_case(self):
        ''' parsesync :: Strings are properly converted to camelCase '''
        self.assertEqual(to_camel_case('foo_bar'), 'fooBar')

    def test_string_is_converted_to_snake_case(self):
        ''' parsesync :: Strings are properly converted to snake_case '''
        self.assertEqual(to_snake_case('fooBar'), 'foo_bar')

    def test_parse_exception_subclasses_exception(self):
        ''' parsesync :: ParseException subclasses Exception '''
        self.assertIsInstance(ParseSyncException(), Exception)


class ParseSyncAdminTest(TestCase):
    def test_system_fields_are_mapped(self):
        ''' parsesync.admin :: object_id, created_at and updated_at are defined as system fields '''
        system_fields = (
            ParseModel.OBJECT_ID_DJANGO_FIELD,
            ParseModel.CREATED_AT_DJANGO_FIELD,
            ParseModel.UPDATED_AT_DJANGO_FIELD
        )
        self.assertTupleEqual(system_fields, ParseModel.SYSTEM_FIELDS)

    def test_system_fields_are_set_as_readonly_in_django_admin(self):
        ''' parsesync.admin :: System fields are defined as readonly in Dango admin '''
        self.assertTupleEqual(ParseModel.SYSTEM_FIELDS, ParseAdmin.readonly_fields)


class ParseSyncClientTest(TestCase):
    pass


class ParseSyncModelTest(TestCase):
    def test_parse_system_fields_are_in_camel_case(self):
        ''' parsesync.models :: Parse system fields are in camelCase '''
        self.assertEquals(ParseModel.DJANGO_ID_PARSE_FIELD, to_camel_case(ParseModel.DJANGO_ID_PARSE_FIELD))
        self.assertEquals(ParseModel.CREATED_AT_PARSE_FIELD, to_camel_case(ParseModel.CREATED_AT_PARSE_FIELD))
        self.assertEquals(ParseModel.OBJECT_ID_PARSE_FIELD, to_camel_case(ParseModel.OBJECT_ID_PARSE_FIELD))
        self.assertEquals(ParseModel.UPDATED_AT_PARSE_FIELD, to_camel_case(ParseModel.UPDATED_AT_PARSE_FIELD))

    def test_django_system_fields_are_snake_case(self):
        ''' parsesync.models :: Django system fields are in snake_case '''
        self.assertEquals(ParseModel.CREATED_AT_DJANGO_FIELD, to_snake_case(ParseModel.CREATED_AT_DJANGO_FIELD))
        self.assertEquals(ParseModel.UPDATED_AT_DJANGO_FIELD, to_snake_case(ParseModel.UPDATED_AT_DJANGO_FIELD))
        self.assertEquals(ParseModel.OBJECT_ID_DJANGO_FIELD, to_snake_case(ParseModel.OBJECT_ID_DJANGO_FIELD))

    def test_parse_system_fields_convert_to_django_system_fields(self):
        ''' parsesync.models :: Parse system fields convert to Django system fields '''
        self.assertEquals(ParseModel.CREATED_AT_PARSE_FIELD, to_camel_case(ParseModel.CREATED_AT_DJANGO_FIELD))
        self.assertEquals(ParseModel.UPDATED_AT_PARSE_FIELD, to_camel_case(ParseModel.UPDATED_AT_DJANGO_FIELD))


if __name__ == '__main__':
    main()
