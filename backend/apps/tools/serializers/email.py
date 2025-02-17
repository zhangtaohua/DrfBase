#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re
from rest_framework import serializers

from comutils.common.regex import MOBILE_PHONE_REGEX
from apps.users.models import Users

class EmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=150, min_length=3, required=True, help_text="手机号") 
  smstype = serializers.CharField(max_length=10, required=True, help_text="短信类型")

  def validate_email(self, email):
    return email
