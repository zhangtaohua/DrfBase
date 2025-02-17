#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import hashlib

from django.apps import apps
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager

from comutils.models.models import BaseTimestampsModel

# 为了创建超级用户时，保持密码一值
# 不然就要用 from django.contrib.auth.hashers import make_password, check_password

class MyUserManager(UserManager):

  def _create_user(self, username, email, password, **extra_fields):
    """
    Create and save a user with the given username, email, and password.
    """
    if not username:
        raise ValueError("The given username must be set")
    
    email = self.normalize_email(email)
    # Lookup the real model class from the global app registry so this
    # manager method can be used in migrations. This is fine because
    # managers are by definition working on the real model.
    GlobalUserModel = apps.get_model(
        self.model._meta.app_label, self.model._meta.object_name
    )
    username = GlobalUserModel.normalize_username(username)
    user = self.model(username=username, email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)
    return self._create_user(username, email, password, **extra_fields)

  def create_superuser(self, username, email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self._create_user(username, email, password, **extra_fields)

class Users(AbstractUser, BaseTimestampsModel):
  """
    用户表
  """
  username = models.CharField(max_length=255, unique=True, db_index=True,
                              help_text="用户名", name="username", verbose_name="用户名")
  nickname = models.CharField(max_length=255, null=True, blank=True,
                              help_text="昵称", name="nickname", verbose_name="昵称")
  name = models.CharField(max_length=255, null=True, blank=True,
                              help_text="姓名", name="name", verbose_name="姓名")
  # password = models.CharField(max_length=255, help_text="密码", name="password", verbose_name="密码")
  email = models.EmailField(max_length=150, null=True, blank=True,
                              help_text="邮箱", name="email", verbose_name="邮箱")
  phone = models.CharField(max_length=32, null=True, blank=True,
                              help_text="手机号", name="phone", verbose_name="手机号")
  tel = models.CharField(max_length=64, null=True, blank=True,
                              help_text="座机电话", name="tel", verbose_name="座机电话")
  avatar = models.ImageField(upload_to="avatar", null=True, blank=True,
                              help_text="头像", name="avatar", verbose_name="头像")
  birthday = models.DateField(null=True, blank=True,
                              help_text="生日", name="birthday", verbose_name="生日")

  GENDER_CHOICES = (
    (0, "未知"),
    (1, "男"),
    (2, "女"),
  )
  gender = models.IntegerField(choices=GENDER_CHOICES, default=0, null=True, blank=True,
                                help_text="性别", name="gender", verbose_name="性别")
  
  USER_TYPE_CHOICES = (
    (0, "未知"),
    (1, "超级管理员"),
    (2, "系统管理员"),
    (3, "普通用户"),
  )
  user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0, null=True, blank=True,
                                  help_text="用户类型", name="user_type", verbose_name="用户类型")

  login_error_count = models.IntegerField(default=0, verbose_name="登录错误次数", help_text="登录错误次数")
  pwd_change_count = models.IntegerField(default=0,blank=True, verbose_name="密码修改次数", help_text="密码修改次数")


  objects = MyUserManager()
  def set_password(self, raw_password):
    hex_password = hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest()
    # print("set_pw", hex_password)
    super().set_password(hex_password)

  def check_password(self, raw_password):
    hex_password = hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest()
    # print("check_pw", hex_password)
    return super().check_password(hex_password)
  

  class Meta:
    db_table = "rj_users"
    verbose_name = "用户表"
    verbose_name_plural = verbose_name
    ordering = ["-id", "-create_time"]
