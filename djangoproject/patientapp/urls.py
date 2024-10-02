# patientapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import PatientViewSet, UploadedDocumentViewSet

# Define DRF Router for API endpoints
router = DefaultRouter()
router.register(r'patients', PatientViewSet)  # API for patient-related operations
router.register(r'documents', UploadedDocumentViewSet)  # API for document uploads

# URL patterns for both regular views and API routes
urlpatterns = [
    # Regular Django Views (Web-based interaction)
    path('', views.landing_page, name='landing_page'),
    path('register/', views.patient_register, name='patient_register'),
    path('login/', views.patient_login, name='patient_login'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('documents/upload/<uuid:patient_id>/', views.upload_document, name='upload_document'),
    path('documents/scan/<uuid:patient_id>/', views.scan_document, name='scan_document'),
    path('documents/upload/success/', views.upload_success, name='upload_success'),
    path('documents/scan/success/', views.scan_success, name='scan_success'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('extracted-text/<int:document_id>/', views.view_extracted_text, name='view_extracted_text'),

    # API routes from Django REST Framework (DRF)
    path('api/', include(router.urls)),  # Includes all API routes
]
