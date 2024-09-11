# doctor/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DoctorRegistrationForm(UserCreationForm):
    specialty = forms.CharField(max_length=100, required=True)
    license_number = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'specialty', 'license_number']