#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re 

from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as django_ValidationError

from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError

from comutils.common import regex
from comutils.response.json_response import DeleteResponse, DataResponse, CreatedResponse

def validate_email(email=None):
  try:
    django_validate_email(email)
  except django_ValidationError:
    raise ValidationError(django_ValidationError.message, django_ValidationError.code)

    
class EmailValMixin:
  def validate_email(self, value):
    validate_email(value)


def validate_phone(phone=None):
  if not phone:
    raise ValidationError("手机号不能为空")
  else:
    if not re.match(regex.MOBILE_PHONE_REGEX, phone):
      raise ValidationError("请输入正确手机号")

class PhoneValMixin:
  def validate_phone(self, value):
    validate_phone(value)
