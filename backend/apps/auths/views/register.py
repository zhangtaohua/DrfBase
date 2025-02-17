#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re

from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from comutils.common import regex
from comutils.common.cache_keys import SMS_CODE_CK
from comutils.response.json_response import ErrorsResponse, BadRequestResponse, ValidationErrorResponse, DataResponse, SuccessResponse
from apps.users.models import Users

class RegisterView(APIView):
  authentication_classes = []
  permission_classes = []

  def post(self, request, *args, **kwargs):
    phone = request.data.get("phone")
    code = request.data.get("code")
    password = request.data.get("password")
    repeat_password = request.data.get("repeat_password")

    if phone is None or code is None or password is None or repeat_password is None:
      return BadRequestResponse(errros = {
        "error": "参数不能为空"
      })
    
    if len(password) < 6:
      return ValidationErrorResponse({
        "phone": "手机号长度不够"
      })
    
    # 验证手机号是否合法
    if not re.match(regex.MOBILE_PHONE_REGEX, phone):
        return ValidationErrorResponse(msg="请输入正确手机号")
    
    if not re.match(regex.CHAR_INT_PASSWORD_REGEX, password):
      return ValidationErrorResponse({
        "phone": "密码模式不对：字母及数字6到20位组合"
      })
    
    if password != repeat_password:
      return ValidationErrorResponse({
        "phone": "两次密码不一致"
      })
  
    if not re.match(r'^\d{6}$', code):
      return ValidationErrorResponse({
        "phone": "验证码不正确"
      })
    sent_code = cache.get(SMS_CODE_CK.format(phone))  # send_flag的值为bytes，需要转换成str ,,send_flag.decode()
    if not sent_code:  # 如果取不到标记，则说明验证码过期
        return ValidationErrorResponse({
          "phone": "短信验证码已过期"
        })
    else:
        if str(sent_code.decode()) != str(code):
            return ValidationErrorResponse({
              "phone": "验证码错误"
            })
        
        # 开始注册
        Users.objects.create(
           username=phone, phone=phone, 
           password=make_password(password), 
           mobile=phone,
           is_staff=False,
           identity=2)
        cache.delete(SMS_CODE_CK.format(phone))
        return SuccessResponse()

    
    


