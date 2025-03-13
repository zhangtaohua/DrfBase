#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os, sys

import django

from faker import Faker

FILE_PATH = os.path.abspath(__file__)
FILE_DIR_PATH = os.path.dirname(FILE_PATH) # dbinit
APP_DIR_PATH = os.path.dirname(FILE_DIR_PATH) # dictionay
APPS_BASE_DIR = os.path.dirname(os.path.dirname(APP_DIR_PATH))
PROJ_PARENT_PATH = os.path.dirname(APPS_BASE_DIR)

sys.path.insert(0, PROJ_PARENT_PATH)

print("sys path", sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.development')
django.setup()

from apps.v1.dictionary.models import Dictionary
from apps.v1.users.models import Users

user = Users.objects.get(pk=1)

def generate_data():
  fake = Faker('zh_CN')
  print(f"字典数据生成中……")

  parent = Dictionary.objects.create(
    label="名称", code="name", description="用于标示名称", 
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=1,
    creator=user, modifier=user,
  )
  parent.save()

  parent = Dictionary.objects.create(
    label="代码", code="code", description="用于标示代码", 
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=2,
    creator=user, modifier=user,
  )
  parent.save()

  parent1 = Dictionary.objects.create(
    label="一级", code="first_level", description="一级", 
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=3,
    creator=user, modifier=user,
  )
  parent1.save()

  parent11 = Dictionary.objects.create(
    label="一级_一级", code="first_first_level", description="一级_一级", 
    parent=parent1,
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=1,
    creator=user, modifier=user,
  )
  parent11.save()

  parent12 = Dictionary.objects.create(
    label="一级_二级", code="first_sec_level", description="一级_二级", 
    parent=parent1,
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=2,
    creator=user, modifier=user,
  )
  parent12.save()

  parent13 = Dictionary.objects.create(
    label="一级_三级", code="first_third_level", description="一级_三级", 
    parent=parent1,
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=3,
    creator=user, modifier=user,
  )
  parent13.save()

  parent111 = Dictionary.objects.create(
    label="一级_一级_一级", code="first_first_first_level", value="first_first_first_level", description="一级_一级_一级",
    parent=parent11,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[1][0],
    sort=1,
    creator=user, modifier=user,
  )
  parent111.save()

  parent112 = Dictionary.objects.create(
    label="一级_一级_二级", code="first_first_sec_level", value="first_first_sec_level", description="一级_一级_二级",
    parent=parent11,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[1][0],
    sort=2,
    creator=user, modifier=user,
  )
  parent112.save()

  parent121 = Dictionary.objects.create(
    label="一级_二级_一级", code="first_sec_first_level", value="first_sec_first_level", description="一级_二级_一级",
    parent=parent12,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[1][0],
    sort=1,
    creator=user, modifier=user,
  )
  parent121.save()

  parent = Dictionary.objects.create(
    label="性别", code="gender", description="性别", 
    is_value=Dictionary.IS_VALUE_CHOICES[0][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[0][0],
    sort=4,
    creator=user, modifier=user,
  )
  parent.save()

  child = Dictionary.objects.create(
    label="未知", code="gender.unknown", value=0, description="性别.未知",
    parent=parent,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[2][0],
    sort=1,
    creator=user, modifier=user,
  )
  child.save()

  child = Dictionary.objects.create(
    label="男", code="gender.male", value=1, description="性别.男",
    parent=parent,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[2][0],
    sort=2,
    creator=user, modifier=user,
  )
  child.save()

  child = Dictionary.objects.create(
    label="女", code="gender.female", value=2, description="性别.女",
    parent=parent,
    is_value=Dictionary.IS_VALUE_CHOICES[1][0],
    value_type=Dictionary.VALUE_TYPE_CHOICES[2][0],
    sort=3,
    creator=user, modifier=user,
  )
  child.save()

  print(f"字典数据生成完成")

if __name__ == '__main__':
    generate_data()