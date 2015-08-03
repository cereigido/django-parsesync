# -*- coding: utf-8 -*-

from datetime import datetime
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from json import loads
from optparse import make_option
from parsesync import to_snake_case
from parsesync.client import ParseClient
from parsesync.config import ParseSyncConfig
from parsesync.models import ParseModel
from urllib import urlretrieve


class Command(BaseCommand):
    help = 'Sync data from parse to Django'

    # Django < 1.7- support
    option_list = BaseCommand.option_list + (
        make_option('--model', help='Sync only provided model name'),
        make_option('--all', action='store_true', default=False, help='Query content from the beggining of time'),
    )

    # Django 1.8+ support
    def add_arguments(self, parser):
        parser.add_argument('--model', help='Sync only provided model name')
        parser.add_argument('--all', action='store_true', default=False, help='Query content from the beggining of time')

    def handle(self, *args, **options):
        self.pc = ParseClient()
        self.psc = ParseSyncConfig()

        # dependencies must be identified and synced first
        model_filter = options.get('model')
        if model_filter:
            model_filter = ''.join(model_filter.lower().split(' '))
            content_types = ContentType.objects.filter(model=model_filter)
        else:
            content_types = ContentType.objects.all().order_by('model')

        for content_type in content_types:
            model = content_type.model_class()
            if issubclass(model, ParseModel):
                self.query(model, options.get('all'))

    def query(self, model, all):
        limit = 500
        page = 1
        model_name = model.__name__
        where = {}

        print 'Querying %s on Parse...' % (model_name)
        while True:
            if not all:
                last_synced = self.psc.get_last_updated_item_from_parse(model)
                if (last_synced):
                    where['updatedAt'] = {'$gt': {'__type': 'Date', 'iso': last_synced}}

            query = self.pc.query(model_name, where=where, order='updatedAt', limit=limit)
            results = query['results']

            self.save(model, model_name, results)
            if len(results) < limit:
                break
            else:
                page += 1

    def save(self, model, model_name, results):
        for item in results:
            object_id = item.get('objectId')
            updated_at = item.get('updatedAt')
            files = []

            try:
                instance = model.objects.get(object_id=object_id)
                print '\tUpdating Django %s.%s, last updated at %s...' % (model_name, object_id, updated_at)
            except model.DoesNotExist:
                print '\tCreating Django %s.%s, last updated at %s...' % (model_name, object_id, updated_at)
                instance = model()

            for key, value in item.items():
                snake_key = to_snake_case(key)

                if type(value) != dict:
                    setattr(instance, snake_key, value)
                elif value['__type'] == 'Date':
                    conv_value = datetime.strptime(value['iso'], "%Y-%m-%dT%H:%M:%S.000Z")
                    setattr(instance, snake_key, conv_value)
                elif value['__type'] == 'File':
                    if 'url' in value:
                        dl_file = urlretrieve(value['url'])
                        files.append([getattr(instance, snake_key), value['name'], File(open(dl_file[0]))])
                elif value['__type'] == 'Pointer':
                    setattr(instance, '%s_id' % value['className'].lower(), value['objectId'])
                else:
                    print 'Unhandled: %s' % value

            # avoiding Parse update, saving only locally
            instance.save_to_parse = False
            try:
                instance.save()
            except Exception, e:
                print 'Error [%s] ocurred while saving your content' % e

            # saving and associating files
            for f in files:
                f[0].save(f[1], f[2])

            self.psc.set_last_updated_item_from_parse(model, updated_at)
            self.psc.save()
