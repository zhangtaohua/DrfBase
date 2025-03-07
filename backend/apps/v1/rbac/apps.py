from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
   
    name = 'apps.v1.rbac'
    path = 'apps/v1/rbac'
