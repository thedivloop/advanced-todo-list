from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods

from .forms import NewTodoForm, UpdateTodoForm, TaskGroupForm
from .models import Todo, TaskGroup

from django.utils import timezone

@login_required
def index(request):
  todos = Todo.objects.filter(user=request.user).order_by('-created_at')
  # Filter by group if specified
  group_filter = request.GET.get('group')
  if group_filter:
    if group_filter == 'none':
      todos = todos.filter(group__isnull=True)
    else:
      todos = todos.filter(group_id=group_filter)
  
  todos = todos.order_by('-created_at')

  # Get all groups for filter dropdown
  groups = TaskGroup.objects.filter(user=request.user)

  return render(request, 'todos/index.html', {
      'todos': todos,
      'groups': groups,
      'current_path': request.path,
      'today': timezone.now().date(),
      'selected_group': group_filter
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
    form = NewTodoForm(user=request.user)
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
    form = UpdateTodoForm(instance=todo, user=request.user)
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

@login_required
def groups_list(request):
  groups = TaskGroup.objects.filter(user=request.user)
  return render(request, 'todos/groups_list.html', {'groups': groups})


@login_required
def create_group(request):
  """Create a new task group"""
  if request.method == 'POST':
    form = TaskGroupForm(request.POST, user=request.user)
    if form.is_valid():
      group = form.save(commit=False)
      group.user = request.user
      group.save()
      return redirect('todos:groups_list')
  else:
    form = TaskGroupForm(user=request.user)

  return render(request, 'todos/create_group.html', {'form': form})

@login_required
def group_detail(request, pk):
  group = get_object_or_404(TaskGroup, pk=pk, user=request.user)
  todos = group.todos.filter(user=request.user).order_by('-created_at')
  return render(request, 'todos/group_detail.html', {'group': group, 'todos': todos})

@login_required
def update_group(request, pk):
  group = get_object_or_404(TaskGroup, pk=pk, user=request.user)
  if request.method == 'POST':
    form = TaskGroupForm(request.POST, instance=group, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('todos:groups_list')
  else:
    form = TaskGroupForm(instance=group, user=request.user)
  
  return render(request, 'todos/update_group.html', {'form': form, 'group': group})

@login_required
def delete_group(request, pk):
  group = get_object_or_404(TaskGroup, pk=pk, user=request.user)
  if request.method == 'POST':
    is_confirmed = request.POST.get('confirm', '').lower() == 'yes'
    if is_confirmed:
      group.delete()
    return redirect('todos:groups_list')
  
  return render(request, 'todos/delete_group.html', {'group': group})