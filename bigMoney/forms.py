from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    USER_ROLES = [  ("S", "Seller"),
                    ("C", "Customer")]
    role = forms.ChoiceField(choices=USER_ROLES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']