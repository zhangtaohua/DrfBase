#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.core.cache import cache
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.renderers import StaticHTMLRenderer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from comutils.response.json_response import DataResponse, ErrorsResponse
from comutils.viewset.viewset import CustomModelViewSet


class PrivacyView(APIView):
  """
  后台隐私政策
  """
  permission_classes = []

  def get(self, request, *args, **kwargs):
    # return render(request, 'privacy.html')
    return StaticHTMLRenderer(request, 'privacy.html')



class TermsServiceView(APIView):
  """
  后台服务条款
  """
  permission_classes = []

  def get(self, request, *args, **kwargs):
    # return render(request, 'terms_service.html')
    return StaticHTMLRenderer(request, 'terms_service.html')

