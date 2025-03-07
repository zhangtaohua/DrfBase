#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.conf import settings
from django.db import models

from comutils.models.models import BaseTimestampsModel

# Create your models here.

class Company(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="company name", name="name", verbose_name="公司名称")
  representative = models.CharField(max_length=150, null=True, blank=True, 
                           help_text="legal representative", name="representative", verbose_name="法定代表人")
  email = models.EmailField(max_length=150, null=True, blank=True,
                              help_text="email", name="email", verbose_name="邮箱")
  phone = models.CharField(max_length=32, null=True, blank=True,
                              help_text="phone", name="phone", verbose_name="手机号")
  
  code = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="unified social credit code", name="code", verbose_name="统一社会信用代码")
  registration_number = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="Business registration number", name="registration_number", verbose_name="工商注册号")
  customs_code = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="customs registration code", name="customs_code", verbose_name="海关注册编码")
  ie_code = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="import and export enterprise code", name="ie_code", verbose_name="进出口企业代码")
  
  taxpyer = models.CharField(max_length=150, null=True, blank=True, 
                           help_text="taxpayer qualification", name="taxpyer", verbose_name="纳税人资质")
    
  registered_capital = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True, 
                           help_text="registered capital", name="registered_capital", verbose_name="注册资本")
  
  paidin_capital = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True, 
                           help_text="paid-in capital", name="paidin_capital", verbose_name="实缴资本")
  
  establishment_time = models.DateTimeField(null=True, blank=True, 
                                   help_text="data of establishment", name="establishment_time", verbose_name="成立时间")
  approval_time = models.DateTimeField(null=True, blank=True, 
                                   help_text="data of approval", name="approval_time", verbose_name="核准时间")
  
  enterprise_type = models.CharField(max_length=150, null=True, blank=True, 
                          help_text="enterprise type", name="enterprise_type", verbose_name="企业类型")
  
  industry = models.CharField(max_length=150, null=True, blank=True, 
                          help_text="affiliated industry", name="industry", verbose_name="所属行业")
  
  registration_authority = models.CharField(max_length=250, null=True, blank=True, 
                           help_text="registration authority", name="registration_authority", verbose_name="登记机关")
  registered_address = models.CharField(max_length=250, null=True, blank=True, 
                           help_text="registered address", name="registered_address", verbose_name="注册地址")
  
  business_scope = models.TextField(null=True, blank=True, 
                           help_text="business scope", name="business_scope", verbose_name="经营范围")
  
  
  STATUS_CHOICES = (
    (0, "倒闭"),
    (1, "存续"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="registration status", name="status", verbose_name="登记状态")
  
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="显示排序")

  parent = models.ForeignKey(
    to="self",
    on_delete=models.CASCADE,
    default=None,
    db_constraint=False,
    null=True,
    blank=True,
    help_text="parent company",
    verbose_name="上级公司",
  )

  class Meta:
    db_table="rj_company"
    verbose_name= "公司表"
    verbose_name_plural = verbose_name
    ordering = ("sort", )




class Dept(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="department name", name="name", verbose_name="部门名称")
  key = models.CharField(max_length=150, unique=True, null=True, blank=True,
                          help_text="relate key", name="key", verbose_name="关联字符")
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="显示排序")
  STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="department status", name="status", verbose_name="部门状态")
  
  owner = models.CharField(max_length=150, null=True, blank=True, 
                           help_text="owner", name="owner", verbose_name="负责人")
  email = models.EmailField(max_length=150, null=True, blank=True,
                              help_text="email", name="email", verbose_name="邮箱")
  phone = models.CharField(max_length=32, null=True, blank=True,
                              help_text="phone", name="phone", verbose_name="手机号")

  parent = models.ForeignKey(
    to="Dept",
    on_delete=models.CASCADE,
    default=None,
    db_constraint=False,
    null=True,
    blank=True,
    help_text="parent department",
    verbose_name="上级部门",
  )

  user = models.ForeignKey(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    db_constraint=False, null=True, blank=True, 
    help_text="user relate dept", 
    verbose_name="用户关联部门")
  

  @classmethod
  def recursion_all_dept(cls, dept_id: int, dept_all_list=None, dept_list=None):
    """
    递归获取部门的所有下级部门
    :param dept_id: 需要获取的id
    :param dept_all_list: 所有列表
    :param dept_list: 递归list
    :return:
    """
    if not dept_all_list:
      dept_all_list = Dept.objects.values("id", "parent")
    if dept_list is None:
      dept_list = [dept_id]
    for ele in dept_all_list:
      if ele.get("parent") == dept_id:
        dept_list.append(ele.get("id"))
        cls.recursion_all_dept(ele.get("id"), dept_all_list, dept_list)
    return list(set(dept_list))

  class Meta:
    db_table = "rj_organizationdept"
    verbose_name = "部门表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)


class Post(BaseTimestampsModel):
  name = models.CharField(max_length=150, null=False,
                          help_text="post name", name="name", verbose_name="职位名称")
  code = models.CharField(max_length=64,
                          help_text="post code", name="code", verbose_name="职位编码")
  sort = models.IntegerField(default=1,
                            help_text="sort", name="sort", verbose_name="职位顺序")
  STATUS_CHOICES = (
    (0, "离职"),
    (1, "在职"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, default=1, 
                              help_text="post status", name="status", verbose_name="职位状态")

  user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, db_constraint=False, 
                                help_text="user relate post", verbose_name="用户关联职位")
  
  class Meta:
    db_table = "rj_organization_post"
    verbose_name = "职位表"
    verbose_name_plural = verbose_name
    ordering = ("sort",)