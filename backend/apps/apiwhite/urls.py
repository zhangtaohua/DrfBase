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

from .views.whitelist import ApiWhiteListViewSet

api_whitelist_url = routers.SimpleRouter()
api_whitelist_url.register(r"whitelist", ApiWhiteListViewSet)

urlpatterns = [
]

urlpatterns += api_whitelist_url.urls

