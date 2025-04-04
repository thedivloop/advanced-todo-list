from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import NewTodoForm, UpdateTodoForm
from .models import Todo

# Create your views here.

def index(request):
  todos = Todo.objects.all()
  return render(request, 'todos/index.html', {'todos': todos, 'current_path': request.path})

def detail(request, pk):
  todo = Todo.objects.get(pk=pk)
  return render(request, 'todos/detail.html', {'todo': todo})

def new(request):
  if request.method== 'POST':
    form = NewTodoForm(request.POST)

    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse("index"))
  else:
    form = NewTodoForm()

  return render(request, 'todos/new.html', {'form' : form})

def update(request,pk):
  todo = Todo.objects.get(pk=pk)
  if request.method== 'POST':
    form = UpdateTodoForm(request.POST, instance=todo)

    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse("index"))
  else:
    form = UpdateTodoForm(instance=todo)
  return render(request, 'todos/update.html', { 'form' : form })

def delete(request,pk):
  todo = Todo.objects.get(pk=pk)
  if request.method == 'POST':
    todo.delete()
    return HttpResponseRedirect(reverse("index"))