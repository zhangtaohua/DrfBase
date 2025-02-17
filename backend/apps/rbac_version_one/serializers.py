#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from .models import Role, Post, Dept, Menu, MenuField, MenuButton, RoleMenuPermission, RoleMenuFieldPermission,  RoleMenuButtonPermission

Users = settings.AUTH_USER_MODEL


class MenuFieldSerializer(serializers.ModelSerializer):
  """
  菜单字段-列权限序列化器
  """

  class Meta:
    model = MenuField
    fields = "__all__"
    read_only_fields = ["id"]


class MenuFieldCreateUpdateSerializer(serializers.ModelSerializer):
  """
  初始化菜单字段-列权限序列化器
  """
  class Meta:
    model = MenuButton
    fields = "__all__"
    read_only_fields = ["id"]


class MenuButtonSerializer(serializers.ModelSerializer):
  """
  菜单按钮-序列化器
  """

  class Meta:
    model = MenuButton
    fields = ["id", "name", "value", "api", "method","menu"]
    read_only_fields = ["id"]


class MenuButtonCreateUpdateSerializer(serializers.ModelSerializer):
  """
  初始化菜单按钮-序列化器
  """

  class Meta:
    model = MenuButton
    fields = "__all__"
    read_only_fields = ["id"]


class MenuSerializer(serializers.ModelSerializer):
  """
  菜单表的简单序列化器
  """
  menu_button = serializers.SerializerMethodField(read_only=True)
  has_children = serializers.SerializerMethodField()

  def get_menu_button(self, obj):
    # 以下是有 MenuButton 相关联
    queryset = obj.menu_buttons.order_by("-name").values("id", "name", "value")
    # MenuButtonSerializer(obj.menu_buttons.all(), many=True)
    if queryset:
      return queryset
    else:
      return None

  def get_has_children(self, obj):
    has_children = Menu.objects.filter(parent=obj.id)
    if has_children:
      return True
    return False

  class Meta:
    model = Menu
    fields = "__all__"
    read_only_fields = ["id"]


class MenuCreateUpdateSerializer(serializers.ModelSerializer):
  """
  菜单表的创建序列化器
  """
  name = serializers.CharField(required=False)

  def create(self, validated_data):
    menu_obj = Menu.objects.filter(parent_id=validated_data.get("parent", None)).order_by("-sort").first()
    last_sort = menu_obj.sort if menu_obj else 0
    validated_data["sort"] = last_sort + 1
    return super().create(validated_data)

  class Meta:
    model = Menu
    fields = "__all__"
    read_only_fields = ["id"]


class MenuWebRouterSerializer(serializers.ModelSerializer):
  """
  前端菜单路由的简单序列化器
  """
  path = serializers.CharField(source="web_path")
  title = serializers.CharField(source="name")

  class Meta:
    model = Menu
    fields = (
        "id", "parent", "name", "icon", "sort", "path",  
        "title",  "is_link", "link_url", "is_catalog", 
        "web_path", "component", "component_name", 
        "cache", "visible", "is_iframe", "is_affix", "status")
    read_only_fields = ["id"]


class MenuPermissionSerializer(serializers.ModelSerializer):
  """
  菜单的按钮权限
  """
  menu_permission = serializers.SerializerMethodField()

  def get_menu_permission(self, obj):
    is_superuser = self.request.user.is_superuser
    if is_superuser:
      queryset = MenuButton.objects.filter(menu__id=obj.id)
    else:
      menu_permission_id_list = self.request.user.role.values_list("permission", flat=True)
      queryset = MenuButton.objects.filter(
         id__in=menu_permission_id_list, 
         menu__id=obj.id)
    serializer = MenuButtonSerializer(queryset, many=True, read_only=True)
    return serializer.data

  class Meta:
    model = Menu
    fields = ["id", "parent", "name", "menuPermission"]


