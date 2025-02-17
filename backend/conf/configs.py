import os

settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", None)

if settings_module:
  if settings_module.find("development") != -1:
    from .development import *
  else:
    from .production import *

else:
  from .development import *