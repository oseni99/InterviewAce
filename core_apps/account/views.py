from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "account/index.html")


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print(form.errors)
    return render(request, "account/register.html", {"registration_form": form})


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Account is not active, Contact Support")
        else:
            form = AuthenticationForm(request.POST)
            messages.error(request, "Invalid username or password.")
    return render(request, "account/login.html", {"login_form": form})


def logout(request):
    auth_logout(request)
    return redirect("home")


def dashboard(request):
    return render(request, "dashboard.html")
