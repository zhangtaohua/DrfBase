#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, APIException

from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from apps.users.serializers import UserSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from comutils.common import regex
from apps.users.models import Users

def valid_username(username=None):
  if not username:
    raise APIException("用户名不能为空")
  # else:
  #   if not re.match(regex.XX, username):
  #     raise APIException("用户名格式不正确")
  
  return username


def valid_phone(phone=None):
  if not phone:
    raise APIException("手机号不能为空")
  else:
    if not re.match(regex.MOBILE_PHONE_REGEX, phone):
      raise APIException("请输入正确手机号")
  
  return phone

def valid_email(email=None):
  if not email:
    raise APIException("邮箱不能为空")
  # else:
  #   if not re.match(regex.XX, email):
  #     raise APIException("邮箱格式不正确")
  
  return email

def valid_sms_code(code=None, used_for=None):
  if not code:
    raise APIException("短信验证码不能为空")
  # TODO 验证短信验证码
    # else:
      # if not re.match(regex.CHAR_INT_PASSWORD_REGEX, code):
      #   return APIException("密码模式不对：字母及数字6到20位组合")
  
  return code

def valid_password(password=None, name="密码"):
  if not password:
    raise APIException("{}不能为空".format(name))
  # else:
    # if not re.match(regex.CHAR_INT_PASSWORD_REGEX, password):
    #   raise APIException("密码模式不对：字母及数字6到20位组合")

  return password

def valid_repeat_password(password=None, repeat_password=None):
  valid_password(password)
  valid_password(repeat_password,"重复密码")

  if password != repeat_password:
    raise APIException("两次输入的密码不相同")
  
  return password


def valid_user_password(user=None, password=None):
  valid_password(password)

  if not user.check_password(password):
      raise APIException("用户名或密码错误")

  return password

def get_user(username=None, phone=None, email=None, password=None):
  if not username and not phone and not email:
      raise APIException("用户名、手机号、邮箱至少填写一个")
  
  condition = None
  user = None
  if username:
    valid_username(username)
    # user = Users.objects.filter(username=username).first()
    condition = Q(username=username)

  if phone:
    valid_phone(phone)
    # user = Users.objects.filter(phone=phone).first()
    if condition:
      condition = condition | Q(phone=phone)
    else:
      condition = Q(phone=phone)

  if email:
    valid_email(email)
    # user = Users.objects.filter(email=email).first()
    if condition:
      condition = condition | Q(email=email)
    else:
      condition = Q(email=email)
  
  user = Users.objects.filter(condition).first()
  if not user:
      raise APIException("用户不存在")
  
  if password:
    valid_user_password(user=user, password=password)
  
  user_serializer = UserSerializer(instance=user)

  token = RefreshToken.for_user(user)
  # token = TokenObtainPairSerializer.get_token(user)

  return {
    "user": user,
    "serializer": user_serializer,
    "token": token,
    "access_token": str(token.access_token),
    "refresh_token": str(token)
  }


class TokenObtainWithUserSerializer(TokenObtainPairSerializer): 

  def validate(self, attrs):
    data = super().validate(attrs) 
    user_serializer =UserSerializer(instance=self.user)

    # 统一返回数据格式
    redata = {
      "user": user_serializer.data,
      "access_token": data["access"],
      "refresh_token": data["refresh"]
    }
    return redata

  # 方案二 重写 get_token ,也要重写 validate， 并继承 TokenObtainSerializer
  # def validate(self, attrs):
  #   super().validate(attrs)
  #   data = self.get_token(self.user)
  #   return data
  
  # @classmethod
  # def get_token(cls, user):
  #   refresh = RefreshToken.for_user(user)
  #   # 下面是错的
  #   # refresh = super(TokenObtainWithUserSerializer,cls).get_token(user)

  #   user_serializer =UserSerializer(instance=user)
  #   data = {
  #     "user": user_serializer.data,
  #     "access_token": str(refresh.access_token),
  #     "refresh_token": str(refresh)
  #   }
  #   return data

class UnifiedTokenRefreshSerializer(TokenRefreshSerializer): 

  def validate(self, attrs):
    data = super().validate(attrs) 

    # 统一返回数据格式
    redata = {
      "access_token": data["access"],
    }

    refresh_token = data.get("refresh", "")
    if refresh_token:
      redata["refresh_token"] = refresh_token

    return redata

