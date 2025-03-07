from django.apps import AppConfig


class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.v1.message'
    path = 'apps/v1/message'
