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
import hashlib
from Crypto.Cipher import AES

from django.conf import settings
from django.core.cache import  cache

from rest_framework.exceptions import APIException
from rest_framework import status

from comutils.common.files import renameImageName
from conf import configs
from comutils.common.cache_keys import WX_APPLET_ACCESS_TOKEN_CK


def filter_emoji(desstr, restr=""):
  # 过滤表情
  try:
    res = re.compile(u"[\U00010000-\U0010ffff]")
  except re.error:
    res = re.compile(u"[\uD800-\uDBFF][\uDC00-\uDFFF]")
  return res.sub(restr, desstr)

"""
WeChat Crypt
"""
class WxCrypt:
  def __init__(self, appid, session_key):
    self.appid = appid
    self.session_key = session_key

  def decrypt(self, encryptedData, iv):
    # base64 decode
    session_key = base64.b64decode(self.session_key)
    encryptedData = base64.b64decode(encryptedData)
    iv = base64.b64decode(iv)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

    if decrypted["watermark"]["appid"] != self.appid:
        raise APIException("Invalid Buffer")

    return decrypted

  def _unpad(self, s):
    return s[:-ord(s[len(s)-1:])]


class WxAppletOpenId:
  def __init__(self, jscode):
    self.api_base_url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code"
    self.app_id = configs.WX_APPLET_APPID
    self.app_secret = configs.WX_APPLET_APPSECRET
    self.jscode = jscode
    self.api_url = self.api_base_url.format(self.app_id, self.app_secret, jscode)

  def get_openid(self):
    # if self.jscode == "111111":
    #   return "test_openid", "test_sesson_key", None
  
    res = requests.get(self.api_url)

    if res.status_code != 200:
      raise APIException("The server failed to connect to WeChat network. Please try again.")

    openid = None
    session_key = None
    unionid = None
    try:
      # json_data = {"errcode":0,"openid":"111","session_key":"test"}
      # res_json = res.json()
      res_json =json.loads(res.content)
      if "errcode" in res_json: #如果获取失败返回失败信息
        raise APIException(res_json["errmsg"])
      
      openid = res_json["openid"]
      session_key = res_json["session_key"]
      unionid = None
      if "unionid" in res_json:
        unionid = res_json["unionid"]

    except KeyError:
      raise APIException("Parse failed")
    
    if not session_key:
        raise APIException("WeChat server doesn't return session key")
    
    if not openid:
        raise APIException("WeChat server doesn't return openid")

    return openid, session_key, unionid


"""
获取小程序的access_token

正常返回，access_token 的有效期目前为 2 个小时，重复获取将导致上次获取的 access_token 失效
{"access_token":"ACCESS_TOKEN","expires_in":7200}
错误返回
{"errcode":40013,"errmsg":"invalid appid"}
"""
class WxAppletAccessToken: 
  def __init__(self):
    self.api_base_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
    self.app_id = configs.WX_APPLET_APPID
    self.app_secret = configs.WX_APPLET_APPSECRET
    self.api_url = self.api_base_url.format(self.app_id, self.app_secret)

  def get_access_token(self):
    access_token = cache.get(WX_APPLET_ACCESS_TOKEN_CK)

    if access_token:
      return access_token
    
    res = requests.get(self.api_url)

    if res.status_code != 200:
      raise APIException("Access_token: The server failed to connect to WeChat network. Please try again.")
    
    access_token = None
    expires_in = 7000
    try:
      # json_data = {"access_token":"ACCESS_TOKEN","expires_in":7200}
      res_json = res.json()
      # res_json =json.loads(res.content)

      if "errcode" in res_json  and res_json["errcode"] !=0 : #如果获取失败返回失败信息
        raise APIException(res_json["errmsg"])
      
      access_token = res_json["access_token"]

      expires_inget = int(res_json["expires_in"])
      if expires_inget > 200:
        expires_in = int(expires_inget) - 200

    except KeyError:
      raise APIException("Access token parse failed")
    
    if not access_token:
        raise APIException("WeChat server doesn't return access token")
    
    cache.set(WX_APPLET_ACCESS_TOKEN_CK, access_token, expires_in)
    return access_token


