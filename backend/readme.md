# 1、环境说明
## 1.1 pyevn 版本控制
```
pyenv 切换版本：
pyenv --help
pyenv install --list 查看当前支持那些版本。
pyevn install -v 3.12.8
pyenv versions 可进当前安装版本
pyenv local 3.12.8
pyenv local --unset
pyenv shell
pyenv global
shell > local > global
pyenv uninstall 3.12.8

#!/usr/bin/env python
#!/usr/bin/python

#!/usr/bin/env phthon3
#!/usr/bin/python3

# coding=utf-8
# -*- coding: utf-8 -*-

```

## 1.2 虚拟环境
python 版本为 3.13.1
python3 -m venv /Users/rj/work/env/python3/drf313
source /Users/rj/work/env/python3/drf313/bin/activate
pip3 install Django
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support

## 1.3 创建工程
cd /Users/rj/work/supermind/python/application
django-admin startproject application ./

按官方教程将'rest_framework' 加入 settings 中。 

# 2、功能记录



# 3、开发记录

## 3.1 版本如何控制？


## 3.2 个人用户系统
mkdir apps
cd apps
mkdir users
python manage.py startapp users ./apps/users

## 3.3 运行
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  #rj  admin@admin.com  111111 111111
python manage.py runserver 0.0.0.0:8000

python manage.py migrate apps.region.apps.RegionConfig zero

## 3.4 重新生成
python ./deptools/del_migrations.py


## 可集成应用
pip install django-silk


# 下面这个是 原django admin 的优化版本
pip install django-simpleui

# 注释风格
5.1 reST风格

这是现在流行的一种风格，reST风格，Sphinx的御用格式，比较紧凑。

"""
This is a reST style.
 
:param param1: this is a first param
:param param2: this is a second param
:returns: this is a description of what is returned
:raises keyError: raises an exception
"""


5.2 Google风格

"""
This is a groups style docs.
 
Parameters:
 param1 - this is the first param
 param2 - this is a second param
 
Returns:
 This is a description of what is returned
 
Raises:
 KeyError - raises an exception
"""
