#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.urls import path, re_path

from rest_framework import routers

from .views import ccc

addr_router = routers.SimpleRouter()
addr_router.register(r"address", xxxView)

urlpatterns = [
    path("", ccc.as_view(), name="")
]

urlpatterns += addr_router.urls