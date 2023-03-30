from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    USER_ROLES = [  ("S", "Seller"),
                    ("C", "Customer")]
    role = forms.ChoiceField(choices=USER_ROLES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['RecipiantName', 'StreetAddress', 'City', 'State', 'zipcode']