from django.apps import AppConfig


class AuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 更改路径
    name = 'apps.auths'
    path = 'apps/auths'
