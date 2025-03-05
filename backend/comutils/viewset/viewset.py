#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework import status
from rest_framework.settings import api_settings

from rest_framework.viewsets import GenericViewSet

from comutils.mixins import viewset_mixins

class CustomModelViewSet(viewset_mixins.CreateModelMixin,
                   viewset_mixins.RetrieveModelMixin,
                   viewset_mixins.UpdateModelMixin,
                   viewset_mixins.DestroyModelMixin,
                   viewset_mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
