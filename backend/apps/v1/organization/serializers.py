#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from .models import Company, Post, Dept

Users = settings.AUTH_USER_MODEL

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
      
