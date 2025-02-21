#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.conf import settings
from django.db import models

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class MonitorManage(BaseTimestampsModel):
    ip = models.CharField(max_length=50, verbose_name="服务器IP", null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name="名称",null=True,blank=True)
    os = models.CharField(max_length=50, verbose_name="系统名称", null=True, blank=True)#windows、centos、小写
    online = models.BooleanField(default=False,verbose_name="在线状态")
    status = models.BooleanField(default=True,verbose_name="监控状态")#True开启 False关闭
    days = models.SmallIntegerField(default=30, verbose_name="日志保留天数")
    interval = models.SmallIntegerField(default=5, verbose_name="监控日志刷新间隔")
    islocal = models.BooleanField(default=False,verbose_name="是否是本机监控")

    class Meta:
        db_table = 'rj_monitor'
        verbose_name = "服务监控"
        verbose_name_plural = verbose_name