#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/01/14 11:00
# @Author  : RJ
# @email   : zthvivid@163.com

"""
@Remark: 自定义的 API Json 响应类
"""

from enum import Enum
from rest_framework.response import Response
from rest_framework import status

class RES_CODE(Enum):
  SUCCESS = 0
  ERROR = -1
  BAD_REQUEST = -400
  UNAUTHORIZED = -401
  FORBIDDEN = -403
  NOT_FOUND = -404
  METHOD_NOT_ALLOWED = -405
  CONFLICT = -409
  UNPROCESSABLE_ENTITY = -422
  INTERNAL_SERVER_ERROR = -500
  BAD_GATEWAY = -502
  SERVICE_UNAVAILABLE = -503


class SuccessResponse(Response):
  def __init__(self, msg="success: success"):
    super().__init__({
      "code": RES_CODE.SUCCESS.value,
      "message": msg,
      "success": True,
    }, status=status.HTTP_200_OK)

  # def __str__(self):
    # return "No data success response"
    # return super().__str__()

class DeleteResponse(Response):
  def __init__(self, msg="success: deleted"):
    super().__init__({
      "code": RES_CODE.SUCCESS.value,
      "message": msg,
      "success": True,
    }, status=status.HTTP_204_NO_CONTENT)

class DataResponse(Response):
  def __init__(self, data=None, msg="success: data response", headers=None):
    # TODO 为了兼容前端，这里的 data 不能为 None
    if data is None:
      data = {}

    super().__init__({
      "code": RES_CODE.SUCCESS.value,
      "message": msg,
      "success": True,
      "data": data,
    }, status=status.HTTP_200_OK, headers=headers)

class CreatedResponse(Response):
  def __init__(self, data=None, msg="success: created", headers=None):
    # TODO 为了兼容前端，这里的 data 不能为 None
    if data is None:
      data = {}

    super().__init__({
      "code": RES_CODE.SUCCESS.value,
      "message": msg,
      "success": True,
      "data": data,
    }, status=status.HTTP_201_CREATED, headers=headers)


# errors handler

class ErrorsResponse(Response):
  def __init__(self, errors=None, msg="error: bad request" ,code=RES_CODE.ERROR.value, status_code=status.HTTP_400_BAD_REQUEST):
   
    # TODO 为了兼容前端，这里的 data 不能为 None
    err =   errors if errors else {}

    super().__init__({
      "code": code,
      "message": msg,
      "success": False,
      "errors": err,
    }, status_code)

class BadRequestResponse(Response):
  def __init__(self, errors=None, msg="error: bad request"):
   
    # TODO 为了兼容前端，这里的 data 不能为 None
    err =   errors if errors else {}

    super().__init__({
      "code": RES_CODE.BAD_REQUEST.value,
      "message": msg,
      "success": False,
      "errors": err,
    }, status=status.HTTP_400_BAD_REQUEST)

class UnauthorizedResponse(Response):
  def __init__(self, msg="error: unauthorized"):
    super().__init__({
      "code": RES_CODE.UNAUTHORIZED.value,
      "message": msg,
      "success": False,
    }, status=status.HTTP_401_UNAUTHORIZED)

class ForbiddenResponse(Response):
  def __init__(self, msg="error: forbidden"):
    super().__init__({
      "code": RES_CODE.FORBIDDEN.value,
      "message": msg,
      "success": False,
    }, status=status.HTTP_403_FORBIDDEN)

class NotFoundResponse(Response):
  def __init__(self, msg="error: not found"):
    super().__init__({
      "code": RES_CODE.NOT_FOUND.value,
      "message": msg,
      "success": False,
    }, status=status.HTTP_404_NOT_FOUND)

class InternalServerErrorResponse(Response):
  def __init__(self, msg="error: internal server error"):
    super().__init__({
      "code": RES_CODE.INTERNAL_SERVER_ERROR.value,
      "message": msg,
      "success": False,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class ValidationErrorResponse(Response):
  def __init__(self, errors=None, msg="error: validation error"):
    # TODO 为了兼容前端，这里的 data 不能为 None
    err =  errors if errors else {}

    super().__init__({
      "code": RES_CODE.UNPROCESSABLE_ENTITY.value,
      "message": msg,
      "success": False,
      "errors": err,
    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



