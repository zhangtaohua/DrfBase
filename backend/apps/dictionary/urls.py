#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


"""
@Remark: 字典模块的 URL 配置
"""


from django.urls import path, re_path

from rest_framework import routers

from .views.dictionary import DictionaryViewSet, InitDictionaryViewSet

dict_router = routers.SimpleRouter()
dict_router.register(r"", DictionaryViewSet)

urlpatterns = [
  path("trees/<int:pk>/", DictionaryViewSet.as_view({
    "get": "retrive_children",
  }), name="dict_pk_trees"),
  path("trees/", DictionaryViewSet.as_view({
    "get": "trees",
  }), name="dict_all_trees"),
  path("init/", InitDictionaryViewSet.as_view(), name="dict_init_data")
]

urlpatterns += dict_router.urls





