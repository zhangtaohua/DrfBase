#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from apps.users.models import Users
from apps.users.serializers import UserSerializer

from comutils.viewset.viewset import CustomModelViewSet

class UserViewSet(CustomModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UserSerializer
  # ordering_fields = '__all__'
  # ordering_fields = ("id", "create_time", "update_time",)
  # ordering = ("-create_time",)

  # def get_queryset(self):
  #   return self.queryset.filter(delete_time__isnull=True)

  # def perform_destroy(self, instance):
  #   instance.delete_time = timezone.now()
  #   instance.save()
  #   return instance
