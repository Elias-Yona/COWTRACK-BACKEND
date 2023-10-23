from django.apps import AppConfig


class SalesmetricsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salesmetrics'

    def ready(self):
        import salesmetrics.signals
