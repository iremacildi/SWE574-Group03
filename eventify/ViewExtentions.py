from collections import UserDict
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.http import HttpResponseRedirect
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.detail import (
    BaseDetailView, SingleObjectMixin, SingleObjectTemplateResponseMixin,
)
from django.contrib.auth.models import User
from eventify.models import RegisterService


class OverRideDeletionMixin:
    """Provide the ability to delete objects."""
    success_url = None

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url ='/service/'+str(self.object.id)
        self.object.IsCancelled=True
        users=RegisterService.objects.filter(service_id=self.object.id,approved_register=True)
        for item in users:
            user=User.objects.get(id=item.author_id)
            user.profile.credits+=self.object.duration
            user.profile.reserved-=self.object.duration
            user.save()
            if self.object.paid==True:
                owner=User.objects.get(id=item.owner)
                owner.profile.reserved-=self.object.duration
                self.object.paid==False
                self.object.save()
        self.object.save()        
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

class BaseDeleteView(OverRideDeletionMixin, BaseDetailView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class OverRideDeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    template_name_suffix = '_confirm_cancel'
