from django.apps import AppConfig


class WorkStreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "WorkStream"

    def ready(self):
        import WorkStream.signals
