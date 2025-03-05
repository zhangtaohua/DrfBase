#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django_filters.rest_framework import FilterSet, CharFilter

from ..serializers import *

from ..models import FilesDownload

from comutils.response.json_response import DataResponse
from comutils.viewset.viewset import CustomModelViewSet


class FilesDownloadFilterSet(FilterSet):
  task = CharFilter(field_name='task', lookup_expr='icontains')
  file_name = CharFilter(field_name='file_name', lookup_expr='icontains')

  class Meta:
    model = filter
    fields = ['status', 'task', 'file_name']


class FilesDownloadViewSet(CustomModelViewSet):
  queryset = FilesDownload.objects.all()
  serializer_class = FilesDownloadSerializer
  filter_class = FilesDownloadFilterSet
  permission_classes = []
  extra_filter_class = []

  def get_queryset(self):
    if self.request.user.is_superuser:
      return super().get_queryset()
    
    return super().get_queryset().filter(creator=self.request.user)

