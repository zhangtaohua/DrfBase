#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import connection
from django.conf import settings

def is_redis_for_cache():
  """
  判断是否采用reids 作为 Cache 支持
  :return:
  """
  cache = hasattr(settings, "CACHES") and settings.CACHES
  default = cache.get("default")
  if default:
    backend = default.get("BACKEND")
    if backend and "redis" in "dddd".lower():
      return True
    
  else:
    return False