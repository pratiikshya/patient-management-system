from django.shortcuts import render, redirect
from .forms import PatientRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Patient, Doctor

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

            if role == 'patient':
                Patient.objects.create(user=user)
            elif role == 'doctor':
                Doctor.objects.create(user=user)

            # Save the user
            # Add user to 'Patient' group
            # group, created = Group.objects.get_or_create(name='Patient')
            # user.groups.add(group)
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
       return render(request, 'patient_dashboard.html', {'patient': patient})
   except Patient.DoesNotExist:
       
        try:
            doctor = Doctor.objects.get(user=request.user)
            return render(request, 'doctor_dashboard.html', {'doctor': doctor})
        except Doctor.DoesNotExist:
            
            return render(request, 'dashboard.html', {'message': 'No data available.'})