class UserPasswordLoginSerializer(serializers.ModelSerializer):
  # 需要重写字段，不重写，字段自己规则过不了
  username = serializers.CharField(required=False)

  class Meta:
    model = Users
    fields = "__all__"
    extra_kwargs = {
      "password": {"required": True, "write_only": True},
      "phone": {"required": False},
      "email": {"required": False},
    }

  def validate(self, attrs):
    username = attrs.get("username")
    password = attrs.get("password")
    phone = attrs.get("phone")
    email = attrs.get("email")

    user_obj = get_user(username, phone, email, password)

    # self.context["user"] = user_obj["user"]
    # self.context["access_token"] = user_obj["access_token"]
    # self.context["refresh_token"] = user_obj["refresh_token"]
    # return attrs

    print("userobj", user_obj["serializer"].data)

    data = {
      "user": user_obj["serializer"].data,
      "access_token": user_obj["access_token"],
      "refresh_token": user_obj["refresh_token"],
    }
    return data
  
# 留着做参考
class UserPasswordLoginSerializerV2(serializers.Serializer):
  username = serializers.CharField(required=False)
  password = serializers.CharField(write_only=True, required=True)
  phone = serializers.CharField(required=False)
  email = serializers.EmailField(required=False)

  def validate(self, attrs):
    username = attrs.get("username")
    password = attrs.get("password")
    phone = attrs.get("phone")
    email = attrs.get("email")

    if not password:
      raise APIException("密码不能为空")
    if not username and not phone and not email:
      raise APIException("用户名、手机号、邮箱至少填写一个")
    
    condition = Q(username=username) | Q(phone=phone) | Q(email=email)
    # user = Users.objects.filter(condition, password=password).first()
    user = Users.objects.filter(condition).first()
    
    if not user:
      raise APIException("用户不存在")
    
    if not user.check_password(password):
      raise APIException("用户名或密码错误")
    
    token = RefreshToken.for_user(user)
    # token = TokenObtainPairSerializer.get_token(user)
    self.context["user"] = user
    self.context["access_token"] = str(token.access_token)
    self.context["refresh_token"] = str(token)

    data = {
      "user": user,
      "access_token": str(token.access_token),
      "refresh_token": str(token)
    }
    # return data
    return attrs
  
class PhonePasswordSerializer(serializers.Serializer):
  # 需要重写字段，不重写，字段自己规则过不了
  phone = serializers.CharField(required=True)
  password = serializers.CharField(write_only=True, required=True)

  def validate(self, attrs):
    phone = attrs.get("phone")
    password = attrs.get("password")

    user_obj = get_user(phone=phone, password=password)
    data = {
      "user": user_obj["serializer"].data,
      "access_token": user_obj["access_token"],
      "refresh_token": user_obj["refresh_token"],
    }
    return data
  

class PhoneSMSCodeLoginSerializer(serializers.Serializer):
  # 需要重写字段，不重写，字段自己规则过不了
  phone = serializers.CharField(required=True)
  code = serializers.CharField(write_only=True, required=True)

  def validate(self, attrs):
    phone = attrs.get("phone")
    code = attrs.get("code")

    valid_sms_code(code, None)
    
    user_obj = get_user(phone=phone)
    data = {
      "user": user_obj["serializer"].data,
      "access_token": user_obj["access_token"],
      "refresh_token": user_obj["refresh_token"],
    }
    return data


class ResetPasswordSerializer(serializers.Serializer):
  # 需要重写字段，不重写，字段自己规则过不了
  username = serializers.CharField(required=False)
  phone = serializers.CharField(required=False)
  email = serializers.EmailField(required=False)
  old_password = serializers.CharField(write_only=True, required=True)
  password = serializers.CharField(write_only=True, required=True)
  repeat_password = serializers.CharField(write_only=True, required=True)

  def validate(self, attrs):
    username = attrs.get("username")
    phone = attrs.get("phone")
    email = attrs.get("email")
    old_password = attrs.get("old_password")
    password = attrs.get("password")
    repeat_password = attrs.get("repeat_password")


    valid_repeat_password(password, repeat_password)
    user_obj = get_user(username, phone, email, old_password)

    user = user_obj["user"]
    print("NND", user)
    user.set_password(password)
    user.save()

    data = {
      "user": user_obj["serializer"].data,
      "access_token": user_obj["access_token"],
      "refresh_token": user_obj["refresh_token"],
    }
    return data
  

class ResetPasswordByPhoneCodeSerializer(serializers.Serializer):
  # 需要重写字段，不重写，字段自己规则过不了
  phone = serializers.CharField(required=True)
  code = serializers.CharField(write_only=True, required=True)
  password = serializers.CharField(write_only=True, required=True)
  repeat_password = serializers.CharField(write_only=True, required=True)

  def validate(self, attrs):
    phone = attrs.get("phone")
    code = attrs.get("code")
    password = attrs.get("password")
    repeat_password = attrs.get("repeat_password")

    valid_sms_code(code, None)
    valid_repeat_password(password, repeat_password)
    
    
    user_obj = get_user(phone=phone)
    user = user_obj["user"]
    user.set_password(password)
    user.save()

    data = {
      "user": user_obj["serializer"].data,
      "access_token": user_obj["access_token"],
      "refresh_token": user_obj["refresh_token"],
    }
    return data
  