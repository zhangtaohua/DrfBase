#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.conf import settings
from django.db import models

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class Role(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="role name", name="name", verbose_name="角色名称")
  key = models.CharField(max_length=64,
                          help_text="role key", name="key", verbose_name="角色权限字符")
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="角色顺序")
  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="role status", name="status", verbose_name="角色状态")
  
  ADMIN_CHOICES = (
    (0, "否"),
    (1, "是"),
  )
  admin = models.IntegerField(choices=ADMIN_CHOICES, default=0, 
                              help_text="is_admin", name="admin", verbose_name="是否为管理员")
  
  remark = models.CharField(max_length=255, null=True, blank=True,
                            help_text="remark", name="remark", verbose_name="备注")
  
  
  DATASCOPE_CHOICES = (
    (0, "仅本人数据权限"),
    (1, "本部门数据权限"),
    (2, "本部门及以下数据权限"),
    (3, "全部数据权限"),
    (4, "自定数据权限"),
  )
  data_range = models.SmallIntegerField(choices=DATASCOPE_CHOICES, default=0,
                                        help_text="data range", name="data_range", verbose_name="数据权限范围")
  
  #自定义数据权限时，即data_range=4时会用到，可以关联多个部门
  # dept = models.ManyToManyField(to="Dept", db_constraint=False, 
  #                               help_text="数据权限-关联部门", verbose_name="数据权限-关联部门")
  
  # menu = models.ManyToManyField(to="Menu", db_constraint=False, 
  #                               help_text="关联菜单", verbose_name="关联菜单")
  # permission = models.ManyToManyField(to="MenuButton", db_constraint=False,
  #                                       help_text="关联菜单的接口按钮", verbose_name="关联菜单的接口按钮")

  user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, db_constraint=False, 
                                help_text="user relate role", verbose_name="用户关联角色")
  
  class Meta:
    db_table = "rj_rbacv1_role"
    verbose_name = "角色表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)


class Post(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="post name", name="name", verbose_name="职位名称")
  code = models.CharField(max_length=64,
                          help_text="post code", name="code", verbose_name="职位编码")
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="职位顺序")
  STATUS_CHOICES = (
    (0, "离职"),
    (1, "在职"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="post status", name="status", verbose_name="职位状态")

  user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, db_constraint=False, 
                                help_text="user relate post", verbose_name="用户关联职位")
  
  class Meta:
    db_table = "rj_rbacv1_post"
    verbose_name = "职位表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)


class Dept(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="department name", name="name", verbose_name="部门名称")
  key = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="relate key", name="key", verbose_name="关联字符")
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="显示排序")
  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="department status", name="status", verbose_name="部门状态")
  
  owner = models.CharField(max_length=150, null=True, blank=True, 
                           help_text="owner", name="owner", verbose_name="负责人")
  email = models.EmailField(max_length=150, null=True, blank=True,
                              help_text="email", name="email", verbose_name="邮箱")
  phone = models.CharField(max_length=32, null=True, blank=True,
                              help_text="phone", name="phone", verbose_name="手机号")

  parent = models.ForeignKey(
    to="Dept",
    on_delete=models.CASCADE,
    default=None,
    db_constraint=False,
    null=True,
    blank=True,
    help_text="parent department",
    verbose_name="上级部门",
  )

  user = models.ForeignKey(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    db_constraint=False, null=True, blank=True, 
    help_text="user relate dept", 
    verbose_name="用户关联部门")
  

  @classmethod
  def recursion_all_dept(cls, dept_id: int, dept_all_list=None, dept_list=None):
    """
    递归获取部门的所有下级部门
    :param dept_id: 需要获取的id
    :param dept_all_list: 所有列表
    :param dept_list: 递归list
    :return:
    """
    if not dept_all_list:
      dept_all_list = Dept.objects.values("id", "parent")
    if dept_list is None:
      dept_list = [dept_id]
    for ele in dept_all_list:
      if ele.get("parent") == dept_id:
        dept_list.append(ele.get("id"))
        cls.recursion_all_dept(ele.get("id"), dept_all_list, dept_list)
    return list(set(dept_list))

  class Meta:
    db_table = "rj_rbacv1_dept"
    verbose_name = "部门表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)


