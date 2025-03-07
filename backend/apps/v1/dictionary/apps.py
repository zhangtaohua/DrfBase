from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 更改路径
    name = 'apps.v1.dictionary'
    path = 'apps/v1/dictionary'
