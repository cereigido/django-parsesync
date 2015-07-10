# -*- coding=utf-8 -*-

from django.contrib import admin
from parsesync.models import ParseModel


class ParseAdmin(admin.ModelAdmin):
    readonly_fields = ParseModel.SYSTEM_FIELDS
