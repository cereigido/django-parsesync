# -*- coding=utf-8 -*-

from django.contrib import admin


class ParseAdmin(admin.ModelAdmin):
    readonly_fields = ('object_id', 'created_at', 'updated_at', )
