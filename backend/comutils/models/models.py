#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import uuid

from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

def make_uuid(has_hyphen = False):
  uuid_ins = uuid.uuid4()
  if has_hyphen:
    return str(uuid_ins)
  else:
    return str(uuid_ins.hex)


class BaseTimestampsModel(models.Model):
  create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, 
                                   help_text="crate time", name="create_time", verbose_name="创建时间")
  update_time = models.DateTimeField(auto_now=True, null=True, blank=True, 
                                   help_text="update time", name="update_time", verbose_name="更新时间")
  delete_time = models.DateTimeField(null=True, blank=True, 
                                   help_text="delete time", name="delete_time", verbose_name="删除时间")

  class Meta:
    abstract = True
    # name = "basic time model"
    verbose_name = "基础时间模型"
    verbose_name_plural = verbose_name
  
  def __str__(self):
      return self.__name__


class BaseUuidModel(BaseTimestampsModel): 
  uuid = models.CharField(max_length=100, default=make_uuid, 
                          help_text="UUID", name="uuid", verbose_name="UUID")
  
  class Meta:
    abstract = True
    # name = "base UUID model"
    verbose_name = "基础UUID模型"
    verbose_name_plural = verbose_name

  def __str__(self):
    return set.__name__


class BaseTitleModel(BaseUuidModel):
  title = models.CharField(max_length=250, null=True, blank=True, 
                                 help_text="title", name="title", verbose_name="标题")
  # slug = models.SlugField(max_length=250, blank=True, null=True, 
  #                         help_text="slug", name="slug", verbose_name="slug")
  slug = AutoSlugField(populate_from='title')

  description = models.CharField(max_length=250, null=True, blank=True, 
                                 help_text="description", name="description", verbose_name="描述")
  creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="creator_query", null=True, on_delete=models.SET_NULL,
                              help_text="creator", name="creator", verbose_name="创建人")
  modifier = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="modifier_query", null=True, on_delete=models.SET_NULL,
                              help_text="modifier", name="modifier", verbose_name="修改人")  
  
  def slugify_function(self, content):
    return content.replace('_', '-').lower()

  class Meta:
    abstract = True
    # name = "base title model"
    verbose_name = "基础标题模型"
    verbose_name_plural = verbose_name

  def __str__(self):
    return set.__name__ 
  

