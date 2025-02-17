#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os, re, random

# 手机号验证正则
MOBILE_PHONE_BROAD_REGEX = r'^1[3-9]\d{9}$'
MOBILE_PHONE_REGEX = r"^1[356789]\d{9}$|^147\d{8}$|^176\d{8}$"

# 中国身份证正则
CHINA_IDCARD_REGEX = r"^[1-9]\d{5}(18|19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"

# 密码规则正则
CHAR_INT_PASSWORD_REGEX = r"^[a-zA_Z0-9]{6,20}$"
