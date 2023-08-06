# -*- coding: UTF-8 -*-

import functools
import typing

import pydantic
from django.conf import settings
from django.db import models as d_models
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django_simple_api import Path, describe_response

from . import service


def result_json(func):
    def convert_model(v):
        dv = {}
        for f in v._meta.fields:
            fv = getattr(v, f.name)
            if isinstance(f, (d_models.ImageField, d_models.FileField)):
                if str(fv):
                    fv = "{}{}".format(settings.MEDIA_URL, fv)
                else:
                    fv = None
            if not isinstance(fv, d_models.Model):
                dv[f.name] = fv
        # end for

        return dv

    # end convert_model

    def serializer(d):
        iter = None
        if isinstance(d, dict):
            iter = d.items()
        elif isinstance(d, list):
            iter = enumerate(d)
        if iter:
            for k, v in iter:
                if isinstance(v, dict) or isinstance(v, list):
                    d[k] = serializer(v)
                elif isinstance(v, (str, int, float, bool, type(None))):
                    pass
                elif isinstance(v, d_models.Model):
                    d[k] = convert_model(v)
                else:
                    d[k] = [convert_model(f) for f in v]
            # end if
        # end for
        # end if

        return d

    # end serializer

    @functools.wraps(func)
    def warpper(*args, **kwargs):
        result = serializer(func(*args, **kwargs))
        if isinstance(result, dict):
            return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})
        elif isinstance(result, str):
            return HttpResponse(result)
        return result

    # end warpper

    return warpper


# end - result_json


class DictionaryConfigure(View):
    class GetResponse(pydantic.BaseModel):
        status: str
        data: typing.Any

    # end - GetResponse

    @method_decorator([cache_page(60), describe_response(200, content=GetResponse), result_json])
    def get(self, request, group: typing.Optional[str] = Path(), key: typing.Optional[str] = Path()):
        """
        获取系统配置
        """
        result = service.getConfig(group, key)
        return {
            "err": 0,
            "msg": "ok",
            "data": result,
        }
