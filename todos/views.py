from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from .forms import NewTodoForm, UpdateTodoForm
from .models import Todo

from django.utils import timezone

@login_required
def index(request):
  todos = Todo.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'todos/index.html', {
      'todos': todos,
      'current_path': request.path,
      'today': timezone.now().date()
  })

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

@login_required
@require_POST
def start_timer(request, pk):
  """Start timer for a specific todo"""
  todo = get_object_or_404(Todo, pk=pk, user=request.user)
  todo.start_timer()

  return JsonResponse({
        'status': 'success',
        'message': 'Timer started',
        'is_active': True,
        'todo_id': todo.id
    })

@login_required
@require_POST
def stop_timer(request, pk):
  """Stop timer for a specific todo"""
  todo = get_object_or_404(Todo, pk=pk, user=request.user)
  todo.stop_timer()
  
  return JsonResponse({
      'status': 'success',
      'message': 'Timer stopped',
      'time_spent': todo.time_spent or 0,
      'time_remaining': todo.time_remaining or 0,
      'time_completion': todo.time_completion or 0
  })

@login_required
@require_http_methods(["GET"])
def get_timer_status(request, pk):
  """Get current timer status for a todo"""
  todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
  return JsonResponse({
      'is_active': todo.is_timer_active,
      'elapsed_seconds': todo.get_elapsed_time(),
      'time_spent': todo.time_spent or 0,
      'time_remaining': todo.time_remaining or 0,
      'duration': todo.duration or 0,
      'status': todo.status
  })

@login_required
@require_http_methods(["GET"])
def check_active_timer(request):
  """Check if user has any active timer"""
  active_todo = Todo.get_active_timer_for_user(request.user)
    
  if active_todo:
    return JsonResponse({
        'has_active_timer': True,
        'active_todo_id': active_todo.id,
        'active_todo_title': active_todo.title,
        'elapsed_seconds': active_todo.get_elapsed_time()
    })
  else:
    return JsonResponse({
        'has_active_timer': False,
        'active_todo_id': None,
        'active_todo_title': None
    })