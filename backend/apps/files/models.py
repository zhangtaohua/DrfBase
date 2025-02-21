#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import os
from pathlib import PurePosixPath
from time import time
import hashlib

from django.db import models
from django.conf import settings

from comutils.models.models import BaseTimestampsModel

def media_file_name_downloadcenter(instance: "FilesDownload", filename):
  h = instance.md5sum
  basename, ext = os.path.splitext(filename)
  return PurePosixPath("files", "dlct", h[:1], h[1:2], basename + "-"+ str(time()).replace(".", "") + ext.lower())

# Create your models here.
class FilesDownload(BaseTimestampsModel):
  TASK_STATUS_CHOICES = [
    (0, "任务已创建"),
    (1, "任务进行中"),
    (2, "任务完成"),
    (3, "任务失败"),
  ]

  task = models.CharField(max_length=255, 
                          help_text="task name", name="task", verbose_name="任务名称")
  
  status = models.SmallIntegerField(choices=TASK_STATUS_CHOICES, default=0, 
                                    help_text="status", name="status", verbose_name="任务状态")
  
  file_name = models.CharField(max_length=255, null=True, blank=True, 
                               help_text="file name", name="file_name", verbose_name="文件名")
  
  url = models.FileField(upload_to=media_file_name_downloadcenter, null=True, blank=True,
                         help_text="url", name="url", verbose_name="下载地址")

  size = models.BigIntegerField(default=0,
                                help_text="file size", name="size", verbose_name="文件大小")

  md5sum = models.CharField(max_length=36, null=True, blank=True, 
                            help_text="md5sum", name="md5sum", verbose_name="文件md5")

  creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="creator_query", null=True, on_delete=models.SET_NULL,
                              help_text="creator", name="creator", verbose_name="创建人")
  
  modifier = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name="modifier_query", null=True, on_delete=models.SET_NULL,
                              help_text="modifier", name="modifier", verbose_name="修改人")  
  

  def save(self, *args, **kwargs):
    if self.url:
      if not self.md5sum:  # file is new
        md5 = hashlib.md5()
        for chunk in self.url.chunks():
          md5.update(chunk)
        self.md5sum = md5.hexdigest()
      if not self.size:
          self.size = self.url.size
    super(FilesDownload, self).save(*args, **kwargs)

  class Meta:
    db_table = "rj_files_download"
    verbose_name = "文件下载中心"
    verbose_name_plural = verbose_name
    ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[:1], h[1:2], h + ext.lower())

class FileList(BaseTimestampsModel):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name, null=True, blank=True,)
    file_url = models.CharField(max_length=255, blank=True, verbose_name="文件地址", help_text="文件地址")
    engine = models.CharField(max_length=100, default='local', blank=True, verbose_name="引擎", help_text="引擎")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="Mime类型", help_text="Mime类型")
    size = models.CharField(max_length=36, blank=True, verbose_name="文件大小", help_text="文件大小")
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")
    UPLOAD_METHOD_CHOIDES = (
        (0, '默认上传'),
        (1, '文件选择器上传'),
    )
    upload_method = models.SmallIntegerField(default=0, blank=True, null=True, choices=UPLOAD_METHOD_CHOIDES, verbose_name='上传方式', help_text='上传方式')
    FILE_TYPE_CHOIDES = (
        (0, '图片'),
        (1, '视频'),
        (2, '音频'),
        (3, '其他'),
    )
    file_type = models.SmallIntegerField(default=3, choices=FILE_TYPE_CHOIDES, blank=True, null=True, verbose_name='文件类型', help_text='文件类型')

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.url.size
        if not self.file_url:
            url = media_file_name(self, self.name)
            self.file_url = f'media/{url}'
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = "rj_file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)