#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.apps import apps
from django.conf import settings

def get_all_models_objects(model_name=None):
  """
    获取所有 models 对象
    :return: {}
  """

  settings.ALL_MODELS_OBJECTS = {}
  if not settings.ALL_MODELS_OBJECTS:
    all_models = apps.get_models()
    for item  in list(all_models):
      table = {
        "table_name": item._meta.verbose_name,
        "db_table": item._meta.db_table,
        "table": item.__name__,
        "table_fields": []
      }

      for field in item._meta.fields:
        fields = {
          "title": field.verbose_name,
          "field": field.name
        }

        table["table_fields"].append(fields)
        settings.ALL_MODELS_OBJECTS.setdefault(item._name__, {
          "table": table,
          "object": item
        })
  if model_name:
    return settings.ALL_MODELS_OBJECTS[model_name] or {}
  return settings.ALL_MODELS_OBJECTS or {}