class MenuButtonPermissionSerializer(serializers.ModelSerializer):
  """
  菜单和按钮权限
  """
  is_check = serializers.SerializerMethodField()

  def get_is_check(self, obj):
    is_superuser = self.request.user.is_superuser
    if is_superuser:
      return True
    else:
      return MenuButton.objects.filter(
          menu__id=obj.id,
          role__id__in=self.request.user.role.values_list("id", flat=True),
      ).exists()

  class Meta:
    model = Menu
    fields = "__all__"


class RoleMenuButtonPermissionSerializer(serializers.ModelSerializer):
  """
  角色-菜单-按钮-权限 查询序列化
  """

  class Meta:
    model = RoleMenuButtonPermission
    fields = "__all__"
    read_only_fields = ["id"]

# TODO 
# 查看到这里
class RoleMenuButtonPermissionCreateUpdateSerializer(serializers.ModelSerializer):
  """
  角色-菜单-按钮-权限 创建/修改序列化
  """
  menu_button__name = serializers.CharField(source="menu_button.name", read_only=True)
  menu_button__value = serializers.CharField(source="menu_button.value", read_only=True)

  class Meta:
    model = RoleMenuButtonPermission
    fields = "__all__"
    read_only_fields = ["id"]


class RoleMenuSerializer(serializers.ModelSerializer):
  """
  角色-菜单 序列化
  """
  is_check = serializers.SerializerMethodField()

  def get_is_check(self, obj):
    params = self.request.query_params
    data = self.request.data
    return RoleMenuPermission.objects.filter(
      menu_id=obj.id,
      role_id=params.get("role_id", data.get("role_id")),
    ).exists()

  class Meta:
    model = Menu
    fields = ["id", "name", "parent", "is_catalog", "isCheck"]


class RoleMenuButtonSerializer(serializers.ModelSerializer):
  """
  角色-菜单-按钮 序列化
  """
  isCheck = serializers.SerializerMethodField()
  data_range = serializers.SerializerMethodField()
  role_menu_btn_perm_id = serializers.SerializerMethodField()
  dept = serializers.SerializerMethodField()

  def get_isCheck(self, obj):
      params = self.request.query_params
      data = self.request.data
      return RoleMenuButtonPermission.objects.filter(
          menu_button_id=obj.id,
          role_id=params.get("roleId", data.get("roleId")),
      ).exists()

  def get_data_range(self, obj):
      obj = self.get_role_menu_btn_prem(obj)
      if obj is None:
          return None
      return obj.data_range

  def get_role_menu_btn_perm_id(self, obj):
      obj = self.get_role_menu_btn_prem(obj)
      if obj is None:
          return None
      return obj.id

  def get_dept(self, obj):
      obj = self.get_role_menu_btn_prem(obj)
      if obj is None:
          return None
      return obj.dept.all().values_list("id", flat=True)

  def get_role_menu_btn_prem(self, obj):
      params = self.request.query_params
      data = self.request.data
      obj = RoleMenuButtonPermission.objects.filter(
          menu_button_id=obj.id,
          role_id=params.get("roleId", data.get("roleId")),
      ).first()
      return obj

  class Meta:
      model = MenuButton
      fields = ["id", "menu", "name", "isCheck", "data_range", "role_menu_btn_perm_id", "dept"]


class RoleMenuFieldSerializer(serializers.ModelSerializer):
  """
  角色-菜单-字段 序列化
  """
  is_query = serializers.SerializerMethodField()
  is_create = serializers.SerializerMethodField()
  is_update = serializers.SerializerMethodField()

  def get_is_query(self, obj):
      params = self.request.query_params
      queryset = obj.menu_field.filter(role=params.get("roleId")).first()
      if queryset:
          return queryset.is_query
      return False

  def get_is_create(self, obj):
      params = self.request.query_params
      queryset = obj.menu_field.filter(role=params.get("roleId")).first()
      if queryset:
          return queryset.is_create
      return False

  def get_is_update(self, obj):
      params = self.request.query_params
      queryset = obj.menu_field.filter(role=params.get("roleId")).first()
      if queryset:
          return queryset.is_update
      return False

  class Meta:
      model = MenuField
      fields = ["id", "field_name", "title", "is_query", "is_create", "is_update"]


