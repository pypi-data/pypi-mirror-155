# -*- coding: UTF-8 -*-

# from ako import router
from django.db import models

from . import service


class Configure(models.Model):
    group = models.CharField(verbose_name="分组", max_length=128, db_index=True)
    key = models.CharField(verbose_name="参数名", max_length=128, db_index=True)
    value = models.TextField(verbose_name="参数值", blank=True, default="")
    description = models.CharField(verbose_name="说明", max_length=255)

    SEO_FIELDS = ["group", "key", "value", "description"]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        result = super().save(force_insert, force_update, using, update_fields)
        service.updateConfig(self.group, self.key, self.value)
        return result

    # end save

    def delete(self, using=None, keep_parents=False):
        result = super().delete(using, keep_parents)
        # utility.updateConfig()    # 完全更新缓存
        return result

    # end delete

    def value_short(self):
        if len(self.value) > 10:
            return self.value[:10] + "..."
        return self.value

    value_short.short_description = "参数值"
    value_short.admin_order_field = "value"

    class Meta:
        db_table = 'dictionary_configure'
        verbose_name_plural = "1. 字典 - 系统配置"
        verbose_name = "配置"
        unique_together = [("group", "key")]

    def __str__(self):
        return "[{}/{}] {}".format(self.group, self.key, self.description)
