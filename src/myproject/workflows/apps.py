from django.apps import AppConfig


class WorkflowsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myproject.workflows"
    verbose_name = "Workflows"

    def ready(self):
        import myproject.workflows.signals  # noqa: F401
