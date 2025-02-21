#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from ..models import MonitorManage
from ..serializers import *

from comutils.viewset.viewset import CustomModelViewSet

class MonitorManageViewSet(CustomModelViewSet):
    """
    前端用户服务器监控
    get:
    前端用户服务器监控
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = MonitorManage.objects.all().order_by("create_datetime")
    serializer_class = MonitorManageSerializer

    # def getsysteminfo(self, request):
    #     data = system().GetSystemAllInfo()
    #     return DetailResponse(data=data)
