# Git 贡献提交规范
feat 新功能
fix 修补 bug
docs 文档
style 格式、样式(不影响代码运行的变动)
refactor 重构(即不是新增功能，也不是修改 BUG 的代码)
perf 优化相关，比如提升性能、体验
test 添加测试
build 编译相关的修改，对项目构建或者依赖的改动
ci 持续集成修改
chore 构建过程或辅助工具的变动
revert 回滚到上一个版本
workflow 工作流改进
mod 不确定分类的修改
wip 开发中
types 类型

# 1 若依Vue系统中的权限分类
根据观察，若依Vue系统中的权限分为以下几类

菜单权限：用户登录系统之后能看到哪些菜单
按钮权限：用户在一个页面上能看到哪些按钮，比如新增、删除等按钮
接口权限：用户带着认证信息请求后端接口，是否有权限访问，该接口和前端页面上的按钮一一对应
数据权限：用户有权限访问后端某个接口，但是不同的用户相同的接口相同的入参，根据权限大小不同，返回的结果应当不一样——权限大的能够看到的数据更多。

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
python manage.py startapp static_pages ./apps/v1/static_pages

## 3.3 运行
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  #rj  admin@admin.com  111111 111111
python manage.py runserver 0.0.0.0:8000

python manage.py migrate apps.region.apps.RegionConfig zero

## 3.4 重新生成
python ./devtools/del_migrations.py


## 可集成应用
pip install django-silk


# 下面这个是 原django admin 的优化版本
pip install django-simpleui

python manage.py shell_plus
%load_ext autoreload
%autoreload 2

# 导出 fixtures 数据
django-admin dumpdata dictionary  不工作
python .\manage.py dumpdata dictionary --indent 2  -o .\apps\v1\dictionary\fixtures\dictionary.json
python3 manage.py dumpdata --natural-primary --natural-foreign -o db.json

# 我的数据因为关联了用户，所以要先创建超级用户 才能导入成功 测试但导入的数据已经是乱码了
python3 .\manage.py loaddata --format=json dictionary

sys.modules.pop('apps.v1.dictionary.expose')


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
