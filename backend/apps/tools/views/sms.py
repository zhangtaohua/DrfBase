#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from random import choice

from django.core.cache import cache

from rest_framework.views import APIView

from ..serializers import sms

from comutils.common.cache_keys import SMS_CODE_CK, SMS_SENT_CK
from comutils.response.json_response import SuccessResponse, DataResponse, ErrorsResponse

class SmsCodeView(APIView):
  authentication_classes = []
  permission_classes = []
  serializer_class = sms.SmsCodeSerializer

  def generate_sms_code(self):
    seeds = "1234567890"
    random_str = []
    for i in range(6):
      random_str.append(choice(seeds))

    return "".join(random_str)

  def post(self, request, *args, **kwargs):
    serializer = sms.SmsCodeSerializer(data=request.data)
    if serializer.is_valid():
      phone = serializer.validated_data.get("phone")
      code = self.generate_sms_code()
      cache.set(SMS_SENT_CK.format(phone), code, 60 * 2)
      cache.set(SMS_CODE_CK.format(phone), code, 60 * 2)

      # TODO: send sms code to phone

      return SuccessResponse()
    return ErrorsResponse(errors=serializer.errors)

