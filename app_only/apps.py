from django.apps import AppConfig


class AppOnlyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_only'
