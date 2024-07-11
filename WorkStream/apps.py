from django.apps import AppConfig
from django.core.management import load_command_class


class WorkStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkStream"

    def ready(self):
        
        # Registrar el comando personalizado
        try:
            load_command_class("WorkStream", "createsuperuser_if_none_exists")
        except ImportError:
            pass
