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

urlpatterns = [
    path("admin/", admin.site.urls),

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
   
]
