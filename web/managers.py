from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from actstream.managers import ActionManager, stream

class MyActionManager(ActionManager):
    @stream
    def mystream(self, obj, verb='created service', time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb = verb, timestamp__lte = time)