#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: request 工具函数
"""

import json
from rest_framework.request import Request
from django.http import QueryDict


# 获取 get 或 post的参数
# 使用方法：
# 方法一：get_parameter_dic(request)["name"], name为获取的参数名, 此种方式获取name不存在则会报错返回name表示name不存在，需要此参数
# 方法二：get_parameter_dic(request).get("name"), name为获取的参数名,   此种方式获取name不存在不会报错，不存在会返回None
def get_parameter_dic(request, *args, **kwargs):
  if isinstance(request, Request) == False:
    return {}

  query_params = request.query_params
  if isinstance(query_params, QueryDict):
      query_params = query_params.dict()
  result_data = request.data
  if isinstance(result_data, QueryDict):
      result_data = result_data.dict()

  if query_params != {}:
      return query_params
  else:
      return result_data

def get_request_ip(request):
  """
  获取请求的 IP 地址
  """
  if "HTTP_X_FORWARDED_FOR" in request.META:
      ip = request.META["HTTP_X_FORWARDED_FOR"]
      if ip: 
        ip = ip.split(",")[-1].strip()
  else:
      ip = request.META['REMOTE_ADDR'] or getattr(request, "request_ip", "")
  return ip

  # methond one
  # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
  # if x_forwarded_for:
  #     ip = x_forwarded_for.split(',')[-1].strip()
  #     return ip
  # ip = request.META.get('REMOTE_ADDR', '') or getattr(request, 'request_ip', None)
  # return ip or 'unknown'

  # methond two
  # ip = getattr(request, 'request_ip', None)
  # if ip:
  #     return ip
  # ip = request.META.get('REMOTE_ADDR', '')
  # if not ip:
  #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
  #     if x_forwarded_for:
  #         ip = x_forwarded_for.split(',')[-1].strip()
  #     else:
  #         ip = 'unknown'
  # return ip