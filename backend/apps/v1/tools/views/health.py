#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework.views import APIView

from comutils.response.json_response import SuccessResponse, DataResponse

class HealthView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request, *args, **kwargs):
    return SuccessResponse()
  
class PingView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request, *args, **kwargs):
    return DataResponse({
      "message": "pong"
    })

