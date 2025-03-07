#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: 用户模块的 URL 配置
"""


from django.urls import path, re_path
from rest_framework import routers

from apps.v1.users.views.user import UserViewSet

user_url = routers.SimpleRouter()
user_url.register(r'', UserViewSet)

urlpatterns = []

urlpatterns += user_url.urls