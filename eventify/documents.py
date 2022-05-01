# documents.py

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Service

@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'service'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Service
         fields = [
            # 'author',
            'title',
            'eventdate',
            'tempLocation',
            'eventtime',
            'duration',
            'category',
            'capacity',
            # 'location',
            'content',
            'picture',
            'date_posted',
            'paid',
            'isLate',
            'isGiven',
            'IsCancelled',
         ]
         related_models = [Service]