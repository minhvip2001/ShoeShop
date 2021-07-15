from django.apps import AppConfig


class CheckoutsConfig(AppConfig):
    name = 'apps.checkouts'

    def ready(self):
        import apps.checkouts.signals
