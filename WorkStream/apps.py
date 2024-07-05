from django.apps import AppConfig


class WorkStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkStream"

    def ready(self):
        import WorkStream.signals

    def ready(self):
        try:
            from django.core.management import load_command_class

            import WorkStream.signals  # Importar señales si las tienes

            load_command_class(
                "myapp", "createsuperuser_if_none_exists"
            )  # Registrar el comando personalizado
        except ImportError:
            pass
