#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

from django.db import DatabaseError

from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status
from comutils.response.json_response import  ErrorsResponse, ValidationErrorResponse


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)

  if response is not None:
    msg = response.data.get("detail", "")
    status_code = response.status_code
    print("custom_exception_handler response \r\n", response)
    print("exc", exc, type(exc))
    print(f"cus_exceptons 1 exc: {exc.get_codes()}, context: {context}\r\n")
    print(f"cus_exceptons 1 msg: {msg}, {type(msg)} status code: {status_code}")
    print("\r\n")
    errors = response.data
    # errors = exc.get_full_details()
    if msg:
      msg = "error: " + msg
    else:
      msg = "error: bad request"
    if isinstance(exc, ValidationError):
      return ValidationErrorResponse(errors=errors)
    
    return ErrorsResponse(errors=errors, msg=msg, status_code=status_code)
  else:
    view = context["view"]
    msg = f"error: internal server error, {exc}"
    
    print(f"cus_exceptons 2 exc: {exc}, context: {context}")
    print("\r\n")

    if isinstance(exc, DatabaseError):
      return ErrorsResponse(errors=None, msg=msg, status_code=status.HTTP_507_INSUFFICIENT_STORAGE)
    else:
      return ErrorsResponse(errors=None, msg=msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
