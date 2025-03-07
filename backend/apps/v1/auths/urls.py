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

from apps.v1.auths.views import user_auth
from apps.v1.auths.views.token_auth import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# auths_url = routers.SimpleRouter()
# user_url.register(r'auth', UserPasswordView)

urlpatterns = [
  # 改写原有的TokenView
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

  path('general/password/login/', user_auth.UserPasswordLoginAPIView.as_view({"post": "login"}), name="general_password_login"),
  path('phone/password/login/', user_auth.PhonePasswordLoginAPIView.as_view({"post": "login"}), name="phone_password_login"),
  path('phone/code/login/', user_auth.PhoneSMSCodeLoginAPIView.as_view({"post": "login"}), name="phone_code_login"),

  path('general/password/reset/', user_auth.ResetPasswordAPIView.as_view({"post": "login"}), name="general_password_reset"),
  path('phone/code/password/reset/', user_auth.ResetPasswordByPhoneAPIView.as_view({"post": "login"}), name="phone_code_password_reset"),

]

# urlpatterns += auths_url.urls