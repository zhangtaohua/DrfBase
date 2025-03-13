#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from django_filters.rest_framework import BooleanFilter
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import OperationLog, LoginLog


class SystemConfigCreateSerializer(CustomModelSerializer):
    """
    系统配置-新增时使用-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_key(self, value):
        """
        验证key是否允许重复
        parent为空时不允许重复,反之允许
        """
        instance = SystemConfig.objects.filter(key=value, parent__isnull=True).exists()
        if instance:
            raise CustomValidationError('已存在相同变量名')
        return value




class SystemConfigSerializer(CustomModelSerializer):
    """
    系统配置-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigChinldernSerializer(CustomModelSerializer):
    """
    系统配置子级-序列化器
    """
    children = serializers.SerializerMethodField()
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    def get_children(self, instance):
        queryset = SystemConfig.objects.filter(parent=instance)
        serializer = SystemConfigSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigListSerializer(CustomModelSerializer):
    """
    系统配置下模块的保存-序列化器
    """

    def update(self, instance, validated_data):
        instance_mapping = {obj.id: obj for obj in instance}
        data_mapping = {item['id']: item for item in validated_data}
        for obj_id, data in data_mapping.items():
            instance_obj = instance_mapping.get(obj_id, None)
            if instance_obj is None:
                return SystemConfig.objects.create(**data)
            else:
                return instance_obj.objects.update(**data)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigSaveSerializer(serializers.Serializer):
    class Meta:
        read_only_fields = ["id"]
        list_serializer_class = SystemConfigListSerializer


class SystemConfigFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    parent__isnull = BooleanFilter(field_name='parent', lookup_expr="isnull")

    class Meta:
        model = SystemConfig
        fields = ['id', 'parent', 'status', 'parent__isnull']
