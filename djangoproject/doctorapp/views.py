from django.shortcuts import render, redirect
from .forms import DoctorRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def doctor_register(request):
    form = DoctorRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Add user to 'Doctor' group
        group = Group.objects.get(name='Doctor')
        user.groups.add(group)
        return redirect('doctor_login')
    return render(request, 'doctor/register.html', {'form': form})

def doctor_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('doctor_dashboard')  # Redirect to doctor's dashboard
        else:
            return render(request, "doctor/doctor_login.html", {"error": "Invalid username or password."})
    return render(request, "doctor/doctor_login.html")

@login_required
def doctor_dashboard(request):
    return render(request, "doctor/doctor_dashboard.html")