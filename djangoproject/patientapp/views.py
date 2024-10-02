from venv import logger
from xml.dom.minidom import Document
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PatientRegistrationForm, DocumentUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Patient, Doctor, UploadedDocument
from django.contrib import messages
from django.conf import settings
import os
#for api views
from rest_framework import viewsets
from .serializers import PatientSerializer, UploadedDocumentSerializer
#for image sacnning and ocr
import pytesseract
from PIL import Image

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UploadedDocumentViewSet(viewsets.ModelViewSet):
    queryset = UploadedDocument.objects.all()
    serializer_class = UploadedDocumentSerializer

def landing_page(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Doctor').exists():
            return redirect('doctor_dashboard')
        elif request.user.groups.filter(name='Patient').exists():
            return redirect('patient_dashboard')
    return render(request, "patientapp/landing_page.html")


def patient_register(request):
    form = PatientRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save() 
            role = form.cleaned_data.get('role')

            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            print("User registered and added to group:", user.username)  # Debugging print
            return redirect('patient_login')  # Redirect after successful registration
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    return render(request, 'patientapp/register.html', {'form': form})

def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')  # Redirect to patient's dashboard
        else:
            print("Invalid login attempt for username:", username)  # Debugging print
            return render(request, "patientapp/patient_login.html", {"error": "Invalid username or password."})
    return render(request, "patientapp/patient_login.html")

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('landing_page')

@login_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user) 
        documents = UploadedDocument.objects.filter(patient=patient)# Fetch the patient instance
        return render(request, 'patientapp/patient_dashboard.html', {'patient': patient, 'documents': documents})
    except Patient.DoesNotExist:
        return render(request, 'patientapp/landing_page.html', {'message': 'No data available.'})
 
@login_required   
def upload_document(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)  # Get the specific patient

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_doc = form.save(commit=False)
            uploaded_doc.patient = patient  # Link the document to the patient
            uploaded_doc.save()

            file_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_doc.document))
            logger.debug(f'File path for uploaded document: {file_path}')
            if uploaded_doc.document.name.endswith(('.png', '.jpg', '.jpeg')):
                try:
                    image = Image.open(file_path)
                    extracted_text = pytesseract.image_to_string(image)
                    logger.debug(f'Extracted text: {extracted_text}')

                    # Save the extracted text to the model
                    uploaded_doc.extracted_text = extracted_text
                    uploaded_doc.save()
                except Exception as e:
                    logger.error(f'Error during OCR processing: {e}')
                    
            return redirect('patient_dashboard')
    else:
        form = DocumentUploadForm()
    return render(request, 'patientapp/upload.html', {'form': form, 'patient': patient})

def scan_document(request, patient_id):
    """
    Simulates a scanning feature where a document (image) is processed as if it's scanned.
    """
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    if request.method == 'POST':
        # Simulate scanning by uploading a file and processing it (as in the upload view)
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            scanned_doc = form.save(commit=False)
            scanned_doc.patient = patient
            scanned_doc.save()

            # Perform OCR if it's an image file (e.g., PNG or JPEG)
            file_path = os.path.join(settings.MEDIA_ROOT, str(scanned_doc.document))
            if scanned_doc.document.name.endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(image)

                # Save the extracted text in the document
                scanned_doc.extracted_text = extracted_text
                scanned_doc.save()

            return redirect('scan_success')
    else:
        form = DocumentUploadForm()

    return render(request, 'scan.html', {'form': form, 'patient': patient})

# Success pages for both upload and scanning
def upload_success(request):
    return render(request, 'success.html', {'message': 'Document uploaded successfully!'})

def scan_success(request):
    return render(request, 'success.html', {'message': 'Document scanned and processed successfully!'})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, patient=request.user.patient)
    document.delete()  # This will also delete the associated file in storage due to the model's delete method.
    return redirect('patient_dashboard')  # Redirect back to the dashboard after deletion

@login_required
def view_extracted_text(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, patient=request.user.patient)
    
    return render(request, 'patientapp/extracted_text.html', {'document': document})   