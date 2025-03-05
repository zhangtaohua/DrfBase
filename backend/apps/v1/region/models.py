#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from django.db import models

# Create your models here.

# 城乡分类 
# (1开头是城镇，2开头是乡村)
# 111表示主城区；
# 112表示城乡接合区；
# 121表示镇中心区；
# 122表示镇乡接合区；
# 123表示特殊区域；
# 210表示乡中心区；
# 220表示村庄

# 级别
# 1级：省、直辖市、自治区
# 2级：地级市
# 3级：市辖区、县（旗）、县级市、自治县（自治旗）、特区、林区
# 4级：镇、乡、民族乡、县辖区、街道
# 5级：村、居委会

class Region(models.Model):

  pcode = models.CharField(max_length=64, null=True, blank=True,
                          help_text="parent code", name="pcode", verbose_name="父级城市编码")
  code = models.CharField(max_length=64, db_index=True, null=True, blank=True,
                          help_text="code", name="code", verbose_name="城市编码")
  name = models.CharField(max_length=150, 
                          help_text="name", name="name", verbose_name="名称")
  pinyin = models.CharField(max_length=255, null=True, blank=True,
                             help_text="pinyin", name="pinyin", verbose_name="拼音")
  initials = models.CharField(max_length=20, null=True, blank=True,
                              help_text="initials", name="initials", verbose_name="首字母")
  
  level = models.PositiveIntegerField(default=0,
                          help_text="level", name="level", verbose_name="级别")
  category = models.PositiveIntegerField(default=0,
                          help_text="category", name="category", verbose_name="城乡分类")
  
  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )
  status = models.SmallIntegerField(default=1,
                              help_text="status", name="status", verbose_name="状态")

  # 外键链接自己
  parent = models.ForeignKey(
    to="self", 
    null=True, 
    blank=True, 
    on_delete=models.SET_NULL, 
    related_name='subs', 
    db_constraint=False, 
    help_text="parent", name="parent", verbose_name='上级行政区')

  # related_name='subs' ，意思为如果想找自己的子级，就可以通过region.subs找到自己下级所有的region区域,
  # 我们也可以这样调用获取市: region.region_set.all() ==> region.subs.all()
  # on_delete=models.SET_NULL: 如果省删掉了,省内其他的信息为 NULL

  class Meta:
    db_table = "rj_region"
    verbose_name = "中国省市区"
    verbose_name_plural = verbose_name

  def __str__(self):
    return self.name
  