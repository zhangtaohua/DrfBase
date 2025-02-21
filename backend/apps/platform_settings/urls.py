#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


"""
@Remark: 文件模块的 URL 配置
"""


from django.urls import path, re_path

from rest_framework import routers

from .views.download import FilesDownloadViewSet

file_url = routers.SimpleRouter()
file_url.register(r"files/download", FilesDownloadViewSet)

urlpatterns = [
]

urlpatterns += file_url.urls





