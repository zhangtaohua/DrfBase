#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, APIException

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import WXUsers

class WxAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WXUsers
        fields = "__all__"
        extra_kwargs = {
          "applet_openid": {"write_only": True}, 
          "session_key": {"write_only": True}, 
          "unionid": {"write_only": True}
        }

class WxAppleLoginSerializer(TokenObtainPairSerializer):

  @classmethod
  def get_token(cls, user):
    token = super(WxAppleLoginSerializer, cls).get_token(user)
    data = {}
    data["openid"] = user.wxusers.applet_openid
    data["userid"] = user.id
    data["refresh"] = str(token)
    data["access"] = str(token.access_token)

    return data