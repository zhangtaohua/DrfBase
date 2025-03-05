#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Address

class AddressSerializer(serializers.ModelSerializer):

  class Meta:
    model = Address
    fields = "__all__"
    read_only_fields = ["id"]

  # 有外键的新增数据时，需要自定义create函数，来处理外键相关数据
  def create(self, validated_data):
    return Address.objects.create(user=self.context["user"], **validated_data)
  

class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """

    class Meta:
        model = Address
        fields = ('title',)
  
  
