#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from ..models import LoginLog
from ..serializers import *

from comutils.viewset.viewset import CustomModelViewSet

"""
  接口白名单
  list:查询
  create:新增
  update:修改
  retrieve:单例
  destroy:删除
"""
class LoginLogViewSet(CustomModelViewSet):
    
    queryset = LoginLog.objects.all().order_by("-create_time")
    serializer_class = LoginLogSerializer
    # permission_classes = []
