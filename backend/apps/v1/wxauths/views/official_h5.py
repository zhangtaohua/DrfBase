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
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from ..utils import WxOfficialPlatform, WxOfficialAccountH5
from ..models import WXUsers
from ..serializers import *

from conf import configs
from comutils.common.regex import MOBILE_PHONE_REGEX

from comutils.response.json_response import DataResponse, ErrorsResponse, ValidationErrorResponse
from apps.v1.users.models import Users
# Create your views here.

WXOP = WxOfficialPlatform()
WXOCH5 = WxOfficialAccountH5()


"""
公众号获取js sdk调用需要的临时签名信息
get:
  公众号获取js sdk调用需要的临时签名信息
"""
class WxOfficialAccountH5JSSDKTempSignAPIView(APIView):
   
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    data = request.data

    #参与临时签名需要前端传递自己当前页面的url地址
    url = data.get("code", None)

    temp_sign_data = WxAppPay().get_gzh_h5_js_sign(url)
    if not temp_sign_data:
      errors = {
        "error": "获取失败，请稍后再试"
      }
      return ErrorsResponse(errors)
    
    return DataResponse({
      "sign": temp_sign_data
    })

"""
接口配置：校验微信发送的验证信息

get:
  微信会发送随机字符，校验服务器是否真实存在
"""

class WxOfficialAccoutCheckH5APIView(APIView):

  permission_classes = []
  authentication_classes = []

  def get(self, request):
    data = request.data
    
    signature = data.get("signature", None)
    timestamp = data.get("timestamp", None)
    nonce = data.get("nonce", None)
    echostr = data.get("echostr", None)

    token = configs.WX_OFFICIAL_ACCOUNT_TOKEN
    if not WXOCH5.wx_h5_checkSignature(token, timestamp, nonce, signature):
      
      return HttpResponse('fail')
    
    return HttpResponse(echostr)
    

"""
微信公众号H5网页授权登录接口

post:
微信公众号网页授权登录接口
微信公众号code获取openid和access_token，新用户获取用户信息（昵称头像等）：
引导用户访问例如如下授权链接：
https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx9747c4bf89d5ce34&redirect_uri=http%3A%2F%2Fdvlyadmin.lybbn.cn%2Fapi%2Fxcx%2Fwxh5login%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
也可以使用拼接
redirect_uri = parse.quote("%s/api/h5/wxh5login/"%configs.DOMAIN_HOST)
#snsapi_base\snsapi_userinfo
link = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect"%(WX_GZH_APPID,redirect_uri,code)
"""
class WxOfficialAccountLoginAPIView(APIView):
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
      
    openid_tokens = WXOCH5.get_openid_tokens(code)
    openid = openid_tokens["openid"]
    access_token = openid_tokens["access_token"]

    #判断用户是否存在(根据openID判断用户是否是第一次登陆)
    user = Users.objects.filter(
      is_active=True, 
      wxusers__official_account_openid=openid
      ).first()
    
    if not user:#如果不存在则提示绑定用户关系
      user_infos = WXOP.get_userinfo(access_token, openid)

      user = Users()

      user.username = openid
      # 先随机生成一个密码，防止别人获取openid直接被登录情况
      password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
      user.set_password(password)
      user.user_type = 3  # 用户身份3表示普通用户

      user.nickname = user_infos["nickname"]
      user.avatar = user_infos["headimgurl"]
      user.gender = user_infos["sex"]

      user.save()

      WXUsers.objects.create(
        user=user, 
        official_account_openid=openid,
        avatar_url=user_infos["headimgurl"],
        nickname=user_infos["nickname"],
        sex=user_infos["sex"],
        official_account_access_token=access_token)

    resdata = WxAppleLoginSerializer.get_token(user)
    return DataResponse(resdata)
  
