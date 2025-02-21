#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.core.cache import cache

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import *

from ..models import Region

from comutils.response.json_response import DataResponse, ErrorsResponse
from comutils.viewset.viewset import CustomModelViewSet

"""
  地区管理接口:
  list:查询
  create:新增
  update:修改
  retrieve:单例
  destroy:删除
"""

class RegionViewSet(CustomModelViewSet):

  queryset = Region.objects.all().order_by("id")
  serializer_class = RegionSerializer
  filterset_fields = ["status", "id", "parent"]
  search_fields = ("name",)

  def region_root(self, request):
    queryset = self.filter_queryset(self.get_queryset())
    queryset = queryset.filter(parent__isnull=True).order_by("id")
    serializer = RegionSerializer(queryset, many=True)
    return DataResponse(data=serializer.data)
  

"""
  查询省数据
  get:
  查询省数据，补充缓存逻辑
  请求方式： GET /regions/
"""
class ProvincesView(APIView):
  # permission_classes = [IsAuthenticated]
  # authentication_classes = [JWTAuthentication]

  def get(self, request):
    #补充缓存逻辑
    province_list = cache.get("province_list")
    if not province_list:
      try:
        province_model_list = Region.objects.filter(parent__isnull=True).order_by("id")
        province_list = []
        for province_model in province_model_list:
            province_list.append({"id": province_model.id,"name": province_model.name})
        # 增加: 缓存省级数据
        cache.set("province_list", province_list, 3600)
      except Exception as e:
        return ErrorsResponse({"error": "省份数据错误"})
    return DataResponse(data=province_list)


"""
  查询市或区数据
  get:
  子级地区：市和区县
  请求方式： GET /regions/(?P<pk>[1-9]\d+)/
"""
class SubRegionsView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  """提供市或区地区数据
    1.查询市或区数据
    2.序列化市或区数据
    3.响应市或区数据
    4.补充缓存数据
  """
  def get(self, request, pk):
    # 判断是否有缓存
    sub_data = cache.get("sub_region_" + pk)

    if not sub_data:
      # 1.查询市或区数据
      try:
        sub_model_list = Region.objects.filter(parent=pk).order_by("id")
        # 查询市或区的父级
        parent_model = Region.objects.get(id=pk)

        # 2.序列化市或区数据
        sub_list = []
        for sub_model in sub_model_list:
          sub_list.append({"id": sub_model.id, "name": sub_model.name})

        sub_data = {
          "id":parent_model.id, # pk
          "name":parent_model.name,
          "subs": sub_list
        }

        # 缓存市或区数据
        cache.set("sub_region_" + pk, sub_data, 3600)
      except Exception as e:
        return ErrorsResponse({"error": "城市或区县数据错误"})

    # 3.响应市或区数据
    return DataResponse(data=sub_data)
  

# TODO
# 抄过来了未调试
"""
  获取结构树
  :param datas:
  :return:
"""
def MakeRegionTree(datas):
  lists=[]
  tree={}
  parent_id=""
  
  for s in datas:
    item=s
    tree[item["id"]]=item
  root=None
  for i in datas:
    obj=i
    if not obj["pid"]:#判断根评论
      root=tree[obj["id"]]
      lists.append(root)#添加到列表
      if "childlist" not in tree[obj["id"]]:
        tree[obj["id"]]["childlist"] = []
    else:
      parent_id=obj["pid"]
      if "childlist" not in tree[parent_id]:
        tree[parent_id]["childlist"]=[]
      tree[parent_id]["childlist"].append(tree[obj["id"]])
  return lists


"""
  递归获取所有省市区
  get:
  递归获取所有省市区
"""
class GetProvinceAreasListView(APIView):
 
  permission_classes = []
  authentication_classes = []
  # permission_classes = [IsAuthenticated]
  # authentication_classes = [JWTAuthentication]

  def get(self, request):
      queryset_ser  = RegionSimpleSerializer(Region.objects.filter(status=True).order_by("id"), many=True)
      queryset_list = MakeRegionTree(queryset_ser.data)
      return DataResponse(data=queryset_list)



# TODO 
# 方案二

class AreaViewSet(CustomModelViewSet):
  """
  地区管理接口
  list:查询
  create:新增
  update:修改
  retrieve:单例
  destroy:删除
  """
  queryset = Region.objects.all()
  serializer_class = RegionSerializer
  create_serializer_class = RegionCreateUpdateSerializer
  update_serializer_class = RegionCreateUpdateSerializer
  extra_filter_class = []

  def list(self, request, *args, **kwargs):
    self.request.query_params._mutable = True
    params = self.request.query_params
    known_params = {'page', 'limit', 'pcode'}
    # 使用集合操作检查是否有未知参数
    other_params_exist = any(param not in known_params for param in params)
    if other_params_exist:
      queryset = self.queryset.filter(status=True)
    else:
      pcode = params.get('pcode', None)
      params['limit'] = 999
      if params and pcode:
        queryset = self.queryset.filter(status=True, pcode=pcode)
      else:
        queryset = self.queryset.filter(status=True, level=1)
    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer(queryset, many=True)
    return DataResponse(data=serializer.data, msg="获取成功")
