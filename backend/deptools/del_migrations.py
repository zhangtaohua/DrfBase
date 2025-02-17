#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os
from pathlib import Path
import django
from django.apps import apps
import sys
import shutil

FILE_PATH = os.path.abspath(__file__)
FILE_DIR_PATH = os.path.dirname(FILE_PATH)
FILE_PARENT_PATH = os.path.dirname(FILE_DIR_PATH)
APPS_BASE_DIR = os.path.join(FILE_PARENT_PATH, "apps")

sys.path.insert(0, FILE_PARENT_PATH)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings.development')
# django.setup()


def del_migrations():
  print(f"删除迁移文件生成中……")
  # all_apps = apps.get_app_configs()
  # for app in all_apps:
  #   print("APP_name:", app.name)
  #   print("\r\n")
  #   if app.name.startswith("django"):
  #     continue
  #   if app.name.startswith("apps"):
  #      print(f"删除 {app.name} 的迁移文件")
  #      continue


  app_dirs = os.listdir(APPS_BASE_DIR)
  for dir in app_dirs:
     print(f"删除知{dir} 的迁移文件")
     app_migrations_dir = os.path.join(APPS_BASE_DIR, dir, "migrations")

     migrations = os.listdir(app_migrations_dir)
     for migration in migrations:
        file_path = os.path.join(app_migrations_dir, migration)
        if migration.startswith("000") and migration.endswith(".py"):
          os.remove(file_path)
          print(f"删除文件：{migration}")

        if migration == "__pycache__":
          shutil.rmtree(file_path)
          print(f"删除文件夹：{migration}")

  print(f"删除迁移文件完成！")

def del_sqlit3():
  sql_path = os.path.join(FILE_PARENT_PATH, "db.sqlite3")
  if os.path.exists(sql_path):
     os.remove(sql_path)

if __name__ == '__main__':
    del_migrations()
    del_sqlit3()