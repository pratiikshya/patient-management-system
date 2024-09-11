# patient/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PatientRegistrationForm(UserCreationForm):
    medical_history = forms.CharField(widget=forms.Textarea, required=True)
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    
       # Custom username validator
    username = forms.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w\s@.+-]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
            )
        ]
    )
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'medical_history']
        
    def save(self, commit=True):
        user = super().save(commit)
        # Additional logic can go here if needed
        return user    