from rest_framework import serializers
from .models import Patient, UploadedDocument

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['user', 'patient_id', 'medical_history', 'age', 'gender', 'contact_number', 'address']

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['patient', 'document', 'uploaded_at', 'extracted_text' ]