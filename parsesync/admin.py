# -*- coding=utf-8 -*-

from django.contrib import admin
from parsesync.models import ParseModel


class ParseAdmin(admin.ModelAdmin):
    list_display = ParseModel.SYSTEM_FIELDS
    readonly_fields = ParseModel.SYSTEM_FIELDS
    search_fields = ('object_id',)

    @staticmethod
    def parse_list_display(*list_display):
        return list_display + ParseModel.SYSTEM_FIELDS
