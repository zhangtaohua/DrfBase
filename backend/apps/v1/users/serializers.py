#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.v1.users.models import Users

class UserSerializer(ModelSerializer):

  # gender = SerializerMethodField()
  gender_name = SerializerMethodField()
  user_type_name = SerializerMethodField()

  class Meta:
    model = Users
    # fields = "__all__"
    # read_only_fields = ("id", "create_time", "update_time", "delete_time")
    exclude = ("password", "phone", "tel",)

  # def get_gender(self, obj):
  #   return obj.get_gender_display() 
  
  def get_gender_name(self, obj):
    return obj.get_gender_display()
  
  def get_user_type_name(self, obj):
    return obj.get_user_type_display()

