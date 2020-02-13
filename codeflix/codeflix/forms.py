from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Extends the django generic UserCreationForm to get all the fields.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
