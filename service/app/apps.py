from django.apps import AppConfig as ApplicationConfig


class AppConfig(ApplicationConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
