#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


# 官方建议 CHOICES 直接写在模型类中，这里这么写，有两个原因，
# 一是想尝试一下，二是也是想从 数据库 字典数据表 中生成相应的 CHOICES
# 虽然感觉 Model 中会有很多重复代码，但个人也不建议这么用

from django.db import models

class EnDisNumberStatusChoices(models.IntegerChoices):
  DISABLED = 0, "禁用"
  ENABLED = 1, "启用"

  __empty__= "禁用"
  # __empty__ = _("(Unknown)")


class EnDisTFStatusChoices(models.Choices):
  DISABLED = False, "禁用"
  ENABLED = True, "启用"

  __empty__= "禁用"
    

EnDisNumberTupleStatusChoices  = (
    (0, "禁用"),
    (1, "启用"),
  )


EnDisNumberDictStatusChoices = {
    0: "禁用",
    1: "启用",
  }


# 以下四个类都是没有办法Mixin的，我的理解有误
# 不要使用呀，等再学学再来看看
class EnDisNumberStatusChoicesMixin(models.Model):
  class STATUS_CHOICES(models.IntegerChoices):
    DISABLED = 0, "禁用"
    ENABLED = 1, "启用"

    __empty__= "禁用"
    # __empty__ = _("(Unknown)")

  class Meta:
    abstract = True


class EnDisTFStatusChoicesMixin(models.Choices):
  DISABLED = False, "禁用"
  ENABLED = True, "启用"

  __empty__= "禁用"
    

class EnDisNumberTupleStatusChoicesMixin(models.Model):
  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )

  class Meta:
    abstract = True

class EnDisNumberDictStatusChoicesMixin:
  STATUS_CHOICES = {
    0: "禁用",
    1: "启用",
  }


