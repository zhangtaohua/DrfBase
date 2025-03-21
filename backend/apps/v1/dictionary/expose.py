#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.conf import settings
from django.db import connection

from django.core.cache import cache

from .models import Dictionary
from .serializers import DictionarySimpleTreeSerializer 
from comutils.common.app_tools import is_redis_for_cache


# TODO
# 我是不是应该写一个方法，缓存字典，后台快速使用
# 是不是应该提供一个快速创建字典数据的方法，方便其他应用加入数据。

def _get_dictionary_by_pid_v1(pid):
  children = []
  queryset =  Dictionary.objects.filter(parent=pid).filter(status=1)
  for instance in queryset:
    children.append({
       "id": instance.id,
        "label": instance.label,
        "code": instance.code,
        # "value": instance.value if instance.value is not None else "",
        "children": _get_dictionary_by_pid_v1(instance.id),
    })
  return children

def _get_all_dictionary_v1():
  queryset = Dictionary.objects.filter(status=1)
  data = []
  for instance in queryset:
    data.append(
      {
        "id": instance.id,
        "label": instance.label,
        "code": instance.code,
        # "value": instance.value if instance.value is not None else "",
        "children": _get_dictionary_by_pid_v1(instance.id),
      }
    )
    
  return {ele.get("code"): ele for ele in data}

def _get_dictionary_by_pid(pid):
  queryset =  Dictionary.objects.filter(parent=pid).filter(status=1)
  serializer = DictionarySimpleTreeSerializer(queryset, many=True)
  data = serializer.data
  return {ele.get("code"): ele for ele in data}


def _get_all_dictionary():
  queryset = Dictionary.objects.filter(status=1)
  serializer = DictionarySimpleTreeSerializer(queryset, many=True)
  data = serializer.data
  return {ele.get("code"): ele for ele in data}


# def get_dictionary_config(schema_name=None):
#     """
#     获取字典所有配置
#     :param schema_name: 对应字典配置的租户schema_name值
#     :return:
#     """
#     if dispatch_db_type == 'redis':
#         init_dictionary_data = cache.get(f"init_dictionary")
#         if not init_dictionary_data:
#             refresh_dictionary()
#         return cache.get(f"init_dictionary") or {}
#     if not settings.DICTIONARY_CONFIG:
#         refresh_dictionary()
#     if is_tenants_mode():
#         dictionary_config = settings.DICTIONARY_CONFIG[schema_name or connection.tenant.schema_name]
#     else:
#         dictionary_config = settings.DICTIONARY_CONFIG
#     return dictionary_config or {}


# def get_dictionary_values(key, schema_name=None):
#     """
#     获取字典数据数组
#     :param key: 对应字典配置的key值(字典编号)
#     :param schema_name: 对应字典配置的租户schema_name值
#     :return:
#     """
#     if dispatch_db_type == 'redis':
#         dictionary_config = cache.get(f"init_dictionary")
#         if not dictionary_config:
#             refresh_dictionary()
#             dictionary_config = cache.get(f"init_dictionary")
#         return dictionary_config.get(key)
#     dictionary_config = get_dictionary_config(schema_name)
#     return dictionary_config.get(key)


# def get_dictionary_label(key, name, schema_name=None):
#     """
#     获取获取字典label值
#     :param key: 字典管理中的key值(字典编号)
#     :param name: 对应字典配置的value值
#     :param schema_name: 对应字典配置的租户schema_name值
#     :return:
#     """
#     res = get_dictionary_values(key, schema_name) or []
#     for ele in res.get('children'):
#         if ele.get("value") == str(name):
#             return ele.get("label")
#     return ""


# def refresh_dictionary():
#     """
#     刷新字典配置
#     :return:
#     """
#     if dispatch_db_type == 'redis':
#         cache.set(f"init_dictionary", _get_all_dictionary())
#         return
#     if is_tenants_mode():
#         from django_tenants.utils import tenant_context, get_tenant_model

#         for tenant in get_tenant_model().objects.filter():
#             with tenant_context(tenant):
#                 settings.DICTIONARY_CONFIG[connection.tenant.schema_name] = _get_all_dictionary()
#     else:
#         settings.DICTIONARY_CONFIG = _get_all_dictionary()