"""
微信小程序生成二维码

这个url生成二维码是无限个,返回的二维码是buffer类型(正式版小程序才能生成，体验版不行)

正常返回
{
 "errcode": 0,
 "errmsg": "ok",
 "contentType": "image/jpeg",
 "buffer": Buffer
}
"""
class WxAppletQrcode: 
  def __init__(self, access_token, scene, page, width=430, auto_color=True, is_hyaline=False):
    self.api_base_url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={0}"
    if not page:
      self.page = "pages/index/index"
    
    self.headers = {
      "Content-type":"application/json"
    }
    # scene 分享用户的 userid
    self.req_data = dict(scene=scene,page=page,width=width,auto_color=auto_color,is_hyaline=is_hyaline)
    
    self.api_url = self.api_base_url.format(access_token)

  def get_qrcode(self, width=430):

    if width:
      self.req_data["width"] = width

    res = requests.post(url=self.api_url,data=json.dumps(self.req_data),headers=self.headers)

    if res.status_code != 200:
      raise APIException("Qrcode: The server failed to connect to WeChat network. Please try again.")
    
    web_img_url = None
    try:
      res_json =json.loads(res.content)

      if "errcode" in res_json  and res_json["errcode"] !=0 : #如果获取失败返回失败信息
        raise APIException(res_json["errmsg"])
      
      curr_time = datetime.datetime.now()
      time_path = curr_time.strftime("%Y-%m-%d")
      img_task_dir = "wx_applet_qrcode"
      image_name = renameImageName("_QRcode.png")
      sub_path = os.path.join(settings.MEDIA_ROOT, img_task_dir, time_path)
      if not os.path.exists(sub_path):
          os.makedirs(sub_path)

      image_path = os.path.join(sub_path, image_name)
      web_img_url = configs.DOMAIN_HOST + settings.MEDIA_URL + img_task_dir + "/" + time_path + "/" + image_name  # 绝对路径http://xxx.xxx.com/media/xxx/xxxx/xxx.png
      with open(image_path, "wb") as f:
        f.write(res.content)
      
    except KeyError:
      raise APIException("Access token parse failed")
    
    if not web_img_url:
        raise APIException("Unable to obtain the sharing QR code")

    return web_img_url


"""
微信小程序发送服务通知消息 view 

1、form_id提交表单的id（支付时用）
2、data 提交的请求体
push_data={
    "keyword1":{
        "value":obj.order_sn
    },
    "keyword2":{
        "value":obj.time
    },
"""
class WxAppletMessage(): 
  def __init__(self, openid, template_id, form_id, push_data):
    self.api_base_url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={0}"
    # self.app_id = configs.WX_APPLET_APPID
    # self.app_secret = configs.WX_APPLET_APPSECRET
    # self.access_token = access_token
    # self.openid = openid
    # self.template_id = template_id
    # self.form_id = form_id
    # self.push_data = push_data
    self.payload = {
      "touser": openid, #这里为用户的openid
      "template_id": template_id, #模板id
      "form_id": form_id, #表单id或者prepay_id
      "data": push_data
    }

  def send_message(self):
    access_token = WxAppletAccessToken().get_access_token()
    api_url = self.api_base_url.format(access_token)
    res = requests.post(url=api_url, json=self.payload)

    if res.status_code != 200:
      raise APIException("Send: The server failed to connect to WeChat network. Please try again.")
    
    try:
      res_json =json.loads(res.content)

      if "errcode" in res_json  and res_json["errcode"] != 0: #如果获取失败返回失败信息
        # TODO
        # 记录日志
        print("微信小程序发送消息服务错误，用户openid:%s，template_id:%s，form_id:%s，data:%s，微信返回错误信息：%s" % (
            self.openid, self.template_id, self.form_id, self.push_data, res_json))
        raise APIException(res_json["errmsg"])
      
    except KeyError:
      raise APIException("Access token parse failed")

    return True
  


