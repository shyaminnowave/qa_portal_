from django.apps import AppConfig


class TestcaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.testcases'

    def ready(self) -> None:
        import apps.testcases.signals