class Menu(BaseTimestampsModel):
  # parent = models.ForeignKey("self")
  parent = models.ForeignKey(
    to="Menu",
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    db_constraint=False,
    help_text="上级菜单",
    name="parent",
    verbose_name="上级菜单",
  )
  icon = models.CharField(max_length=150, null=True, blank=True,
                           help_text="菜单图标", name="icon", verbose_name="菜单图标",)
  name = models.CharField(max_length=64, 
                          help_text="菜单名称", name="name", verbose_name="菜单名称")
  sort = models.IntegerField(default=1,  null=True, blank=True, 
                             help_text="显示排序", name="sort", verbose_name="显示排序")
  ISLINK_CHOICES = [
    (0, "否"),
    (1, "是"),
  ]
  is_link = models.BooleanField(choices=ISLINK_CHOICES, default=0,
                                help_text="是否外链", name="is_link", verbose_name="是否外链")
  link_url = models.CharField(max_length=255, null=True, blank=True, 
                              help_text="链接地址", name="link_url", verbose_name="链接地址")
  
  ISCATALOG_CHOICES = [
    (0, "否"),
    (1, "是"),
  ]
  is_catalog = models.BooleanField(choices=ISCATALOG_CHOICES, default=0, 
                                   help_text="是否目录", name="is_catalog", verbose_name="是否目录")
  web_path = models.CharField(max_length=255,  null=True, blank=True, 
                              help_text="路由地址", name="web_path", verbose_name="路由地址")
  component = models.CharField(max_length=255, null=True, blank=True, 
                                help_text="组件地址", name="component", verbose_name="组件地址")
  component_name = models.CharField(max_length=150, null=True, blank=True,
                                    help_text="组件名称", name="component_name", verbose_name="组件名称")
  ISAUTOPM_CHOICES=(
    (0,"不自动创建"),
    (1,"自动创建")
  )
  
  is_autopm = models.SmallIntegerField(choices=ISAUTOPM_CHOICES, default=1,
                                      help_text="自动创建按钮权限", name="is_autopm", verbose_name="自动创建按钮权限")

  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )
  status = models.BooleanField(choices=STATUS_CHOICES, default=1, blank=True, 
                               help_text="菜单状态", name="status", verbose_name="菜单状态")
  CACHE_CHOICES = (
    (0, "禁用"),
    (1, "启用")
  )
  cache = models.BooleanField(choices=CACHE_CHOICES, default=0, blank=True, 
                              help_text="是否页面缓存", name="cache", verbose_name="是否页面缓存")
  
  VISIBLE_CHOICES=(
    (0, "不可见"),
    (1, "可见")
  )
  visible = models.BooleanField(choices=VISIBLE_CHOICES, default=1, blank=True, 
                                help_text="侧边栏中是否显示", name="visible", verbose_name="侧边栏中是否显示",)
  is_iframe = models.BooleanField(default=False, blank=True, 
                                  help_text="框架外显示", name="is_iframe", verbose_name="框架外显示")
  is_affix = models.BooleanField(default=False, blank=True, 
                                 help_text="是否固定", name="is_affix", verbose_name="是否固定")

  @classmethod
  def get_all_parent(cls, id: int, all_list=None, nodes=None):
    """
    递归获取给定ID的所有层级
    :param id: 参数ID
    :param all_list: 所有列表
    :param nodes: 递归列表
    :return: nodes
    """
    if not all_list:
      all_list = Menu.objects.values("id", "name", "parent")
    if nodes is None:
      nodes = []

    for ele in all_list:
      if ele.get("id") == id:
        parent_id = ele.get("parent")
        if parent_id is not None:
          cls.get_all_parent(parent_id, all_list, nodes)
        nodes.append(ele)
    return nodes
  
  class Meta:
    db_table = "rj_rbacv1_menu"
    verbose_name = "菜单表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)


