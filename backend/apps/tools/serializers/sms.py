#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re

from django.core.cache import cache

from rest_framework import serializers

from comutils.common.regex import MOBILE_PHONE_REGEX
from apps.users.models import Users

class SmsCodeSerializer(serializers.Serializer):
   phone = serializers.CharField(max_length=11, required=True, help_text="手机号")

   def validate_phone(self, phone):
      if not re.match(MOBILE_PHONE_REGEX, phone):
         raise serializers.ValidationError("手机号格式不正确")
      
      # TODO 
      # 从缓存中获取手机号是否已获取验证码
      # 判断一定时间里只能调用一次这个接口
      sent_flag = cache.get("sms_sent_{}".format(phone))
      if sent_flag:
        raise serializers.ValidationError("每120秒可再次获取验证码")
      
      return phone

class SmsUsersSerializer(serializers.Serializer):
  phone = serializers.CharField(max_length=11, required=True, help_text="手机号") 
  smstype = serializers.CharField(max_length=10, required=True, help_text="短信类型")

  def validate_phone(self, phone):
    if not re.match(MOBILE_PHONE_REGEX, phone):
      raise serializers.ValidationError("手机号格式不正确")
    
    smstype_req = self.context["smstype"]
    
    if smstype_req == "register":
      if Users.objects.filter(phone=phone).exists():
      # if Users.objects.filter(phone=phone).count():
        raise serializers.ValidationError("手机号已经注册")
      
    if smstype_req == "login" or smstype_req == "change_password":
      if not Users.objects.filter(phone=phone).count():
        raise serializers.ValidationError("用户不存在")
      # TODO 判断用户是否禁用
      # if not Users.objects.filter(username=mobile,identity=2,is_active=True).count():
      #   raise serializers.ValidationError("没有找到该用户或已禁用",400)

    if smstype_req == "wxbind":#微信绑定
      if not Users.objects.filter(username=phone, phone=phone, identity=2, is_active=True, oauthwxuser__isnull=True).count():
          raise serializers.ValidationError("没有找到该用户或该用户已绑定微信",400)

    if smstype_req == "rebind":#换绑手机号，前提用户已经登录
        #是否跟原来绑定过的号码一致
        mqueryset = Users.objects.filter(id = self.context['request'].user.id)
        if not mqueryset:
            raise serializers.ValidationError("该用户不存在", 400)
        if mqueryset[0].phone == phone:
            raise serializers.ValidationError("请使用新的手机号绑定", 400)
        if Users.objects.filter(phone=phone).count():
            raise serializers.ValidationError("该手机号已被其他用户绑定",400)

      
    return phone
