#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Dictionary

# vertion one
# one table

class DictionarySerializer(serializers.ModelSerializer):
  """
  字典-序列化器
  """
  
  class Meta:
    model = Dictionary
    fields = "__all__"
    read_only_fields = ["id"]


class DictionaryCreateUpdateSerializer(serializers.ModelSerializer):

  value = serializers.CharField(max_length=250)

  # TODO
  # 这里要加入必要字段的较验，不然现在测试，什么数据都能创建成功。
  def validate_value(self, value):
    """
    在父级的字典编号验证重复性
    """
    initial_data = self.initial_data
    parent = initial_data.get('parent', None)
    if parent is None:
      unique =  Dictionary.objects.filter(value=value).exists()
      if unique:
        raise APIException("字典编号不能重复")
    return value

  class Meta:
    model = Dictionary
    fields = "__all__"


class DictionaryTreeSerializer(serializers.ModelSerializer):
  children = serializers.SerializerMethodField(read_only = True)

  def get_children(self, instance):
    queryset = Dictionary.objects.filter(parent=instance.id).filter(status=1)

    if queryset:
      serializersIns = DictionaryTreeSerializer(queryset, many=True)
      return serializersIns.data
    else: 
      return None

  class Meta:
    model = Dictionary
    fields = "__all__"
    read_only_fields = ["id"]


class DictionarySimpleTreeSerializer(serializers.ModelSerializer):
  children = serializers.SerializerMethodField(read_only = True)

  def get_children(self, instance):
    queryset = Dictionary.objects.filter(parent=instance.id).filter(status=1)

    if queryset:
      serializersIns = DictionarySimpleTreeSerializer(queryset, many=True)
      return serializersIns.data
    else: 
      return None

  class Meta:
    model = Dictionary
    fields = ["id", "label", "code", "value", "children"]
    read_only_fields = ["id"]
