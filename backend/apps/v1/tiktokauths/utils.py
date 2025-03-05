#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

import re
import os
import base64
import json
import requests
import datetime
from Crypto.Cipher import AES

from django.conf import settings
from django.core.cache import  cache

from rest_framework.exceptions import APIException
from rest_framework import status

from comutils.common.files import renameImageName
from conf import configs
from comutils.common.cache_keys import TIKTOK_APPLET_ACCESS_TOKEN_CK

class TictokAppletOpenId:
  app_id = configs.TIKTOK_APPLET_APPID
  app_secret = configs.TIKTOK_APPLE_APPSECRET
  headers = { 
    "Content-Type": "application/json"
  }

  # 接口调用凭证getAccessToken，获取的access_token有效期2 小时，
  # 重复获取 access_token 会导致上次 access_token 失效。
  # 为了平滑过渡，新老 access_token 在 5 分钟内都可使用
  """
    正确返回信息：
    {
      "err_no": 0,
      "err_tips": "success",
      "data": {
        "access_token": "0801121***********",
        "expires_in": 7200
      }
    }
  """
  def get_access_token(self):
    access_token = cache.get(TIKTOK_APPLET_ACCESS_TOKEN_CK)

    if access_token:
      return access_token
    
    api_url = "https://developer.toutiao.com/api/apps/v2/token"
    payload = {
      "appid":  self.app_id,
      "secret": self.app_secret,
      "grant_type": "client_credential"
      }
  
    res = requests.post(url=api_url, data=json.dumps(payload), headers=self.headers)

    if res.status_code != 200:
      raise APIException("The server failed to connect to Tiktok network. Please try again.")

    access_token = None
    expires_in = 7000
    try:
      res_json =json.loads(res.content)
      if not int(res_json["err_no"]) == 0:#如果获取失败返回失败信息
        print("Tiktok session:", res_json)
        raise APIException(res_json["err_tips"])
      
      access_token = res_json["data"]["access_token"]

      expires_inget = int(res_json["data"]["expires_in"])
      if expires_inget > 200:
        expires_in = int(expires_inget) - 200
      
    except KeyError:
      raise APIException("Access token parse failed")
    
    if not access_token:
        raise APIException("Tiktok server doesn't return access_token")

    cache.set(TIKTOK_APPLET_ACCESS_TOKEN_CK, access_token, expires_in)
    return access_token


  """
    获取字节跳动code2Session（返回值有openid）

    code：为前端小程序通过tt.login传过来的code
    小程序正确返回信息：
    {
      "err_no": 0,
      "err_tips": "success",
      "data": {
        "session_key": "hZy6t19VPjFqm********",
        "openid": "V3WvSshYq9******",
        "anonymous_openid": "",
        "unionid": "f7510d9ab***********"
      }
    }
  """
  def get_session_key(self, code):
    api_url = "https://developer.toutiao.com/api/apps/v2/jscode2session"
    payload = {
      "appid":  self.app_id,
      "secret": self.app_secret,
      "code": code
      }
  
    res = requests.post(url=api_url, data=json.dumps(payload), headers=self.headers)

    if res.status_code != 200:
      raise APIException("The server failed to connect to Tiktok network. Please try again.")

    openid = None
    session_key = None
    unionid = None
    anonymous_openid = None
    try:
      # res_json = res.json()
      res_json =json.loads(res.content)
      if not int(res_json["err_no"]) == 0:#如果获取失败返回失败信息
        print("Tiktok session:", res_json)
        raise APIException(res_json["err_tips"])
      
      openid = res_json["data"]["openid"]
      session_key = res_json["data"]["session_key"]
      if "unionid" in res_json["data"]:
        unionid = res_json['unionid']
      
      if "anonymous_openid" in res_json["data"]:
        anonymous_openid = res_json['anonymous_openid']

    except KeyError:
      raise APIException("Parse failed")
    
    if not session_key:
        raise APIException("Tiktok server doesn't return session key")
    
    if not openid:
        raise APIException("Tiktok server doesn't return openid")

    return openid, session_key, unionid, anonymous_openid




