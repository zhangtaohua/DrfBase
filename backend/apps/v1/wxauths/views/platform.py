#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import datetime
import random
import string

from django.db import transaction
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from ..utils import WxOfficialPlatform
from ..models import WXUsers
from ..serializers import *

from conf import configs
from comutils.common.regex import MOBILE_PHONE_REGEX

from comutils.response.json_response import DataResponse, ErrorsResponse, ValidationErrorResponse
from apps.v1.users.models import Users
# Create your views here.

WXOP = WxOfficialPlatform()

"""
  post:
  微信公众平台登录接口
  微信公众平台 通过 code 获取 openid 和 access_token
"""
class WxOfficialPlatformLoginAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  @transaction.atomic
  def post(self, request):
    data = request.data
    code = data.get("code", None)

    if not code:
      errors= {
                "code": "This field is required"
              }
      return ErrorsResponse(errors)
      
    openid_tokens = WXOP.get_openid_tokens(code)
    openid = openid_tokens["openid"]

    #判断用户是否存在(根据openID判断用户是否是第一次登陆)
    user = Users.objects.filter(
      is_active=True, 
      wxusers__official_account_openid=openid
      ).first()
    
    if not user:#如果不存在则提示绑定用户关系
      data={
        "openid": openid,
        "is_bind": False,
        "user": None,
        }
      return ErrorsResponse(data)

    resdata = WxAppleLoginSerializer.get_token(user)
    return DataResponse(resdata)
  
"""
  绑定微信用户
  post:
  绑定微信用户
  微信公众号openid、mobile（绑定手机号）、code（验证码）
"""
class WxOfficialPlatformBindAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  def post(self, request):
    data = request.data
    openid = data.get("openid", None)
    mobile = data.get("mobile", None) #邀请码#为推广者的userid
    code = data.get("code", None)
   
    hasErrors = False
    errors= {}
    if openid is None:
      hasErrors = True
      errors["openid"] =  "This field is required"
    
    if mobile is None:
      hasErrors = True
      errors["mobile"] =  "This field is required"

    # 验证手机号是否合法
    if not re.match(MOBILE_PHONE_REGEX, mobile):
        hasErrors = True
        errors["mobile"] =  "The mobile is wrong format"
    
    if code is None:
      hasErrors = True
      errors["code"] =  "This field is required"

    verify_code = cache.get()
    if not verify_code:
      hasErrors = True
      errors["code"] =  "This field has expired"
    else: 
      if str(verify_code) != str(code):
        hasErrors = True
        errors["code"] =  "This field is wrong"
    
    if hasErrors:
      return ErrorsResponse(errors)

    user = Users.objects.filter(
      is_active=True, 
      username=mobile+"app",
      identity__contains="1",
      oauthwxuser__isnull=True).first()
    
    if not user:#如果不存在
      data={
        "openid": openid,
        "is_bind": False,
        "user": None,
        "error": "cannot bind, has no user",
        }
      return ErrorsResponse(data)
    
    WXUsers.objects.create(user=user, official_account_openid=openid)

    resdata = WxAppleLoginSerializer.get_token(user)
    return DataResponse(resdata)

    