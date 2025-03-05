#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db.models import F

from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import MenuField, RoleMenuFieldPermission

from comutils.response.json_response import DataResponse


def merge_permission(data):
  """
  合并权限
  """
  result = {}

  for item in data:
    field_name = item.pop('field_name')
    if field_name not in result:
      result[field_name] = item
    else:
      for key, value in item.items():
        result[field_name][key] = result[field_name][key] or value
  return result


class FieldPermissionMixin:
  @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
  def field_permission(self, request):
    """
    获取字段权限
    """
    model = self.serializer_class.Meta.model.__name__
    user = request.user
    # 创建一个默认字典来存储最终的结果
    if user.is_superuser == 1:
      data = MenuField.objects.filter(model=model).values('field_name')
      result = {item['field_name']: {"is_create": True, "is_query": True, "is_update": True} for item in data}
    else:
      roles = request.user.role.values_list('id', flat=True)
      data = RoleMenuFieldPermission.objects.filter(
          field__model=model, role__in=roles
      ).values('is_create', 'is_query', 'is_update', field_name=F('field__field_name'))
      result = merge_permission(data)
      
    return DataResponse(data=result)