class MenuField(BaseTimestampsModel):
  menu = models.ForeignKey(
    to="Menu", 
    on_delete=models.CASCADE, 
    db_constraint=False,
    related_name="menu_fields",
    help_text="related menu", name="menu", verbose_name="关联菜单")
  model = models.CharField(max_length=150, 
                           help_text="model", name="model", verbose_name="表名")
  field_name = models.CharField(max_length=150, 
                                help_text="field name", name="field_name", verbose_name="模型表字段名")
  title = models.CharField(max_length=150, 
                           help_text="title", name="title", verbose_name="字段显示名")
  
  class Meta:
    db_table = "rj_rbacv1_menu_field"
    verbose_name = "菜单字段表"
    verbose_name_plural = verbose_name
    ordering = ("id",)


class MenuButton(BaseTimestampsModel):
  menu = models.ForeignKey(
    to="Menu",
    on_delete=models.CASCADE,
    db_constraint=False,
    related_name="menu_buttons",
    help_text="related menu",
    name="menu",
    verbose_name="关联菜单",
  )

  name = models.CharField(max_length=150, 
                          help_text="name", name="name", verbose_name="名称")
  value = models.CharField(max_length=150, unique=True,
                           help_text="permission value", name="value", verbose_name="权限值")
  api = models.CharField(max_length=255, 
                         help_text="api address", name="api", verbose_name="接口地址")
  
  METHOD_CHOICES = (
    (0, "GET"),
    (1, "POST"),
    (2, "PUT"),
    (3, "DELETE"),
  )
  method = models.IntegerField(default=0, null=True, blank=True,
                                help_text="api method", name="method", verbose_name="接口请求方法")

  class Meta:
    db_table = "rj_rbacv1_menu_button"
    verbose_name = "菜单权限表"
    verbose_name_plural = verbose_name
    ordering = ("-name",)


class RoleMenuPermission(BaseTimestampsModel):
  role = models.ForeignKey(
    to="Role",
    db_constraint=False,
    related_name="role_menu",
    on_delete=models.CASCADE,
    help_text="关联角色",
    name="role",
    verbose_name="关联角色",
  )
  menu = models.ForeignKey(
    to="Menu",
    db_constraint=False,
    related_name="role_menu",
    on_delete=models.CASCADE,
    help_text="关联菜单",
    name="menu",
    verbose_name="关联菜单",
  )

  class Meta:
      db_table = "rj_role_menu_permission"
      verbose_name = "角色菜单权限表"
      verbose_name_plural = verbose_name
      # ordering = ("-create_datetime",)

class RoleMenuFieldPermission(BaseTimestampsModel):
  role = models.ForeignKey(to="Role", on_delete=models.CASCADE, db_constraint=False,
                           help_text="role", name="role", verbose_name="角色",)
  field = models.ForeignKey(to="MenuField", on_delete=models.CASCADE,related_name="menu_field", db_constraint=False,
                            help_text="field", name="field", verbose_name="字段",)
  is_query = models.BooleanField(default=1, 
                                 help_text="is query", name="is_query", verbose_name="是否可查询")
  is_create = models.BooleanField(default=1, 
                                  help_text="is create", name="is_create", verbose_name="是否可创建")
  is_update = models.BooleanField(default=1, 
                                  help_text="is update", name="is_update", verbose_name="是否可更新")

  class Meta:
    db_table =  "rj_rbacv1_role_menu_field_permission"
    verbose_name = "字段权限表"
    verbose_name_plural = verbose_name
    ordering = ("id",)

class RoleMenuButtonPermission(BaseTimestampsModel):
  role = models.ForeignKey(
    to="Role",
    db_constraint=False,
    related_name="role_menu_button",
    on_delete=models.CASCADE,
    help_text="关联角色",
    name="role",
    verbose_name="关联角色",
  )
  menu_button = models.ForeignKey(
    to="MenuButton",
    null=True,
    blank=True,
    db_constraint=False,
    related_name="menu_button_permission",
    on_delete=models.CASCADE,
    help_text="关联菜单按钮",
    name="menu_button",
    verbose_name="关联菜单按钮",
  )

  class Meta:
    db_table = "rj_rbacv1_role_menu_button_permission"
    verbose_name = "角色按钮权限表"
    verbose_name_plural = verbose_name
    ordering = ("-create_datetime",)






