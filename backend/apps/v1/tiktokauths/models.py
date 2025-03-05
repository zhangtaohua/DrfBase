#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import models
from django.conf import settings

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class TiktokUsers(BaseTimestampsModel):
  """
    抖音用户表
  """

  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                              help_text="用户", name="user", verbose_name="用户")
  
  applet_openid = models.CharField(max_length=150, db_index=True, null=True, blank=True,
                                         help_text="mini program openid", name="applet_openid", verbose_name="小程序openid")
  unionid = models.CharField(max_length=150, db_index=True, null=True, blank=True,
                            help_text="unionid", name="unionid", verbose_name="联合号")
  
  session_key = models.CharField(max_length=255, null=True, blank=True,
                                help_text="session key", name="session_key", verbose_name="后台认证key")
  applet_access_token = models.CharField(max_length=255, null=True, blank=True, 
                                      help_text="applet access token", name="applet_access_token", verbose_name="小程序access_token")
  applet_refresh_token = models.CharField(max_length=255, null=True, blank=True, 
                                      help_text="applet refresh token", name="applet_refresh_token", verbose_name="小程序refresh_token")

  nickname = models.CharField(max_length=150, null=True, blank=True,
                              help_text="nick name", name="nickname", verbose_name="昵称")
  language = models.CharField(max_length=40, null=True, blank=True,
                              help_text="language", name="language", verbose_name="语言")
  gender = models.CharField(max_length=100, null=True, blank=True,
                          help_text="gender", name="gender", verbose_name="性别") # 1男2女0未知
  country = models.CharField(max_length=100, null=True, blank=True,
                              help_text="country", name="country", verbose_name="国家")
  province = models.CharField(max_length=100, null=True, blank=True,
                              help_text="province", name="province", verbose_name="省")
  city = models.CharField(max_length=100, null=True, blank=True,
                          help_text="city", name="city", verbose_name="市")
  avatar_url = models.CharField(max_length=900, null=True, blank=True,
                             help_text="avatar url", name="avatar_url", verbose_name="用户头像")
  privilege = models.JSONField( null=True, blank=True,
                               help_text="privilege", name="privilege", verbose_name="用户特权信息")
  mobile = models.CharField(max_length=150, default="",
                            help_text="mobile", name="mobile", verbose_name="抖音小程序绑定的手机号码")

  class Meta:
    db_table = "rj_tiktok_users"
    verbose_name = "抖音用户数据"
    verbose_name_plural = verbose_name

  def __str__(self):
    if self.nickname:
      return self.nickname
    else:
      return self.user.username


