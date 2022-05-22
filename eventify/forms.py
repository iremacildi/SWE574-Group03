from django import forms
from django.forms.widgets import DateInput, TimeInput

from .models import Post,Service


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','duration','eventdate','category','eventtime','location','content','picture','capacity']

        widgets = {
            'title':forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Event Title'}),
            'content':forms.Textarea(attrs={'rows': '5','class': 'form-control','placeholder': 'Event details'}),            
            'eventdate':DateInput(attrs={'type': 'date'}),
            'eventtime':TimeInput(attrs={'type': 'time'}),


        }
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title','duration','eventdate','category','eventtime','location','content','picture','capacity']

        widgets = {
            'title':forms.Textarea(attrs={'rows': '1','class': 'form-control','placeholder': 'Service Title'}),
            'content':forms.Textarea(attrs={'rows': '5','class': 'form-control','placeholder': 'Service details'}),                        
            'eventdate':DateInput(attrs={'type': 'date'}),
            'eventtime':TimeInput(attrs={'type': 'time'}),
        }
