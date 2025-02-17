#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import base64

from django.conf import settings

from rest_framework.views import APIView

from captcha.views import CaptchaStore, captcha_image

from comutils.response.json_response import DataResponse

class CaptchaView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request):
    data = {}
    # if settings.CAPTCHAVIEW == "char":
    
    hashkey = CaptchaStore.generate_key()
    id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
    imgage = captcha_image(request, hashkey)
    # 将图片转换为base64
    image_base = base64.b64encode(imgage.content)
    data = {
      "key": id,
      "image": "data:image/png;base64," + image_base.decode("utf-8"),
    }
    return DataResponse(data=data)


