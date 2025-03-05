#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from rest_framework.views import APIView

from ..serializers import *

from ..models import Dictionary

from comutils.response.json_response import DataResponse
from comutils.viewset.viewset import CustomModelViewSet

class DictionaryViewSet(CustomModelViewSet):

  queryset = Dictionary.objects.all()
  serializer_class = DictionarySerializer
  filterset_fields = ["status"]
  search_fields =["name", "label"]

  def trees(self, request):
    params = request.query_params
    parent = params.get("parent", None)
    queryset = Dictionary.objects.exclude(status=0).filter(parent=None)
    if params:
      if parent:
        queryset = Dictionary.objects.exclude(status=0).filter(parent=parent)
      
    serializer = DictionaryTreeSerializer(queryset, many=True)

    return DataResponse(serializer.data)
  
  def retrive_children(self, request, pk):
    queryset = Dictionary.objects.exclude(status=0).get(pk=pk)
    serializer = DictionaryTreeSerializer(queryset)

    return DataResponse(serializer.data)
  
  def get_queryset(self):
    # return super().get_queryset()
    if self.action =="list":
      params = self.request.query_params
      parent = params.get("parent", None)
      if params:
        if parent:
          queryset = self.queryset.filter(parent=parent)
        else:
          queryset = self.queryset.filter(parent__isnull=True)
      else:
        queryset = self.queryset.filter(parent__isnull=True)
      return queryset
    else:
      return self.queryset

class InitDictionaryViewSet(APIView):
  """
  获取初始化配置
  """
  authentication_classes = []
  permission_classes = []
  queryset = Dictionary.objects.all()

  def get(self, request):
    dictionary_key = self.request.query_params.get("dictionary_key")
    if dictionary_key:
      if dictionary_key == "all":
        pass
        # data = [ele for ele in dispatch.get_dictionary_config().values()]
        # if not data:
          # dispatch.refresh_dictionary()
          # data = [ele for ele in dispatch.get_dictionary_config().values()]
        
      else:
          data = self.queryset.filter(parent__value=dictionary_key, status=True).values("label", "value", "type",
                                                                                          "color")
      return DataResponse(data=data, msg="获取成功")
    
    return DataResponse(data=[], msg="获取成功")





