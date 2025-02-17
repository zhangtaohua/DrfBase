#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django_filters.rest_framework import FilterSet, CharFilter


from ..serializers import *

from ..models import Role

from comutils.response.json_response import DataResponse
from comutils.viewset.viewset import CustomModelViewSet


class RoleViewSet(CustomModelViewSet, FastCrudMixin, FieldPermissionMixin):
  """
  角色管理接口
  list:查询
  create:新增
  update:修改
  retrieve:单例
  destroy:删除
  """
  queryset = Role.objects.all()
  serializer_class = RoleSerializer
  create_serializer_class = RoleCreateUpdateSerializer
  update_serializer_class = RoleCreateUpdateSerializer
  search_fields = ['name', 'key']

  @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
  def set_role_users(self, request, pk):
      """
      设置 角色-用户
      :param request:
      :return:
      """
      data = request.data
      direction = data.get('direction')
      movedKeys = data.get('movedKeys')
      role = Role.objects.get(pk=pk)
      if direction == "left":
          # left : 移除用户权限
          role.users_set.remove(*movedKeys)
      else:
          # right : 添加用户权限
          role.users_set.add(*movedKeys)
      serializer = RoleSerializer(role)
      return DetailResponse(data=serializer.data, msg="更新成功")
