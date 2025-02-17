#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import models

from comutils.models.models import BaseTimestampsModel

# Create your models here.
class ApiWhiteList(BaseTimestampsModel):
  url = models.CharField(max_length=255, 
                         help_text="url地址", name="url", verbose_name="url")
  
  METHOD_CHOICES = (
    (0, "GET"),
    (1, "POST"),
    (2, "PUT"),
    (3, "DELETE"),
  )
  method = models.IntegerField(default=0, null=True, blank=True,
                               help_text="request method", name="method", verbose_name="接口请求方法")
  
  enable_datasource = models.BooleanField(default=True, null=True, blank=True,
                                        help_text="激活数据权限", name="enable_datasource", verbose_name="激活数据权限")

  class Meta:
    db_table = "rj_api_white_list"
    verbose_name = "接口白名单"
    verbose_name_plural = verbose_name
    ordering = ("-create_time",)