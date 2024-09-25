import uuid
from django.db import models
from django.contrib.auth.models import User

from doctorapp.models import Doctor # type: ignore


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank= True) 
    patient_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)# Link to the User model
    medical_history = models.TextField(default="", blank=True)  # Store medical history
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Patient Profile"
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient} - {self.appointment_date}"
    
    
class UploadedDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient model
    document = models.FileField(upload_to='documents/')  # Stores file path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto-save upload timestamp
    extracted_text = models.TextField(blank=True, null=True)  # To store OCR results
    report_date = models.DateField(blank=True, null=True)  # Optional field for report date

    def __str__(self):
        return f"Document for {self.patient.user.username}"
    
    
