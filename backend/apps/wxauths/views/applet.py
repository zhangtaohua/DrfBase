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
from ..models import WXUsers
from ..serializers import *

from conf import configs
from comutils.response.json_response import DataResponse, ErrorsResponse, ValidationErrorResponse
from apps.users.models import Users
# Create your views here.

"""
Mini Program Login
@params:
    str: jscode

流程
  1.使用微信小程序登录和获取用户信息Api接口
  2.把Api获取的用户资料和code发送给django后端
  3.通过微信接口把code换取成openid
  4.后端将openid作为用户名和密码
  5.后端通过JSON web token方式登录，把token和用户id传回小程序
  6.小程序将token和用户id保存在storage中
"""
class WxAppletLoginAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  @transaction.atomic
  def post(self, request):
    data = request.data
    jscode = data.get("jscode", None)
    inviter = data.get("inviter", None)

    if not jscode:
      errors= {
                "jscode": "This field is required"
              }
      return ErrorsResponse(errors)
      
    openid, session_key, unionid = WxAppletOpenId(jscode).get_openid()

    # 判断用户是否存在
    try:
      wxuser = Users.objects.get(username=openid)
      wxuser.wxusers.session_key = session_key  # wxusers 表示关联的外键
      wxuser.wxusers.applet_openid = openid
      wxuser.wxusers.unionid = unionid
      wxuser.wxusers.save()
      resdata = WxAppleLoginSerializer.get_token(wxuser)
      return DataResponse(data=resdata)
    except Exception as e:
      with transaction.atomic():
        try:
          savepoint = transaction.savepoint()
          user = Users()
          user.username = openid

          # 先随机生成一个密码，防止别人获取openid直接被登录情况
          password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
          user.set_password(password)
          user.user_type = 3  # 用户身份3表示普通用户
          user.save()

          WXUsers.objects.create(
            user=user,
            session_key=session_key,
            applet_openid=openid,
            unionid=unionid)
          
          # if inviter:  # 如果存在邀请码
          #   integral = FenXiaoManage.objects.filter(type=1, status=True).values_list('content', flat=True).first()
          #   if integral:  # 如果推广积分活动还存在
          #       Users.objects.filter(id=inviter).update(integral=F('integral') + int(integral))
          #       InviteRecord.objects.create(inv_user_id=inviter, invitee_user=user, get_integral=integral)
          #       IntegralRecord.objects.create(user_id=inviter,type=4,income=1,integral=integral)
        
        except Exception as e:
          transaction.savepoint_rollback(savepoint)
          return ErrorsResponse({
            "error": str(e)
          })
      
        # 清除保存点
        transaction.savepoint_commit(savepoint)
        resdata = WxAppleLoginSerializer.get_token(user)
        return DataResponse(resdata)
  
