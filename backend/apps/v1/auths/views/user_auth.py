#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework.viewsets import GenericViewSet

from ..serializers import *

from apps.v1.users.serializers import UserSerializer
from apps.v1.users.models import Users

from comutils.response.json_response import DataResponse, BadRequestResponse

class LoginMixin:

  def login(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # serializer.is_valid(raise_exception=False)
    # if serializer.errors:
    #   return BadRequestResponse(serializer.errors)
    
    # 返回 attrs 时的初版写法
    # user = serializer.context.get("user")
    # user = serializer.context["user"]
    # access_token = serializer.context["access_token"]
    # refresh_token = serializer.context["refresh_token"]
    # print("user", user.id, type(user), access_token, refresh_token)
    # user_serializer = self.get_serializer(instance=user)

    return DataResponse(serializer.validated_data)


class UserPasswordLoginAPIView(LoginMixin, GenericViewSet):
  serializer_class = UserPasswordLoginSerializer

class PhonePasswordLoginAPIView(LoginMixin, GenericViewSet):
  serializer_class = PhonePasswordSerializer

class PhoneSMSCodeLoginAPIView(LoginMixin, GenericViewSet):
  serializer_class = PhoneSMSCodeLoginSerializer

class ResetPasswordAPIView(LoginMixin, GenericViewSet):
  serializer_class = ResetPasswordSerializer

class ResetPasswordByPhoneAPIView(LoginMixin, GenericViewSet):
  serializer_class = ResetPasswordByPhoneCodeSerializer