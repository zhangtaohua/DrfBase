#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import FilesDownload

class FilesDownloadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
      if self.request.query_params.get('prefix'):
        if settings.ENVIRONMENT in ['local']:
          prefix = 'http://127.0.0.1:8000'
        elif settings.ENVIRONMENT in ['test']:
          prefix = 'http://{host}/api'.format(host=self.request.get_host())
        else:
          prefix = 'https://{host}/api'.format(host=self.request.get_host())
        return (f'{prefix}/media/{str(instance.url)}')
      return f'media/{str(instance.url)}'

    class Meta:
      model = FilesDownload
      fields = "__all__"
      read_only_fields = ["id"]


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        if self.request.query_params.get('prefix'):
            if settings.ENVIRONMENT in ['local']:
                prefix = 'http://127.0.0.1:8000'
            elif settings.ENVIRONMENT in ['test']:
                prefix = 'http://{host}/api'.format(host=self.request.get_host())
            else:
                prefix = 'https://{host}/api'.format(host=self.request.get_host())
            if instance.file_url:
                return instance.file_url if instance.file_url.startswith('http') else f"{prefix}/{instance.file_url}"
            return (f'{prefix}/media/{str(instance.url)}')
        return instance.file_url or (f'media/{str(instance.url)}')

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        file_engine = dispatch.get_system_config_values("fileStorageConfig.file_engine") or 'local'
        file_backup = dispatch.get_system_config_values("fileStorageConfig.file_backup")
        file = self.initial_data.get('file')
        file_size = file.size
        validated_data['name'] = str(file)
        validated_data['size'] = file_size
        md5 = hashlib.md5()
        for chunk in file.chunks():
            md5.update(chunk)
        validated_data['md5sum'] = md5.hexdigest()
        validated_data['engine'] = file_engine
        validated_data['mime_type'] = file.content_type
        ft = {'image':0,'video':1,'audio':2}.get(file.content_type.split('/')[0], None)
        validated_data['file_type'] = 3 if ft is None else ft
        if file_backup:
            validated_data['url'] = file
        if file_engine == 'oss':
            from dvadmin_cloud_storage.views.aliyun import ali_oss_upload
            file_path = ali_oss_upload(file)
            if file_path:
                validated_data['file_url'] = file_path
            else:
                raise ValueError("上传失败")
        elif file_engine == 'cos':
            from dvadmin_cloud_storage.views.tencent import tencent_cos_upload
            file_path = tencent_cos_upload(file)
            if file_path:
                validated_data['file_url'] = file_path
            else:
                raise ValueError("上传失败")
        else:
            validated_data['url'] = file
        # 审计字段
        try:
            request_user = self.request.user
            validated_data['dept_belong_id'] = request_user.dept.id
            validated_data['creator'] = request_user.id
            validated_data['modifier'] = request_user.id
        except:
            pass
        return super().create(validated_data)


class FileAllSerializer(CustomModelSerializer):
    
    class Meta:
        model = FileList
        fields = ['id', 'name']


class FileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", help_text="文件名")
    mime_type = django_filters.CharFilter(field_name="mime_type", lookup_expr="icontains", help_text="文件类型")

    class Meta:
        model = FileList
        fields = ['name', 'mime_type', 'upload_method', 'file_type']