#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import models
from django.conf import settings

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class Dictionary(BaseTimestampsModel):

  VALUE_TYPE_CHOICES = (
    (0, ""),
    (1, "text"),
    (2, "number"),
    (3, "date"),
    (4, "datetime"),
    (5, "time"),
    (6, "files"),
    (7, "boolean"),
    (8, "images"),
  )

  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )

  IS_VALUE_CHOICES = (
    (0, "否"),
    (1, "是"),
  )

  # 如 性别，真假，是否
  # 如 男，女，未知； 真，假； 是，否；
  label = models.CharField(max_length=150, null=True, blank=True,
                            help_text="label", name="label", verbose_name="名称/标识")
  code = models.CharField(max_length=150, null=True, blank=True, unique=True,
                            help_text="code", name="code", verbose_name="代号")
  value = models.CharField(max_length=255, null=True, blank=True,
                            help_text="value", name="value", verbose_name="实际值")
  description = models.CharField(max_length=255, null=True, blank=True, 
                                help_text="description", name="description", verbose_name="描述")
  
  parent = models.ForeignKey(
    # to="Dictionary",
    to="self",
    related_name="sublist",
    db_constraint=False,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    help_text="parent",
    name="parent",
    verbose_name="父级",
  )
  
  is_value = models.SmallIntegerField(choices=IS_VALUE_CHOICES, default=0, 
                                help_text="is value", name="is_value", verbose_name="是否为value值")
  
  value_type = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=0, 
                                    help_text="value type", name="value_type", verbose_name="数值类型")
  
  color = models.CharField(max_length=150, null=True, blank=True, 
                            help_text="show color", name="color", verbose_name="颜色")

  status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[1][0],
                              help_text="status", name="status", verbose_name="状态")
  
  sort = models.IntegerField(default=1, null=True, blank=True,
                            help_text="sort", name="sort", verbose_name="显示排序")
  
  remark = models.CharField(max_length=255, blank=True, null=True, 
                            help_text="remark", name="remark", verbose_name="备注")

  creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="creator_query", 
                              related_name="creator", null=True, on_delete=models.SET_NULL,
                              help_text="creator", name="creator", verbose_name="创建人")
  modifier = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="modifier_query",
                              related_name="modifier", null=True, on_delete=models.SET_NULL,
                              help_text="modifier", name="modifier", verbose_name="修改人")  
  

  def __str__(self):
    return self.label

  class Meta:
    db_table = "rj_dictionary"
    verbose_name = "字典表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)

  # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
  #     super().save(force_insert, force_update, using, update_fields)
  #     dispatch.refresh_dictionary()  # 有更新则刷新字典配置

  # def delete(self, using=None, keep_parents=False):
  #     res = super().delete(using, keep_parents)
  #     # dispatch.refresh_dictionary()
  #     return res
  
