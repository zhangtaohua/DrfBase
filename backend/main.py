#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os
import sys
import multiprocessing

import uvicorn
from django.conf import settings

root_path = os.getcwd()
sys.path.append(root_path)


if __name__ == "__main__":
  multiprocessing.freeze_support()
  workers = 4
  if os.sys.platform.startswith('win'):
    # Windows操作系统
    workers = None
  uvicorn.run("application.asgi:application", reload=False, host="0.0.0.0", port=8000, workers=workers,
              log_config=settings.LOGGING)