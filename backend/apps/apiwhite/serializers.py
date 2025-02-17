#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import ApiWhiteList

"""
  接口白名单-序列化器
"""
class ApiWhiteListSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = ApiWhiteList
    fields = "__all__"
    read_only_fields = ["id"]