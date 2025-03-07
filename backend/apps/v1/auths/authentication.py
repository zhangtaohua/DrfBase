#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ApiException
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.v1.users.models import Users
from comutils.response.json_response import BadRequestResponse, UnauthorizedResponse

class UsernamePswAuthentication(BaseAuthentication):
  def authenticate(self, request):
    token = request.META.get("HTTP_AUTHORIZATION", "")
    if not token:
      raise ApiException("token 不能为空")
    
    try:
      validated_token = AccessToken(token)
    except Exception as e:
      raise ApiException("token 格式错误")
    
    # id = validated_token["id"]
    user = Users.objects.filter(pk=validated_token["id"]).first()

    return user, token