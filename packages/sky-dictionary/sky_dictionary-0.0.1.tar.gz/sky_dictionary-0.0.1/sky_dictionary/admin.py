# -*- coding: UTF-8 -*-

from django.contrib import admin

from . import models


@admin.register(models.Configure)
class ConfigureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["group", "description", "key", "value", ],
        }),
    ]

    list_display = ["description", "group", "key", "value_short"]
    list_filter = ["group"]

    def get_form(self, request, obj=None, **kwargs):
        # if not router.isMobile(request):
        # 	kwargs["form"] = forms.py.ConfigAdminForm

        return super().get_form(obj, **kwargs)