# ================================================= #
# ****************** 微信公众平台相关 ***************** #
# ================================================= #
class WxOfficialPlatform():
  app_id = configs.WX_OFFICIAL_PLATFORM_APPID
  app_secret = configs.WX_OFFICIAL_PLATFORM_APPSECRET
  
  """
  #通过 code 换取 access_token 和 openid, code为前端获取后传过来得
  正确返回
  {
    "access_token": "ACCESS_TOKEN", 有效期2小时
    "expires_in": 7200,
    "refresh_token": "REFRESH_TOKEN",有效期30天
    "openid": "OPENID",
    "scope": "SCOPE",
    "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
  }
  错误返回
  {
    "errcode": 40029,
    "errmsg": "invalid code"
  }
  """
  def get_openid_tokens(self, code):
    if not code: 
      raise APIException("code is blank")
    
    # access_token = cache.get(WX_APPLET_ACCESS_TOKEN_CK)

    # if access_token:
    #   return access_token
     
    api_base_url =  "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
    api_url = api_base_url.format(self.app_id, self.app_secret, code)

    res = requests.get(api_url)

    if res.status_code != 200:
      raise APIException("The server failed to connect to WeChat network. Please try again.")

    openid = None
    session_key = None
    unionid = None
    access_token = ""
    refresh_token = ""
    scope = None
    expires_in = 7000

    try:
      res_json =json.loads(res.content)

      if "errcode" in res_json and res_json['errcode'] !=0: #如果获取失败返回失败信息
        print("微信app登录服务错误，用户提交code:%s，微信返回错误信息：%s" % (code, res_json))
        raise APIException(res_json["errmsg"])
      
      openid = res_json["openid"]
      session_key = res_json["session_key"]
      if "unionid" in res_json:
        unionid = res_json["unionid"]

      access_token = res_json["access_token"]
      refresh_token = res_json["refresh_token"]
      scope = res_json["scope"]

      expires_inget = int(res_json["expires_in"])
      if expires_inget > 200:
        expires_in = int(expires_inget) - 200

    except KeyError:
      raise APIException("Parse failed")
    
    if not openid:
        raise APIException("WeChat server doesn't return openid")
    
    if not session_key:
        raise APIException("WeChat server doesn't return session key")
    
    if not access_token:
        raise APIException("WeChat server doesn't return access token")
    
    if not refresh_token:
        raise APIException("WeChat server doesn't return refresh key")
    

    cache.set(WX_APPLET_ACCESS_TOKEN_CK, access_token, expires_in)
    return {
      "openid": openid,
      "session_key": session_key,
      "unionid": unionid,
      "access_token": access_token,
      "refresh_token": refresh_token,
      "scope": scope,
    }
 

  """
  获取微信用户公开个人信息

  正确返回
  {
    "openid": "OPENID",
    "nickname": "NICKNAME",
    "sex": 1,
    "province": "PROVINCE",
    "city": "CITY",
    "country": "COUNTRY",
    "headimgurl": "https://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
    "privilege": ["PRIVILEGE1", "PRIVILEGE2"],
    "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
  }
  错误返回
  {
    "errcode": 40003,
    "errmsg": "invalid openid"
  }
  """
  def get_userinfo(self, access_token, openid):
    api_base_url =  "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN"
    api_url = api_base_url.format(access_token, openid)

    res = requests.get(api_url)

    if res.status_code != 200:
      raise APIException("The server failed to connect to WeChat network. Please try again.")

    openid = None
    nickname = None
    sex = None
    province = None
    city = None
    country = None
    headimgurl = None
    privilege = None
    unionid = None
    try:
      # res_json = res.json()
      res_json =json.loads(res.content)
      if "errcode" in res_json and res_json['errcode'] != 0: #如果获取失败返回失败信息
        raise APIException(res_json["errmsg"])
      
      openid = res_json["openid"]
      nickname = res_json["nickname"]
      sex = res_json["sex"]
      province = res_json["province"]
      city = res_json["city"]
      country = res_json["country"]
      headimgurl = res_json["headimgurl"]
      privilege = res_json["privilege"]

      unionid = None
      if "unionid" in res_json:
        unionid = res_json["unionid"]


    except KeyError:
      raise APIException("Parse failed")
    
    if not openid:
        raise APIException("WeChat server doesn't return openid")

    # return res_json
    return {
      "openid": openid,
      "nickname": nickname,
      "sex": sex,
      "province": province,
      "city": city,
      "country": country,
      "headimgurl": headimgurl,
      "privilege":  privilege,
      "unionid": unionid
    }

  """
  检验授权凭证access_token 是否有效

  有效返回
  {
    "errcode": 0,
    "errmsg": "ok"
  }
  """
  # TODO
  # 前面也有 sns 开头的接口，是不是要调整在一起
  def is_access_token_valid(self, access_token, openid):
    api_base_url = "https://api.weixin.qq.com/sns/auth?access_token={0}&openid={1}"
    api_url = api_base_url.format(access_token, openid)
    res = requests.get(api_url)
    return res
  
  # TODO
  # 未处理
  """
  微信公众平台通过refresh_token刷新过期的access_token

  有效返回
  {
    "access_token": "ACCESS_TOKEN",
    "expires_in": 7200,
    "refresh_token": "REFRESH_TOKEN",
    "openid": "OPENID",
    "scope": "SCOPE"
  }
  错误返回
  {
    "errcode": 40030,
    "errmsg": "invalid refresh_token"
  }
  """
  def refresh_access_token(self, refresh_token):
      api_base_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}"
      api_url = api_base_url.format(self.app_id,refresh_token)
      r = requests.get(api_url)
      return r


