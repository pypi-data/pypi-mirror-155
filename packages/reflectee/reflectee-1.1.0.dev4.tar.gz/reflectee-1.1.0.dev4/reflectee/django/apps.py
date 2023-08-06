import os

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

__all__ = ["DjangoAppConfig"]


class DjangoAppConfig(AppConfig):
    name = "reflectee"
    verbose_name = "Application"

    def ready(self):

        from django.conf import settings

        from ..core.handlers import loads

        api_path = getattr(
            settings,
            "REFLECTEE_API_PATH",
            os.environ.get("REFLECTEE_API_PATH", None),
        )
        if api_path:
            loads(api_path)

        autodiscover_modules("api", "views")
        # from django.apps import apps
        # for app_config in apps.get_app_configs():
