#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os, sys
import pypinyin

import django

import csv

FILE_PATH = os.path.abspath(__file__)
FILE_DIR_PATH = os.path.dirname(FILE_PATH) # dbinit
APPS_BASE_DIR = os.path.dirname(os.path.dirname(FILE_DIR_PATH))
PROJ_PARENT_PATH = os.path.dirname(APPS_BASE_DIR)

sys.path.insert(0, PROJ_PARENT_PATH)

print("sys path", sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.development')
django.setup()

from apps.region.models import Region
from apps.users.models import Users

user = Users.objects.get(pk=1)

def generate_data():
  # code,name,level,pcode,category
  # level: 省1，市2，县3，镇4，村5
  # code: 12位，省2位，市2位，县2位，镇3位，村3位
  # pcode: 直接父级别的code
  # category: 城乡分类
  # length: 665552
  with open(os.path.join(FILE_DIR_PATH, "area_code_2024.csv"), encoding="utf-8") as csv_obj:
    reader_obj = csv.reader(csv_obj)
    length = 0
    print(f"开始导入")
    for row in reader_obj:
      pinyin = "".join(["".join(i) for i in pypinyin.pinyin(row[1], style=pypinyin.NORMAL)])
      initials = pinyin[0].upper() if pinyin else "#"
      parent= Region.objects.filter(code=row[3]).first()
      region = Region.objects.create(
        pcode=row[3], code=row[0], name=row[1],
        pinyin=pinyin, initials=initials,
        level=int(row[2]), category=int(row[4]),
        status=1,
      )
      if parent:
        region.parent = parent
      region.save()
      length = length + 1
    
    print(f"导入完成{length}")


def generate_json_data():
  pass

def get_data_number():
  # print("数据项长度：", Region.objects.count())
  queryset = Region.objects.filter(parent=None)

  print("数据项长度：", queryset.count())
  for q in queryset:
    print(f"名称： {q.name} - {q.code} - {q.id}")

  dongguang = Region.objects.filter(name = "东莞市").first()
  print(f"名称： {dongguang.name} - {dongguang.code} - {dongguang.id}")

  
if __name__ == '__main__':
  # generate_data()
  get_data_number()