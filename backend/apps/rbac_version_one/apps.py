from django.apps import AppConfig


class RbacVersionOneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
   
    name = 'apps.rbac_version_one'
    path = 'apps/rbac_version_one'
