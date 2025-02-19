#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: 腾讯云短信
"""

# ------------------------------
# #unicloud短信云函数url发短信api
# ------------------------------
# 官网文档地址：https://uniapp.dcloud.net.cn/uniCloud/send-sms.html
# ------------------------------

import requests
import json

class UniCloudSms(object):

    def __init__(self):
        self.single_send_url = "https://XXXXXXX.bspapp.com/http/lybbnunisms"#要修改的短信url

    def send_sms(self, code, mobile, expminute):
        # 需要传递的参数
        parmas = {
            "mobile": mobile,
            "code": code, #验证码
            "expminute":expminute//60 #把秒转换成分钟
        }
        contenttype = "application/json"
        headers = {'Content-Type': contenttype}
        response = requests.post(self.single_send_url, data=json.dumps(parmas),headers = headers)
        # print(response.text)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    unicloudsms = UniCloudSms()
    unicloudsms.send_sms("2021", "手机号码",300)