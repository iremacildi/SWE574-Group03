from controlcenter import Dashboard, widgets
from eventify.models import Post, Service,Comment,ServiceComment,RegisterEvent,RegisterService as models


class ModelItemList(widgets.ItemList):
    model = models
    list_display = ('pk', 'field')

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )