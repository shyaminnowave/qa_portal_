from django.apps import AppConfig


class StbsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stbs'

    # def ready(self) -> None:
    #     import apps.stbs.signals