from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, 'public_frontend/index.html')

def about(request):
  return render(request, 'public_frontend/about.html')

def features(request):
  return render(request, 'public_frontend/features.html')