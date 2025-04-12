from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .forms import NewTodoForm, UpdateTodoForm
from .models import Todo

@login_required
def index(request):
  todos = Todo.objects.filter(user=request.user)
  return render(request, 'todos/index.html', {'todos': todos, 'current_path': request.path})

@login_required
def detail(request, pk):
  todo = Todo.objects.get(pk=pk)
  return render(request, 'todos/detail.html', {'todo': todo})

@login_required
def new(request):
  if request.method == 'POST':
    form = NewTodoForm(request.POST)
    if form.is_valid():
      todo = form.save(commit=False)
      todo.user = request.user
      todo.save()
      return redirect("todos:index")
  else:
    form = NewTodoForm()
  return render(request, 'todos/new.html', {'form' : form})

@login_required
def update(request,pk):
  todo = Todo.objects.get(pk=pk)
  if request.method== 'POST':
    form = UpdateTodoForm(request.POST, instance=todo)

    if form.is_valid():
      if todo.user != request.user:
        return HttpResponseForbidden("You cannot update this Todo")
      todo = form.save(commit=False)
      todo.user = request.user
      todo.save()
      return redirect("todos:index")
  else:
    form = UpdateTodoForm(instance=todo)
  return render(request, 'todos/update.html', { 'form' : form })

@login_required
def delete(request,pk):
  todo = get_object_or_404(Todo, pk=pk)
  if request.method == 'POST':
    is_confirmed = request.POST.get('confirm', '').lower() == 'yes'
    if is_confirmed:
      if todo.user != request.user:
        return HttpResponseForbidden("You cannot delete this Todo")
      todo.delete()
    return redirect('todos:index')
  return render(request, 'todos/delete.html', {'todo': todo})