from django.apps import AppConfig


class WxauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
   
    # 更改路径
    name = 'apps.v1.wxauths'
    path = 'apps/v1/wxauths'
