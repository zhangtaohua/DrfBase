#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/15 11:00
# @Author  : RJ
# @email   : zthvivid@163.com


from django.db import models
from django.conf import settings

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class Address(BaseTimestampsModel):

  # one to many
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses",
                           help_text="user", name="user", verbose_name="所属用户")
  receiver = models.CharField(max_length=150, null=True, blank=True,
                              help_text="receiver", name="receiver", verbose_name="收货人")
  title = models.CharField(max_length=20, null=True, blank=True,
                          help_text="title", name="title", verbose_name='地址名称')
  
  phone = models.CharField(max_length=64, null=True, blank=True,
                            help_text="phone", name="phone", verbose_name="手机号")
  
  tel = models.CharField(max_length=64, null=True, blank=True, default='',
                              help_text="座机电话", name="tel", verbose_name="座机电话")
  email = models.EmailField(max_length=150, null=True, blank=True, default='',
                              help_text="邮箱", name="email", verbose_name="邮箱")

  country = models.CharField(max_length=150, null=True, blank=True,
                            help_text="country", name="country", verbose_name="国家")
  province = models.CharField(max_length=150, null=True, blank=True,
                            help_text="province", name="province", verbose_name="省")
  city = models.CharField(max_length=150,null=True, blank=True,
                          help_text="city", name="city", verbose_name="市")
  district = models.CharField(max_length=150, null=True, blank=True,
                              help_text="district", name="district", verbose_name="区/县")
  town = models.CharField(max_length=150, null=True, blank=True,
                              help_text="town", name="town", verbose_name="镇")
  village = models.CharField(max_length=150, null=True, blank=True,
                              help_text="village", name="village", verbose_name="村")
  
 
  street = models.CharField(max_length=150, null=True, blank=True,
                            help_text="street", name="street", verbose_name="街道")
  place = models.CharField(max_length=150,
                          help_text="place", name="place", verbose_name="收货地址")
  
  PLACE_CHOICES = (
    (0, "家"),
    (1, "公司"),
    (2, "临时"),
  )

  type = models.SmallIntegerField(choices=PLACE_CHOICES, null=True, blank=True,
                                  help_text="type", name="type", verbose_name="类型")
  longitude = models.FloatField(verbose_name="经度", null=True, blank=True,
                                help_text="longitude", name="longitude", verbose_name="经度")
  latitude = models.FloatField(verbose_name="纬度", null=True, blank=True,
                               help_text="latitude", name="latitude", verbose_name="纬度")
  is_default = models.BooleanField(default=False,
                                   help_text="is default", name="is_default", verbose_name="是否默认")
  is_deleted = models.BooleanField(default=False,
                                   help_text="is deleted", name="is_deleted", verbose_name="逻辑删除") #是否有效，是否显示
  
  def get_region_format(self):

    return "{self.country}{self.provice}{self.city}{self.district}{self.town}{self.village}".format(self=self)
  
  class Meta:
    db_table = "rj_user_address"
    verbose_name = "用户地址"
    verbose_name_plural = verbose_name

  def __str__(self):
    if self.street:
      return self.get_region_format() + self.street + self.place
    else:
      return self.get_region_format() + self.place
