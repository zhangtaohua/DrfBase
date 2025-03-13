# 第一章 环境说明

## 1、python 版本控制
可以使用[pyevn](https://github.com/pyenv/pyenv)进行版本管理。

基本使用参考：
```shell
# 查看帮助
pyenv --help

# 查看网络上支持的版本
pyenv install -l
pyenv install --list

# 过滤查看网络上支持的版本 
pyenv install -l | findstr 3.8

# 查看你当前使用版本和其路径
pyenv version

# 查看你当前系统中安装的所有版本
pyenv versions

# 安装版本
pyenv install 3.12.7
pyenv install -v 3.12.7
pyenv install  3.12.7  3.12.8

# 卸载版本
pyenv uninstall 3.12.7

# 更新系统中已安装的python版本
pyenv update

# 使用`pip`安装或者卸载依赖库，或者修改了版本文件夹，请用以下命令更新
pyenv rehash

# 设置全局版本
pyenv global 3.12.7

# 设置本地(本文件夹)版本
pyenv local 3.12.7

# 设置shell 环境版本
pyenv shell 3.12.7

# 取消版本设置
pyenv global --unset
pyenv local --unset
pyenv shell --unset

# 优先级
shell > local > global

```

# python 虚拟环境
建议使用虚拟环境，网络中各种方案，请自行选择。
我采用`python3`官方的`python3 -m venv` 创建。

基本使用参考：

```shell
# 创建环境
python3 -m venv /Users/rj/work/env/python3/drf313

# 激活环境
# linux/mac
source /Users/rj/work/env/python3/drf313/bin/activate
# windows 
E:\env\python\drfbase\Scripts\activate

# 退出虚拟环境: 进入虚拟环境bin或者Scripts 目录
deactivate

```

# python 文件开头

```
#!/usr/bin/env python
#!/usr/bin/python

#!/usr/bin/env phthon3
#!/usr/bin/python3

# coding=utf-8
# -*- coding: utf-8 -*-

```

# node 环境
node 版本
npm 版本
pnpm 版本
yarn 版本


# 整体目录结构






