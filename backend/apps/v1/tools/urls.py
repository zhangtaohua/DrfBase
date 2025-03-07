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

from apps.v1.tools.views.health import HealthView, PingView
from apps.v1.tools.views.captcha import CaptchaView

# tools_url = routers.SimpleRouter()
# tools_url.register(r'', )

urlpatterns = [
  # for docker check
  path("health/", HealthView.as_view(), name="health_check"),
  path("ping/", PingView.as_view(), name="ping_check"),

  # 验证码相关
  path("captcha/chars/", CaptchaView.as_view(), name="captcha_chars")

  # SMS 相关

  # email 相关

]

# urlpatterns += tools_url.urls