class RoleMenuPermissionSerializer(serializers.ModelSerializer):
  """
  菜单按钮-序列化器
  """

  class Meta:
    model = RoleMenuPermission
    fields = "__all__"
    read_only_fields = ["id"]


class RoleMenuPermissionInitSerializer(serializers.ModelSerializer):
  """
  初始化菜单按钮-序列化器
  """

  class Meta:
    model = RoleMenuPermission
    fields = "__all__"
    read_only_fields = ["id"]


class RoleMenuPermissionCreateUpdateSerializer(serializers.ModelSerializer):
  """
  初始化菜单按钮-序列化器
  """

  class Meta:
    model = RoleMenuPermission
    fields = "__all__"
    read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Post
    fields = "__all__"
    read_only_fields = ["id"]
    

class DeptSerializer(serializers.ModelSerializer):
  """
  部门-序列化器
  """
  parent_name = serializers.CharField(read_only=True, source="parent.name")
  status_label = serializers.SerializerMethodField()
  has_children = serializers.SerializerMethodField()
  has_child = serializers.SerializerMethodField()
  children = serializers.SerializerMethodField(read_only = True)

  dept_user_count = serializers.SerializerMethodField()

  def get_dept_user_count(self, obj: Dept):
    return Users.objects.filter(dept=obj).count()

  def get_has_child(self, obj: Dept):
    hasChild = Dept.objects.filter(parent=obj.id)
    if hasChild:
      return True
    return False

  def get_status_label(self, obj: Dept):
    if obj.status:
      return "启用"
    return "禁用"

  def get_has_children(self, obj: Dept):
    return Dept.objects.filter(parent_id=obj.id).count()
  
  # TODO 
  # 极有可能是错的 
  # 参考字典app 的 treeSerializer 来的。
  def get_children(self, obj: Dept):
    queryset = Dept.objects.filter(parent=obj.id).filter(status=1)

    if queryset:
      serializersIns = DeptSerializer(queryset, many=True)
      return serializersIns.data
    else: 
      return None

  class Meta:
      model = Dept
      fields = "__all__"
      read_only_fields = ["id"]


class DeptImportSerializer(serializers.ModelSerializer):
  """
  部门-导入-序列化器
  """

  class Meta:
    model = Dept
    fields = "__all__"
    read_only_fields = ["id"]


class DeptCreateUpdateSerializer(serializers.ModelSerializer):
  """
  部门管理 创建/更新时的列化器
  """

  def create(self, validated_data):
    value = validated_data.get("parent", None)
    if value is None:
      validated_data["parent"] = self.request.user.dept
    dept_obj = Dept.objects.filter(parent=self.request.user.dept).order_by("-sort").first()
    last_sort = dept_obj.sort if dept_obj else 0
    validated_data["sort"] = last_sort + 1
    instance = super().create(validated_data)
    instance.dept_belong_id = instance.id
    instance.save()
    return instance

  class Meta:
    model = Dept
    fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
  """
  角色-序列化器
  """
  users = serializers.SerializerMethodField()

  @staticmethod
  def get_users(obj):
      users = obj.users_set.exclude(id=1).values("id", "name", "dept__name")
      return users

  class Meta:
      model = Role
      fields = "__all__"
      read_only_fields = ["id"]


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
  """
  角色管理 创建/更新时的列化器
  """
  menu = MenuSerializer(many=True, read_only=True)
  dept = DeptSerializer(many=True, read_only=True)
  permission = MenuButtonSerializer(many=True, read_only=True)
  key = serializers.CharField(max_length=50,
                              validators=[UniqueValidator(queryset=Role.objects.all(), message="权限字符必须唯一")])
  name = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=Role.objects.all())])

  def validate(self, attrs: dict):
      return super().validate(attrs)

  # def save(self, **kwargs):
  #     is_superuser = self.request.user.is_superuser
  #     if not is_superuser:
  #         self.validated_data.pop("admin")
  #     data = super().save(**kwargs)
  #     return data

  class Meta:
      model = Role
      fields = "__all__"
      
