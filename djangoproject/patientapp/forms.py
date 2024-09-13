# patient/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Patient
class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    medical_history = forms.CharField(widget=forms.Textarea, required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    contact_number = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Enter a valid contact number. It should be between 9 to 15 digits.'
            )
        ]
    )
    address = forms.CharField(widget=forms.Textarea, required=True)
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
        fields = ['username', 'email', 'password1', 'password2', 'age','medical_history', 'role','gender','contact_number', 'address']
        
    def save(self, commit=True):
        user = super().save(commit) 
        if commit:
            patient = Patient.objects.create (
                user=user, 
                medical_history=self.cleaned_data['medical_history'],
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address']
            )
            patient.save()
        # Additional logic can go here if needed
        return user