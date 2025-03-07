from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 更改路径
    name = 'apps.v1.files'
    path = 'apps/v1/files'
