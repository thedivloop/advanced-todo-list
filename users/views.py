from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
  return render(request, 'users/index.html')

def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return HttpResponseRedirect(reverse("users:dashboard"))
    else:
        return render(request, 'users/login.html', {'form': form})
  user = auth.get_user(request)
  if user.is_authenticated:
    return HttpResponseRedirect(reverse("users:dashboard"))
  return render(request, 'users/login.html', {'form': AuthenticationForm()})

def register_view(request):
  return render(request, 'users/register.html')

@login_required
def dashboard_view(request):
  return render(request, 'users/dashboard.html')

def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("users:login"))

# Create your views here.
"""
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/users.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "users/users.html", { "message": "Logged in" })
        else:
            return render(request, "users/login.html", { "message": "Invalid credentials." })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", { "message": "Logged out." })

"""