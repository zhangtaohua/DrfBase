#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from ..models import OperationLog
from ..serializers import *

from comutils.viewset.viewset import CustomModelViewSet


class OperationLogViewSet(CustomModelViewSet):
    """
      操作日志
      list:查询
      create:新增
      update:修改
      retrieve:单例
      destroy:删除
    """
    
    queryset = OperationLog.objects.all().order_by("-create_time")
    serializer_class = OperationLogSerializer
    # permission_classes = []
