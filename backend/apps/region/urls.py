#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


"""
@Remark: 中国行政区模块的 URL 配置
"""


from django.urls import path, re_path

from rest_framework import routers

from .views.region import RegionViewSet, ProvincesView, SubRegionsView, GetProvinceAreasListView, AreaViewSet

region_router = routers.SimpleRouter()

region_router.register(r"", RegionViewSet)

# 方案二
# region_router.register(r"", AreaViewSet)

urlpatterns = [
    re_path('root/', RegionViewSet.as_view({'get': 'region_root'})),
    re_path('provinces/', RegionViewSet.as_view({'get': 'region_root'})),
]

urlpatterns += region_router.urls





