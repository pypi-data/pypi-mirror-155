# encoding: utf-8
"""
@project: djangoModel->service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/6/6 14:23
"""
# -*- coding: UTF-8 -*-

from django.core.cache import cache

from . import models


# cache 不支持异步
def getConfig(group=None, key=None):
    ch = cache.get('dictionary_configure')
    if not ch:
        ch = updateConfig()
    if not group:
        return ch
    if group in ch:
        if not key:
            return ch[group]
        if key in ch[group]:
            return ch[group][key]
    return None


def updateConfig(group=None, key=None, value=None):
    ch = (cache.get('dictionary_configure') or {}) if group else {}
    if not ch or not group:
        for kv in models.Configure.objects.all():
            if str(kv.group) not in ch:
                ch[str(kv.group)] = {}
            ch[str(kv.group)][str(kv.key)] = str(kv.value)
    # end for
    elif group and key and value:
        if str(group) not in ch:
            ch[str(group)] = {}

        ch[str(group)][str(key)] = str(value)
    elif group and key:
        if str(group) not in ch:
            ch[str(group)] = {}

        try:
            ch[str(group)][str(key)] = str(models.Configure.objects.get(group=group, key=key).value)
        except:
            pass
    # end try
    elif group:
        if str(group) not in ch:
            ch[str(group)] = {}

        for kv in models.Configure.objects.filter(group=group):
            ch[str(group)][str(kv.key)] = str(kv.value)
    return ch


def getPricing(province, hurry, key="邮费"):
    priceBase = None
    if province:
        priceBase = getConfig(key, province)
    if not priceBase and province:
        priceBase = getConfig(key, "其他省份")
    if not priceBase:
        priceBase = "0.0"

    price = float(priceBase)

    if hurry:
        priceHurry = getConfig(key, "当日加急")
        if priceHurry:
            price += float(priceHurry)
    return price


def setConfig(group, key, value):
    models.Configure.objects.update_or_create(
        group=group, key=key,
        defaults={"value": value}
    )

    updateConfig()
