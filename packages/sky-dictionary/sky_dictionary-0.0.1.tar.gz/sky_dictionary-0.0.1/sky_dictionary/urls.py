# encoding: utf-8
"""
@project: djangoModel->url
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/6/6 14:25
"""

from django.urls import path

from .views import DictionaryConfigure

urlpatterns = [
    path("configure/", DictionaryConfigure.as_view()),
    path("configure/<str:group>", DictionaryConfigure.as_view()),
    path("configure/<str:group>/<str:key>", DictionaryConfigure.as_view()),
]


