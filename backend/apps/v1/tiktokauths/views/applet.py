#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import datetime
import random
import string

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from ..utils import *
from ..models import TiktokUsers
from ..serializers import *

from conf import configs
from comutils.response.json_response import DataResponse, ErrorsResponse, ValidationErrorResponse
from apps.users.models import Users

# Create your views here.

# ================================================= #
# ***************** 字节跳动小程序登录 *************** #
# ================================================= #

"""
  post:
  字节跳动小程序登录接口
  字节跳动小程序code获取openid
"""
class TiktokAppletAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  @transaction.atomic 
  def post(self, request):
    data = request.data
    
    code= data.get("code", None)
    nickname = data.get("nickname", None)
    avatar_url = data.get("avatar_url", None)
    gender = data.get("gender", None)

    hasErrors = False
    errors= {}

    if not code:
      hasErrors = True
      errors["code"] =  "This field is required"
    
    if hasErrors:
      return ErrorsResponse(errors)
    
    tiktok_ins = TictokAppletOpenId()

    openid, session_key, unionid, anonymous_openid = tiktok_ins.get_session_key(code=code)
     
    # 判断用户是否存在
    try:
      tiktok_user = Users.objects.get(username=openid)
      if not tiktok_user.is_active:
        return ErrorsResponse({ "user": "该用户已禁用，请联系管理员"})
      
      tiktok_user.tiktokusers.session_key = session_key  # tiktokusers 表示关联的外键
      tiktok_user.tiktokusers.applet_openid = openid
      tiktok_user.tiktokusers.unionid = unionid
      tiktok_user.tiktokusers.avatar_url = avatar_url
      tiktok_user.tiktokusers.gender = gender
      tiktok_user.tiktokusers.nickname = nickname
      tiktok_user.tiktokusers.save()

      tiktok_user.nickname = nickname
      tiktok_user.avatar = avatar_url
      tiktok_user.gender = gender
      tiktok_user.save()

      resdata = TiktokAppleLoginSerializer.get_token(tiktok_user)
      return DataResponse(data=resdata)
    
    except Exception as e:  # 新用户
      with transaction.atomic():
        try:
          savepoint = transaction.savepoint()

          user = Users()
          user.username = openid

          # 先随机生成一个密码，防止别人获取openid直接被登录情况
          password = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
          user.set_password(password)
          user.user_type = 3  # 用户身份3表示普通用户

          user.nickname = nickname
          user.avatar = avatar_url
          user.save()

          TiktokUsers.objects.create(
            user=user, 
            session_key=session_key, 
            applet_openid=openid,
            avatar_url=avatar_url, 
            gender=gender, 
            nickname=nickname)
          
        except Exception as e:
          transaction.savepoint_rollback(savepoint)
          return ErrorsResponse({
            "error": str(e)
          })
        
        # 清除保存点
        transaction.savepoint_commit(savepoint)

        resdata = TiktokAppleLoginSerializer.get_token(user)
        return DataResponse(resdata)




