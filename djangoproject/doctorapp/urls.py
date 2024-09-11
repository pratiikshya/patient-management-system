from django.urls import path
from .views import doctor_register, doctor_login, doctor_dashboard

urlpatterns = [
    path('register/', doctor_register, name='doctor_register'),
    path('login/', doctor_login, name='doctor_login'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'), 
]