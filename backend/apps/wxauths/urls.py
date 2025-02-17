#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: 认证模块的 URL 配置
"""


from django.urls import path, re_path
from rest_framework import routers

from .views.applet import WxAppletLoginAPIView
# oauths_url = routers.SimpleRouter()
# user_url.register(r'auth', UserPasswordView)

urlpatterns = [
  path("applet/login", WxAppletLoginAPIView.as_view(), name="wx_applet_login")
]

# urlpatterns += oauths_url.urls