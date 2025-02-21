"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger doc
schema_view = get_schema_view(
   openapi.Info(
      title="DrfBase API",
      default_version="v1",
      description="DrfBase API",
      terms_of_service="https://www.rj.com/",
      contact=openapi.Contact(email="zthvivid@163.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # swagger doc
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # 接口白名单模型
    # path("api/whitelist/", include("apps.apiwhite.urls")),

    # 中国行政区
    path("api/china/regions/", include("apps.region.urls")),

    # 字典模型
    path("api/dicts/", include("apps.dictionary.urls")),

    # 共用工具模块
    path("api/tools/", include("apps.tools.urls")),

    # 用户模块
    path("api/users/", include("apps.users.urls")),

    # 登录认证模块
    path("api/auths/", include("apps.auths.urls")),

    # 第三方登录认证模块--微信
    path("api/wxauths/", include("apps.wxauths.urls")),

     # 第三方登录认证模块--抖音
    path("api/tiktokauths/", include("apps.tiktokauths.urls")),

    # 日志模型
    # path("api/logs/", include("apps.logs.urls")),
   
]
