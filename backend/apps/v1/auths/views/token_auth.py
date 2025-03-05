#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework.request import Request

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from ..serializers import TokenObtainWithUserSerializer, UnifiedTokenRefreshSerializer
from comutils.response.json_response import DataResponse, ValidationErrorResponse

# 这一版是直接重写 TokenViewBase 的 post 方法
# TODO
# 下一版可以尝，直接重写 TokenObtainPairSerializer 等系列器，加入用户信息
class TokenBasePostMixin():
  def post(self, request: Request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    try:
      serializer.is_valid(raise_exception=True)
    except TokenError as e:
      print("Token Error", e)
      errors = {
        self.error_key: e.args[0],
      }
      return ValidationErrorResponse(errors=errors)
    
    data = serializer.validated_data
    return DataResponse(data)
  
class MyTokenViewBase(TokenBasePostMixin, TokenViewBase):
  error_key = "token"

class TokenRefreshView(MyTokenViewBase):
  # serializer_class = TokenRefreshSerializer 
  serializer_class = UnifiedTokenRefreshSerializer 
  error_key = "refresh"

class TokenVerifyView(MyTokenViewBase):
  serializer_class = TokenVerifySerializer 
  error_key = "token"


class TokenObtainPairView(MyTokenViewBase):
  # serializer_class = TokenObtainPairSerializer 
  serializer_class = TokenObtainWithUserSerializer 
  error_key = "refresh"

# 以下是方案一 直接继续Mixin
# class TokenRefreshView(GenericAPIView, TokenBasePostMixin):
#   serializer_class = TokenRefreshSerializer 
#   authentication_classes = []
#   permission_classes = []
#   error_key = "refresh"

# class TokenVerifyView(GenericAPIView, TokenBasePostMixin):
#   serializer_class = TokenVerifySerializer 
#   authentication_classes = []
#   permission_classes = []
#   error_key = "token"


# class TokenObtainPairView(GenericAPIView, TokenBasePostMixin):
#   serializer_class = TokenObtainPairSerializer 
#   authentication_classes = []
#   permission_classes = []
#   error_key = "refresh"



  