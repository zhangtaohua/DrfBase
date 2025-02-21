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

from .views.login import LoginLogViewSet
from .views.operation import OperationLogViewSet

log_router = routers.SimpleRouter()
log_router.register(r"login", LoginLogViewSet, basename="login_log")
log_router.register(r"operation", OperationLogViewSet, basename="operation_log")

urlpatterns = [
]

urlpatterns += log_router.urls

