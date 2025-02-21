#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import pypinyin

from rest_framework import serializers

from rest_framework.exceptions import APIException

from .models import Region

class RegionSerializer(serializers.ModelSerializer):
  """
  地区-序列化器
  """

  child_count = serializers.SerializerMethodField(read_only=True)
  has_child = serializers.SerializerMethodField()
  parent_info = serializers.SerializerMethodField(read_only=True)

  def get_child_count(self, obj: Region):
    return Region.objects.filter(parent=obj).count()
  
  def get_has_child(self, obj: Region):
    has_child = Region.objects.filter(pcode=obj.code)
    if has_child:
      return True
    return False 
  
  def get_parent_info(self, obj: Region):
    pcode_info = Region.objects.filter(code=obj.pcode).values("name", "code")
    return pcode_info

  class Meta:
    model = Region
    fields = "__all__"
    read_only_fields = ["id"]


class RegionCreateUpdateSerializer(serializers.ModelSerializer):

  def to_internal_value(self, data):
    pinyin = "".join(["".join(i) for i in pypinyin.pinyin(data["name"], style=pypinyin.NORMAL)])
    data["level"] = 1
    data["pinyin"] = pinyin
    data["initials"] = pinyin[0].upper() if pinyin else "#"
    pcode = data["pcode"] if "pcode" in data else None
    parent = data["parent"] if "parent" in data else None
    # TODO this is wrong!!!
    if pcode:
        pcode = Region.objects.get(pk=pcode)
        data["pcode"] = pcode.code
        data["level"] = pcode.level + 1
    return super().to_internal_value(data)

  class Meta:
    model = Region
    fields = "__all__"


class RegionSimpleSerializer(serializers.ModelSerializer):

  pid = serializers.CharField(source="parent_id")

  class Meta:
    model = Region
    fields = ["id", "name", "pid", "pcode"]
    read_only_fields = ["id"]

  
  
