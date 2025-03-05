#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..models import Dept
from ..serializers import *

from comutils.response.json_response import DataResponse, ErrorsResponse
from comutils.viewset.viewset import CustomModelViewSet

class DeptViewSet(CustomModelViewSet):
  """
  部门管理接口
  list:查询
  create:新增
  update:修改
  retrieve:单例
  destroy:删除
  """
  queryset = Dept.objects.all()
  serializer_class = DeptSerializer
  create_serializer_class = DeptCreateUpdateSerializer
  update_serializer_class = DeptCreateUpdateSerializer
  filter_fields = ['name', 'id', 'parent']
  search_fields = []
  # extra_filter_class = []
  import_serializer_class = DeptImportSerializer
  import_field_dict = {
    "name": "部门名称",
    "key": "部门标识",
  }

  def list(self, request, *args, **kwargs):
    # 如果懒加载，则只返回父级
    request.query_params._mutable = True
    params = request.query_params
    parent = params.get('parent', None)
    page = params.get('page', None)
    limit = params.get('limit', None)
    if page:
      del params['page']
    if limit:
      del params['limit']
    if params and parent:
      queryset = self.queryset.filter(status=True, parent=parent)
    else:
      queryset = self.queryset.filter(status=True)
    queryset = self.filter_queryset(queryset)
    serializer = DeptSerializer(queryset, many=True, request=request)
    data = serializer.data
    return DataResponse(data=data)

  @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
  def all_dept(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    data = queryset.filter(status=True).order_by('sort').values('name', 'id', 'parent')
    return DetailResponse(data=data, msg="获取成功")

  @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
  def move_up(self, request):
    """部门上移"""
    dept_id = request.data.get('dept_id')
    try:
        dept = Dept.objects.get(id=dept_id)
    except Dept.DoesNotExist:
        return ErrorResponse(msg="部门不存在")
    previous_menu = Dept.objects.filter(sort__lt=dept.sort, parent=dept.parent).order_by('-sort').first()
    if previous_menu:
        previous_menu.sort, dept.sort = dept.sort, previous_menu.sort
        previous_menu.save()
        dept.save()
    return SuccessResponse(data=[], msg="上移成功")

  @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
  def move_down(self, request):
    """部门下移"""
    dept_id = request.data['dept_id']
    try:
        dept = Dept.objects.get(id=dept_id)
    except Dept.DoesNotExist:
        return ErrorResponse(msg="部门不存在")
    next_menu = Dept.objects.filter(sort__gt=dept.sort, parent=dept.parent).order_by('sort').first()
    if next_menu:
        next_menu.sort, dept.sort = dept.sort, next_menu.sort
        next_menu.save()
        dept.save()
    return SuccessResponse(data=[], msg="下移成功")

  @action(methods=['GET'], detail=False, permission_classes=[])
  def dept_info(self, request):
    """部门信息"""
    def inner(did, li):
        sub = Dept.objects.filter(parent_id=did)
        if not sub.exists():
            return li
        for i in sub:
            li.append(i.pk)
            inner(i, li)
        return li
    dept_id = request.query_params.get('dept_id')
    show_all = request.query_params.get('show_all')
    if dept_id is None:
        return ErrorResponse(msg="部门不存在")
    if not show_all:
        show_all = 0
    if int(show_all):  # 递归当前部门下的所有部门，查询用户
        all_did = [dept_id]
        inner(dept_id, all_did)
        users = Users.objects.filter(dept_id__in=all_did)
    else:
        if dept_id != '':
            users = Users.objects.filter(dept_id=dept_id)
        else:
            users = Users.objects.none()
    dept_obj = Dept.objects.get(id=dept_id) if dept_id != '' else None
    sub_dept = Dept.objects.filter(parent_id=dept_obj.pk) if dept_id != '' else []
    data = {
        'dept_name': dept_obj and dept_obj.name,
        'dept_user': users.count(),
        'owner': dept_obj and dept_obj.owner,
        'description': dept_obj and dept_obj.description,
        'gender': {
            'male': users.filter(gender=1).count(),
            'female': users.filter(gender=2).count(),
            'unknown': users.filter(gender=0).count(),
        },
        'sub_dept_map': []
    }
    for dept in sub_dept:
        all_did = [dept.pk]
        inner(dept.pk, all_did)
        sub_data = {
            'name': dept.name,
            'count': Users.objects.filter(dept_id__in=all_did).count()
        }
        data['sub_dept_map'].append(sub_data)
    return SuccessResponse(data)