# ================================================= #
# ****************** 微信公众平台H5相关 ***************** #
# ================================================= #
class WxOfficialAccountH5():
  app_id = configs.WX_OFFICIAL_ACCOUNT_APPID
  app_secret = configs.WX_OFFICIAL_ACCOUNT_APPSECRET

  # 这个方法和 WxOfficialPlatform中的 get_openid_tokens 就是一样的
  def get_openid_tokens(self, code):
    if not code: 
      raise APIException("code is blank")
    
    # access_token = cache.get(WX_APPLET_ACCESS_TOKEN_CK)

    # if access_token:
    #   return access_token
      
    api_base_url =  "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
    api_url = api_base_url.format(self.app_id, self.app_secret, code)

    res = requests.get(api_url)

    if res.status_code != 200:
      raise APIException("The server failed to connect to WeChat network. Please try again.")

    openid = None
    session_key = None
    unionid = None
    access_token = ""
    refresh_token = ""
    scope = None
    expires_in = 7000

    try:
      res_json =json.loads(res.content)

      if "errcode" in res_json and res_json['errcode'] !=0: #如果获取失败返回失败信息
        print("微信app登录服务错误，用户提交code:%s，微信返回错误信息：%s" % (code, res_json))
        raise APIException(res_json["errmsg"])
      
      openid = res_json["openid"]
      session_key = res_json["session_key"]
      if "unionid" in res_json:
        unionid = res_json["unionid"]

      access_token = res_json["access_token"]
      refresh_token = res_json["refresh_token"]
      scope = res_json["scope"]

      expires_inget = int(res_json["expires_in"])
      if expires_inget > 200:
        expires_in = int(expires_inget) - 200

    except KeyError:
      raise APIException("Parse failed")
    
    if not openid:
        raise APIException("WeChat server doesn't return openid")
    
    if not session_key:
        raise APIException("WeChat server doesn't return session key")
    
    if not access_token:
        raise APIException("WeChat server doesn't return access token")
    
    if not refresh_token:
        raise APIException("WeChat server doesn't return refresh key")
    

    cache.set(WX_APPLET_ACCESS_TOKEN_CK, access_token, expires_in)
    return {
      "openid": openid,
      "session_key": session_key,
      "unionid": unionid,
      "access_token": access_token,
      "refresh_token": refresh_token,
      "scope": scope,
    }
  
  def check_h5_signature(token, timestamp, nonce, signature):
    temp = [token, timestamp, nonce]
    temp.sort()
    res = hashlib.sha1("".join(temp).encode('utf8')).hexdigest()
    return True if res == signature else False


