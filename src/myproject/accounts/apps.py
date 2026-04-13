from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myproject.accounts"
    verbose_name = "Accounts"

    def ready(self):
        import myproject.accounts.signals  # noqa: F401
