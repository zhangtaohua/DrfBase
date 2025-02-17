from django.apps import AppConfig


class ToolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 更改路径
    name = 'apps.tools'
    path = 'apps/tools'
