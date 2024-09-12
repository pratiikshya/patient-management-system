from django.urls import path
from .views import logout_view
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing page
    path('register/', views.patient_register, name='patient_register'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', logout_view, name='logout'),
]