#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com



class FileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = FileList.objects.all()
    serializer_class = FileSerializer
    filter_class = FileFilter
    permission_classes = []

    @action(methods=['GET'], detail=False)
    def get_all(self, request):
        data1 = self.get_serializer(self.get_queryset(), many=True).data
        data2 = []
        if dispatch.is_tenants_mode():
            from django_tenants.utils import schema_context
            with schema_context('public'):
                data2 = self.get_serializer(FileList.objects.all(), many=True).data
        return DetailResponse(data=data2+data1)

    def list(self, request, *args, **kwargs):
        if self.request.query_params.get('system', 'False') == 'True' and dispatch.is_tenants_mode():
            from django_tenants.utils import schema_context
            with schema_context('public'):
                return super().list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)