from django.apps import AppConfig


class WxauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
   
    # 更改路径
    name = 'apps.wxauths'
    path = "apps/wxauths"
