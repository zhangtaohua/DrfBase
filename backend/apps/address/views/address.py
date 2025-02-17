#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers import *

from ..models import Address

from comutils.response.json_response import DataResponse
from comutils.viewset.viewset import CustomModelViewSet

# TODO 只是复制过来，没有修改调试


# ================================================= #
# ************** 根据详细地址获取经纬度信息 view  ************** #
# ================================================= #
class GetAddressAccuracyView(APIView):
    """
    get:
    根据详细地址信息获取经纬度
    【参数】：address 为要查询的详细地址
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        address = request.data.get("address")
        if address is None:
            return ErrorResponse(msg="要查询的地址不能为空")
        # 获取经纬度
        data = gettecentlnglat(address)
        return  SuccessResponse(data=data,msg="success")

class GetAssressesListView(APIView):
    """
    用户查询地址列表/获取默认地址接口
    get:
    【参数】type=default 获取默认地址，不传type默认获取地址列表
    【参数】type=detail 获取单个地址详情，后面需跟上地址的id
    【参数】type=all 获取地址列表
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AddressSerializer

    def get(self, request):
        type = get_parameter_dic(request)['type']
        user = request.user
        if type == "default":
            # queryset = Address.objects.filter(id=user.default_address_id).first()
            queryset = Address.objects.filter(user=user, is_deleted=False,is_default=True).first()
            serializer = self.serializer_class(queryset,many=False)
            return SuccessResponse(data=serializer.data, msg="success")
        elif type == "detail":
            id = get_parameter_dic(request)['id']
            if id is None:
                return ErrorResponse(msg="id不能为空")
            queryset = Address.objects.filter(id=id,user=user,is_deleted=False).first()
            serializer = self.serializer_class(queryset, many=False)
            return SuccessResponse(data=serializer.data, msg="success")
        else:
            queryset = Address.objects.filter(user=user, is_deleted=False)
            serializer = self.serializer_class(queryset,many=True)
            return SuccessResponse(data=serializer.data,msg="success")

class CreateUpdateAssressesView(APIView):
    """
    用户地址新增/修改管理接口
    post:
    【参数】提交的参数名，与获取地址列表名保持一致
    receiver 收货人姓名
    province 省
    city 市
    district 区
    street 街道
    place 详细地址
    mobile 手机号
    参数中有id字段表示修改，没有id则表示新增
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AddressSerializer

    def post(self, request):
        mobile = get_parameter_dic(request)['mobile']
        if not re.match(REGEX_MOBILE, mobile):
            return ErrorResponse(msg="手机号不正确")
        user = request.user
        type = get_parameter_dic(request)['type']
        receiver = get_parameter_dic(request)['receiver']
        province = get_parameter_dic(request)['province']
        city = get_parameter_dic(request)['city']
        district = get_parameter_dic(request)['district']
        street = get_parameter_dic(request)['street']
        place = get_parameter_dic(request)['place']
        latitude=get_parameter_dic(request)['latitude']
        longitude=get_parameter_dic(request)['longitude']
        is_default = int(get_parameter_dic(request)['is_default'])

        if is_default not in [0,1]:
            return ErrorResponse(msg="is_default类型错误")

        if type=="add":#新增
            queryset = Address.objects.filter(user=user,is_deleted=False,is_default=True)
            if queryset:
                if is_default:
                    queryset.update(is_default=False)

            myaddress = Address.objects.create(user=user,receiver=receiver,province=province,city=city,district=district,street=street,place=place,mobile=mobile,latitude=latitude,longitude=longitude,is_default=is_default)
            return SuccessResponse(data={'addressid':myaddress.id},msg='success')
        elif type=='edit':
            id = get_parameter_dic(request)['id']
            queryset = Address.objects.filter(id=id,user=user).first()
            if queryset:#有这个地址数据
                otheraddresslist = Address.objects.filter(user=user,is_deleted=False).exclude(id=id)
                if is_default:  # 设置默认
                    if otheraddresslist:  # 取消其他地址的默认
                        otheraddresslist.update(is_default=False)
                    queryset.is_default = True
                else:  # 取消默认
                    queryset.is_default = False

                queryset.receiver = receiver
                queryset.province = province
                queryset.city = city
                queryset.district = district
                queryset.receiver = receiver
                queryset.street = street
                queryset.place = place
                queryset.mobile = mobile
                queryset.longitude = longitude
                queryset.latitude = latitude
                queryset.save()
                return SuccessResponse(msg='修改成功')
            else:
                return ErrorResponse(msg="修改失败")
        else:
            return ErrorResponse(msg="type类型错误")
class DeleteAssressesView(APIView):
    """
    用户地址删除接口
    get:
    【参数】id:需要删除的地址id
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AddressSerializer

    def get(self, request):
        id = get_parameter_dic(request)['id']
        if id is None:
            return ErrorResponse(msg="id不能为空")
        user = request.user
        queryset = Address.objects.filter(Q(id=id)&Q(user=user)&Q(is_deleted=False))
        if queryset:
            queryset.update(is_deleted=True)
            return SuccessResponse(msg='success')
        return ErrorResponse(msg="删除失败")

class SetDefaultAssressesView(APIView):
    """
    用户设置默认地址接口
    post:
    【参数】id:设置默认的地址id,is_default:0非默认地址，1默认地址
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AddressSerializer

    def post(self, request):
        id = get_parameter_dic(request)['id']
        is_default = get_parameter_dic(request)['is_default']
        if id is None:
            return ErrorResponse(msg="id不能为空")
        user = request.user
        otheraddresslist = Address.objects.filter(user=user).exclude(id=id)
        currentaddress = Address.objects.filter(id=id,user=user).first()
        if not currentaddress:
            return ErrorResponse(msg="设置失败")
        if is_default:#设置默认
            currentaddress.is_default = True
            currentaddress.save()
            if otheraddresslist:#取消其他地址的默认
                otheraddresslist.update(is_default=False)
            return SuccessResponse(msg='success')
        else:#取消默认
            currentaddress.is_default = False
            currentaddress.save()
            return SuccessResponse(msg='success')