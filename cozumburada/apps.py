from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cozumburada'

    def ready(self):
        import cozumburada.signals
