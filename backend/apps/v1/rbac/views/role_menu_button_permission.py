#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django_filters.rest_framework import FilterSet, CharFilter

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from ..serializers import *

from ..models import RoleMenuPermission

from comutils.response.json_response import DataResponse, ErrorsResponse
from comutils.viewset.viewset import CustomModelViewSet
from comutils.mixins.fastcrud_mixins import FastCrudMixin


class RoleMenuButtonPermissionViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = RoleMenuButtonPermission.objects.all()
    serializer_class = RoleMenuButtonPermissionSerializer
    create_serializer_class = RoleMenuButtonPermissionCreateUpdateSerializer
    update_serializer_class = RoleMenuButtonPermissionCreateUpdateSerializer
    extra_filter_class = []

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_role_menu(self, request):
        """
        获取 角色-菜单
        :param request:
        :return:
        """
        menu_queryset = Menu.objects.all()
        serializer = RoleMenuSerializer(menu_queryset, many=True, request=request)
        return DetailResponse(data=serializer.data)

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def set_role_menu(self, request):
        """
        设置 角色-菜单
        :param request:
        :return:
        """
        data = request.data
        roleId = data.get('roleId')
        menuId = data.get('menuId')
        isCheck = data.get('isCheck')
        if isCheck:
            # 添加权限：创建关联记录
            instance = RoleMenuPermission.objects.create(role_id=roleId, menu_id=menuId)
        else:
            # 删除权限：移除关联记录
            RoleMenuPermission.objects.filter(role_id=roleId, menu_id=menuId).delete()
        menu_instance = Menu.objects.get(id=menuId)
        serializer = RoleMenuSerializer(menu_instance, request=request)
        return DetailResponse(data=serializer.data, msg="更新成功")

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_role_menu_btn_field(self, request):
        """
        获取 角色-菜单-按钮-列字段
        :param request:
        :return:
        """
        params = request.query_params
        menuId = params.get('menuId', None)
        menu_btn_queryset = MenuButton.objects.filter(menu_id=menuId)
        menu_btn_serializer = RoleMenuButtonSerializer(menu_btn_queryset, many=True, request=request)
        menu_field_queryset = MenuField.objects.filter(menu_id=menuId)
        menu_field_serializer = RoleMenuFieldSerializer(menu_field_queryset, many=True, request=request)
        return DetailResponse(data={'menu_btn': menu_btn_serializer.data, 'menu_field': menu_field_serializer.data})

    @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
    def set_role_menu_field(self, request, pk):
        """
        设置 角色-菜单-列字段
        """
        data = request.data
        for col in data:
            FieldPermission.objects.update_or_create(
                role_id=pk, field_id=col.get('id'),
                defaults={
                    'is_create': col.get('is_create'),
                    'is_update': col.get('is_update'),
                    'is_query': col.get('is_query'),
                })

        return DetailResponse(data=[], msg="更新成功")

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def set_role_menu_btn(self, request):
        """
        设置 角色-菜单-按钮
        """
        data = request.data
        isCheck = data.get('isCheck', None)
        roleId = data.get('roleId', None)
        btnId = data.get('btnId', None)
        if isCheck:
            # 添加权限：创建关联记录
            RoleMenuButtonPermission.objects.create(role_id=roleId, menu_button_id=btnId)
        else:
            # 删除权限：移除关联记录
            RoleMenuButtonPermission.objects.filter(role_id=roleId, menu_button_id=btnId).delete()
        menu_btn_instance = MenuButton.objects.get(id=btnId)
        serializer = RoleMenuButtonSerializer(menu_btn_instance, request=request)
        return DetailResponse(data=serializer.data, msg="更新成功")

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def set_role_menu_btn_data_range(self, request):
        """
        设置 角色-菜单-按钮-权限
        """
        data = request.data
        instance = RoleMenuButtonPermission.objects.get(id=data.get('role_menu_btn_perm_id'))
        instance.data_range = data.get('data_range')
        instance.dept.add(*data.get('dept'))
        if not data.get('dept'):
            instance.dept.clear()
        instance.save()
        serializer = RoleMenuButtonPermissionSerializer(instance, request=request)
        return DetailResponse(data=serializer.data, msg="更新成功")

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def role_to_dept_all(self, request):
        """
        当前用户角色下所能授权的部门:角色授权页面使用
        :param request:
        :return:
        """
        is_superuser = request.user.is_superuser
        params = request.query_params
        # 当前登录用户的角色
        role_list = request.user.role.values_list('id', flat=True)

        menu_button_id = params.get('menu_button')
        # 当前登录用户角色可以分配的自定义部门权限
        dept_checked_disabled = RoleMenuButtonPermission.objects.filter(
            role_id__in=role_list, menu_button_id=menu_button_id
        ).values_list('dept', flat=True)
        dept_list = Dept.objects.values('id', 'name', 'parent')

        data = []
        for dept in dept_list:
            dept["disabled"] = False if is_superuser else dept["id"] not in dept_checked_disabled
            data.append(dept)
        return DetailResponse(data=data)
