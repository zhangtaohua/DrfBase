#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import OperationLog, LoginLog


class OperationLogSerializer(serializers.ModelSerializer):
  """
  操作日志-序列化器
  """

  class Meta:
    model = OperationLog
    fields = "__all__"
    read_only_fields = ["id"]

class OperationLogCreateUpdateSerializer(serializers.ModelSerializer):
    """
    操作日志-创建/更新时的列化器
    """

    class Meta:
        model = OperationLog
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):
  """
  登录日志-序列化器
  """
  
  class Meta:
    model = LoginLog
    fields = "__all__"
    read_only_fields = ["id"]