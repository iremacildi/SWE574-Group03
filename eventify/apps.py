from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model

class EventifyConfig(AppConfig):
    name = 'eventify'

    def ready(self):
        import users.signals
        from actstream import registry
        registry.register(get_user_model(), self.get_model('Post'), self.get_model('Service'))