from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget

from .models import Profile


class CodeforcesUserSelectorWidget(ModelSelect2Widget):
    search_fields = [
        'handle__istartswith',
    ]


class CodeforcesUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cfuser']
        widgets = {
            'cfuser': CodeforcesUserSelectorWidget,
        }
        labels = {
            "cfuser": ""
        }


class SignUpForm(UserCreationForm):
    """
    Extends the django generic UserCreationForm to get all the fields.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
