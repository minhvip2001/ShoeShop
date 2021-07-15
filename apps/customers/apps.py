from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'apps.customers'

    def ready(self):
        import apps.customers.signals
