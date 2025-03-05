from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 更改路径
    name = 'apps.users'
    path = 'apps/users'
