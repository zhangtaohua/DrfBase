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
