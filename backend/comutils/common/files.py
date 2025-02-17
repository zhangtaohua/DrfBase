#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os, re, random, time


"""
上传图片名自定义

参数为图片文件名
"""
def renameImageName(srcimg):
  # 文件扩展名
  ext = os.path.splitext(srcimg)[1]
  # File names longer than 255 characters can cause problems on older OSes.
  if len(srcimg) > 255:
      ext = ext[:255]
  # 定义文件名，年月日时分秒随机数
  fn = time.strftime('%Y%m%d%H%M%S')
  fn = fn + '_%d' % random.randint(100, 999)
  # 重写合成文件名
  name =  fn + ext
  return name