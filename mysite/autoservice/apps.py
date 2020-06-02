from django.apps import AppConfig


class AutoserviceConfig(AppConfig):
    name = 'autoservice'

    def ready(self):
        from .signals import create_profile, save_profile