"""
post:

微信小程序手机号授权登录接口
微信小程序code获取openid，并解密前端传的手机号encryptedData加密数据
"""
class WxAppletMobileLoginAPIView(APIView):
  authentication_classes = []
  permission_classes = []

  @transaction.atomic
  def post(self, request):
    data = request.data
    jscode = data.get("jscode", None)
    inviter = data.get("inviter", None) #邀请码#为推广者的userid
    iv = data.get("iv", None)
    encrypted_data = data.get("encrypted_data", None)
    nickname = data.get("nickname", None)
    avatar_url = data.get("avatar_url", None)
    gender = data.get("gender", None)

    nickname = filter_emoji(nickname, '')
    hasErrors = False
    errors= {}
    if jscode is None:
      hasErrors = True
      errors["jscode"] =  "This field is required"
    
    if iv is None:
      hasErrors = True
      errors["jscode"] =  "This field is required"
    
    if encrypted_data is None:
      hasErrors = True
      errors["encrypted_data"] =  "This field is required"
    
    if avatar_url is None:
      hasErrors = True
      errors["avatar_url"] =  "This field is required"
    
    if hasErrors:
      return ErrorsResponse(errors)

    openid, session_key, unionid = WxAppletOpenId(jscode).get_openid()

    wxdc = WxCrypt(configs.WX_APPLET_APPID, session_key)
    pResult = wxdc.decrypt(encrypted_data, iv)

    #判断用户是否存在
    try:
      wxuser = Users.objects.get(username = openid)
      if not wxuser.is_active:
          return ErrorsResponse({ "user": "该用户已禁用，请联系管理员"})
      wxuser.wxusers.session_key = session_key #小写 wxusers 表示关联的外键
      wxuser.wxusers.applet_openid = openid
      wxuser.wxusers.unionid = unionid
      wxuser.wxusers.avatar_url = avatar_url
      wxuser.wxusers.sex = gender
      wxuser.wxusers.mobile = pResult['phoneNumber']
      wxuser.wxusers.nickname = nickname
      wxuser.wxusers.save()
      wxuser.nickname = nickname
      wxuser.avatar = avatar_url
      wxuser.gender = gender

      # wxuser.phone = pResult['phoneNumber']
      wxuser.mobile = pResult['phoneNumber']
      wxuser.save()

      resdata = WxAppleLoginSerializer.get_token(wxuser)
      return DataResponse(data=resdata)
    except Exception as e: # 新用户
      with transaction.atomic():
        try:
          savepoint = transaction.savepoint()
          user = Users()
          user.username = openid
          # 先随机生成一个密码，防止别人获取openid直接被登录情况
          password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
          user.set_password(password)
          user.user_type = 3  # 用户身份3表示普通用户

          user.nickname = nickname
          user.avatar = avatar_url
          user.mobile = pResult['phoneNumber']
          user.gender = gender

          user.save()

          WXUsers.objects.create(
            user=user,
            session_key=session_key,
            applet_openid=openid,
            avatar_url=avatar_url,
            sex=gender,
            mobile=pResult['phoneNumber'],
            nickname=nickname)
          

          # if inviter:#如果存在邀请码
          #   integral = FenXiaoManage.objects.filter(type=1,status=True).values_list('content',flat=True).first()
          #   if integral:#如果推广积分活动还存在
          #     Users.objects.filter(id=inviter).update(integral=F('integral')+int(integral))
          #     InviteRecord.objects.create(inv_user_id=inviter,invitee_user=user,get_integral=integral)
          #     IntegralRecord.objects.create(user_id=inviter, type=4, income=1, integral=integral)
        
        except Exception as e:
            transaction.savepoint_rollback(savepoint)
            return ErrorsResponse({
              "error": str(e)
            })
        
        # 清除保存点
        transaction.savepoint_commit(savepoint)
        resdata = WxAppleLoginSerializer.get_token(user)
        return DataResponse(resdata)


"""
微信小程序更新用户信息
@params:
    str:encryptedData
    str:iv
"""
class WxAppletUserInfoUpdateAPIView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    data = request.data
    iv = data.get("iv", None)
    encrypted_data = data.get("encrypted_data", None)

    hasErrors = False
    errors= {}
    if iv is None:
      hasErrors = True
      errors["iv"] =  "This field is required"
    
    if encrypted_data is None:
      hasErrors = True
      errors["encrypted_data"] =  "This field is required"

    if hasErrors:
      return ErrorsResponse(errors)
    
    wxuser = WXUsers.objects.filter(user=request.user).first()

    if not wxuser:
      return ErrorsResponse({"error": "No such user"})

    wxdc = WxCrypt(configs.WX_APPLET_APPID, wxuser.session_key)

    user = wxdc.decrypt(encrypted_data, iv)

    wxuser.nickname = user['nickName']
    wxuser.sex = user['gender']
    wxuser.language = user['language']
    wxuser.city = user['city']
    wxuser.avatar_url = user['avatarUrl']
    wxuser.save()

    # 关联用户
    myuser = request.user
    myuser.nickname = user['nickName']
    myuser.avatar = user['avatarUrl']
    myuser.save()

    resdata = WxAppleLoginSerializer.get_token(myuser)

    return DataResponse({
      "user": user,
      "token": resdata
    })


"""
微信小程序获取推广二维码
    
@params:
    scene 分享用户的userid
    page 要跳转的页面
"""

class WxAppletShareQrcodeAPIView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    data = request.data
    scene = data.get("scene", None) # 分享用户的userid
    page = data.get("page", None)

    hasErrors = False
    errors= {}
    if scene is None:
      hasErrors = True
      errors["scene"] =  "This field is required"
    
    if page is None:
      hasErrors = True
      errors["page"] =  "This field is required"

    if hasErrors:
      return ErrorsResponse(errors)
    
    access_token = WxAppletAccessToken().get_access_token()
    qrcode_img_url = WxAppletQrcode(access_token, scene, page).get_qrcode()
    
    print("qrcode_url", qrcode_img_url)
    res_data = {
      "qrcode": qrcode_img_url
    }

    return DataResponse(res_data)

