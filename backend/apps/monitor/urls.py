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

from .views.monitor import MonitorManageViewSet

monitor_router = routers.SimpleRouter()
monitor_router.register(r"monitor", MonitorManageViewSet)

urlpatterns = [
    path('getsysteminfo/',MonitorManageViewSet.as_view({'get':'getsysteminfo'}), name='实时获取本机监控信息'),
]

urlpatterns += monitor_router.urls





