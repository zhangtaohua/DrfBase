from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
   
    name = 'apps.rbac'
    path = 'apps/rbac'
