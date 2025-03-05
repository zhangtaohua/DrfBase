#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


"""
@Remark: API接口白名单模块的 URL 配置
"""


from django.urls import path, re_path

from rest_framework import routers

from .views.whitelist import ApiWhiteListViewSet

api_whitelist_router = routers.SimpleRouter()
api_whitelist_router.register(r"", ApiWhiteListViewSet, basename="api_white_list")

urlpatterns = [
]

urlpatterns += api_whitelist_router.urls

