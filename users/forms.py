from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InterestSelection, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2','id']
        exclude = ('id',)

class InterestsForm(forms.ModelForm):

    class Meta:
        model = InterestSelection
        fields = ['user','interest_1', 'interest_2', 'interest_3'] 
        exclude = ('user',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location','image']
