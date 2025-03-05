#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import MonitorManage


class MonitorManageSerializer(serializers.ModelSerializer):
    """
    服务器监控 简单序列化器
    """

    class Meta:
        model = MonitorManage
        # fields = "__all__"
        exclude = ['dept_belong_id', 'modifier', 'creator', 'description']
        read_only_fields = ["id"]