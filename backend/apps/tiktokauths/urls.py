#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: 抖音认证模块的 URL 配置
"""


from django.urls import path, re_path
from rest_framework import routers

from .views.applet import TiktokAppletAPIView

# oauths_url = routers.SimpleRouter()
# oauths_url.register(r'auth', UserPasswordView)

urlpatterns = [
  path("applet/login", TiktokAppletAPIView.as_view(), name="tiktok_applet_login")
]

# urlpatterns += oauths_url.urls