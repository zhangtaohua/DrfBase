# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # @Time    : 2025/01/15 11:00
# # @Author  : RJ
# # @email   : zthvivid@163.com

# import datetime
# import random
# import string

# import xmltodict
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# from django.contrib.auth.models import User
# from django.shortcuts import render
# from pip._vendor import requests
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from rest_framework import viewsets, generics, views, status


# '''
# Mini Program Payment Callback
# '''

# class PayResultsNotice(views.APIView):
#     parser_classes = (XMLParser,)
#     IGNORE_FIELDS_PREFIX = ["coupon_type_","coupon_id_","coupon_fee_"]
#     def post(self,request):
#         dataDict = xmltodict.parse(request.body)["xml"] #type:dict
#         sign = WeChatSignHelper(dataDict,settings.WECHAT_MINIPROGRAM_CONFIG['WECHAT_PAY']['KEY']).getSign()
#         if sign != dataDict['sign']:
#             return Response(status=status.HTTP_403_FORBIDDEN)

#         keyToBeDelete = []
#         for key in dataDict.keys():
#             for ignorePrefix in self.IGNORE_FIELDS_PREFIX:
#                 if ignorePrefix in key:
#                     keyToBeDelete.append(key)
#         for key in keyToBeDelete:
#             del dataDict[key]

#         #process timeEnd
#         dataDict['time_end'] = datetime.datetime.strptime(dataDict['time_end'],"%Y%m%d%H%M%S")

#         dataDict['out_trade_no'] = dataDict['out_trade_no']
#         # assign order Id
#         preOrder = PayOrder.objects.filter(out_trade_no=dataDict['out_trade_no']).first()

#         if preOrder and not preOrder.paid:
#             preOrder.paid = True
#             preOrder.save()

#         return Response(data=WeChatPay().dic_to_xml({'return_code':'SUCCESS'}))