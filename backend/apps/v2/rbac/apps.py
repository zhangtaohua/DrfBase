from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.v2.rbac'
    path = 'apps/v2/rbac'
