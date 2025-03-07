from django.apps import AppConfig


class AddressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.v1.address'
    path = 'apps/v1/address'
