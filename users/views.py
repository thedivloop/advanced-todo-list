from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, 'users/index.html')

def login(request):
  return render(request, 'users/login.html')

def register(request):
  return render(request, 'users/register.html')