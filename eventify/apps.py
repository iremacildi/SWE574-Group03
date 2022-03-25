from django.apps import AppConfig
from django.conf import settings

class EventifyConfig(AppConfig):
    name = 'eventify'

    def ready(self):
        import users.signals
        from actstream import registry
        registry.register(settings.AUTH_USER_MODEL, self.get_model('Post'), self.get_model('Service'))