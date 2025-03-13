#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import connection

def is_tenants_mode():
    """
    判断是否为租户模式
    :return:
    """
    return hasattr(connection, "tenant") and connection.tenant.schema_name