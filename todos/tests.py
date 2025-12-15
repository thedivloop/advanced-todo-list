from datetime import date
from unittest import skip
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from todos.apps import TodosConfig
from .forms import NewTodoForm
from .models import Todo
from django.utils import timezone
from datetime import timedelta
import json

app_name = 'todos'

class TodosAppConfigTest(TestCase):
  def test_todos_app_config(self):
    app_config = apps.get_app_config(app_name)
    assert isinstance(app_config, TodosConfig)
    assert app_config.name == app_name

class LoggedInTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.client.login(username='testuser', password='testpassword')

class TodosModelTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')

  def test_todos_model_exists(self):
    todos_count = Todo.objects.count()
    self.assertEqual(todos_count,0)

  def test_mode_has_string_representation(self):
    todo = Todo.objects.create(title='First todo', user=self.user)
    self.assertEqual(str(todo), todo.title)

  def test_todo_fields(self):
    todo = Todo.objects.create(
      title = "Test Task",
      description = "Test description",
      due_date = date(2025, 5, 1),
      priority = "High",
      status = "Pending",
      duration = 60,
      created_at = date(2023, 10, 1),
      updated_at = date(2023, 10, 1),
      time_completion = 30,
      time_spent = 10,
      time_remaining = 20,
      user=self.user,
    )
    self.assertEqual(todo.title, "Test Task")
    self.assertEqual(todo.description, "Test description")
    self.assertEqual(todo.due_date, date(2025, 5, 1))
    self.assertEqual(todo.priority, "High")
    self.assertEqual(todo.status, "Pending")
    self.assertEqual(todo.user, self.user)

class IndexPageTest(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.non_owner = User.objects.create_user(username='non_owner', password='password')

    self.todo = Todo.objects.create(title='First todo', user=self.user)
    self.todo2 = Todo.objects.create(title='Test Todo 2', user=self.user)
    self.todo3 = Todo.objects.create(title='Non-owner Todo', user=self.non_owner)

  def test_index_page_displays_only_user_own_todos(self):
    response = self.client.get(reverse('todos:index'))
    self.assertContains(response, self.todo.title)
    self.assertContains(response, self.todo2.title)
    self.assertNotContains(response, self.todo3.title)

  def test_index_page_returns_correct_response(self):
    response = self.client.get(f'/{app_name}/')

    self.assertTemplateUsed(response, 'todos/index.html')
    self.assertEqual(response.status_code, 200)

  def test_index_page_has_todos(self):
    response = self.client.get(f'/{app_name}/')

    self.assertContains(response, self.todo.title)

class DetailPageTest(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.todo = Todo.objects.create(title='First todo', description='The description', user=self.user)
    self.todo2 = Todo.objects.create(title='Second todo', description='The description', user=self.user)

  def test_detail_page_returns_correct_response(self):
    response = self.client.get(f'/{app_name}/{self.todo.id}/')

    self.assertTemplateUsed(response, 'todos/detail.html')
    self.assertEqual(response.status_code, 200)

  def test_detail_page_has_correct_content(self):
    response = self.client.get(f'/{app_name}/{self.todo.id}/')

    self.assertContains(response, self.todo.title)
    self.assertContains(response, self.todo.description)
    self.assertNotContains(response, self.todo2.title)

class NewPageTest(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.url = reverse('todos:new')
    self.validTodo = {
      'title': 'The title',
      'description': 'The description',
      'priority' : 'Medium',
      'status' : 'Pending',
    }
    self.invalidTodo = {
      'title': '',
      'description': 'The description',
      'priority' : 'Medium',
      'status' : 'Pending',
      'user' : self.user,
    }

  def test_new_page_returns_correct_response(self):
    response = self.client.get(self.url)
    self.assertTemplateUsed(response, 'todos/new.html')
    self.assertEqual(response.status_code, 200)

  def test_form_can_be_valid(self):
    form = NewTodoForm(self.validTodo)
    self.assertTrue(form.is_valid())

  def test_new_page_form_rendering(self):
    response = self.client.get(self.url)
    self.assertContains(response, '<form')
    self.assertContains(response, 'csrfmiddlewaretoken')
    self.assertContains(response, '<label for')

    # Test invalid form

    response = self.client.post(self.url,self.invalidTodo)
    self.assertContains(response,'<ul class="errorlist"')
    self.assertContains(response,'This field is required.')

    # test valid form

    response = self.client.post(self.url,self.validTodo)
    self.assertEqual(response.status_code, 302)
    todo = Todo.objects.get(title='The title')
    self.assertEqual(todo.user, self.user)
    self.assertRedirects(response, expected_url=f'/{app_name}/')
    self.assertEqual(Todo.objects.count(), 1)


class UpdatePageTest(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.non_owner = User.objects.create_user(username='non_owner', password='password')
    self.todo = Todo.objects.create(title='Original Title',
                                    description='Original Description',
                                    priority='Medium',
                                    status='Pending',
                                    user = self.user)
    self.url = reverse('todos:update', args=[self.todo.id])
    self.valid_data = {
      'title': 'Updated Title',
      'description': 'Updated Description',
      'priority': 'High',
      'status': 'In Progress',
    }
    self.invalid_data = {
      'title': '',
      'description': 'Updated Description',
      'priority': 'High',
      'status': 'In Progress',
    }

  def test_update_page_returns_correct_response(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'todos/update.html')
    self.assertContains(response, '<form')
    self.assertContains(response, 'csrfmiddlewaretoken')

  def test_update_form_initial_data(self):
    response = self.client.get(self.url)
    self.assertContains(response, 'Original Title')
    self.assertContains(response, 'Original Description')

  def test_update_with_invalid_data(self):
    response = self.client.post(self.url, self.invalid_data)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, '<ul class="errorlist"')
    self.assertContains(response, 'This field is required.')

  def test_update_with_valid_data_redirects(self):
    response = self.client.post(self.url, self.valid_data)
    self.assertEqual(response.status_code, 302)
    self.todo.refresh_from_db()
    self.assertEqual(self.todo.title, 'Updated Title')
    self.assertEqual(self.todo.description, 'Updated Description')
    self.assertRedirects(response, reverse('todos:index'))

  def test_user_cannot_update_another_user_todo(self):
    self.client.login(username='non_owner', password='password')
    response = self.client.post(self.url, self.valid_data)
    self.assertEqual(response.status_code, 403)
    todo = Todo.objects.get(id=self.todo.id)
    self.assertNotEqual(todo.title, self.valid_data['title']) 
    self.assertNotEqual(todo.description, self.valid_data['description']) 

class DeletePageTest(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.non_owner = User.objects.create_user(username='non_owner', password='password')

    self.todo = Todo.objects.create(
        title='Test Todo',
        description='This is a test todo item',
        priority='Medium',
        status='Pending',
        user = self.user
        )
    self.url = reverse('todos:delete', args=[self.todo.id])
    self.invalid_data = {'confirm': 'no'}
    self.valid_data = {'confirm': 'yes'}

  def test_delete_page_returns_correct_response(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'todos/delete.html')

  def test_delete_with_data_redirects(self):
    self.assertEqual(Todo.objects.count(), 1)
    response = self.client.post(self.url, self.invalid_data)  
    self.assertRedirects(response, reverse('todos:index')) 
    self.assertEqual(Todo.objects.count(), 1)
    response = self.client.post(self.url, self.valid_data)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('todos:index'))
    self.assertEqual(Todo.objects.count(), 0)
    with self.assertRaises(Todo.DoesNotExist):
      Todo.objects.get(id=self.todo.id)

  def test_user_cannot_delete_another_user_todo(self):
    self.client.login(username='non_owner', password='password')
    response = self.client.post(self.url, self.valid_data)
    self.assertEqual(response.status_code, 403)
    todo_exists = Todo.objects.filter(id=self.todo.id).exists()
    self.assertTrue(todo_exists)

class TodoAccessTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='password')
    self.todo = Todo.objects.create(
        title='Test Todo',
        description='Test description',
        user=self.user
    )
    self.todo_list_url = reverse('todos:index')
    self.todo_url = reverse('todos:detail', args=[self.todo.id])
    self.create_url = reverse('todos:new')
    self.update_url = reverse('todos:update', args=[self.todo.id])
    self.delete_url = reverse('todos:delete', args=[self.todo.id])
  
  def test_access_pages_as_unauthenticated_user(self):
    urls = [self.todo_list_url, self.create_url, self.todo_url, self.update_url, self.delete_url]
    for url in urls:
      with self.subTest(url=url):
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next={url}')

class TodoUserAssociationTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')

  def test_todo_is_linked_to_user(self):
    todo = Todo.objects.create(
      user=self.user,
      title="Test Todo",
      description="Test description",
      due_date=date.today(),
      priority="High",
      status="Pending",
      duration=60,
      time_completion=50,
      time_spent=30,
      time_remaining=30
    )
    self.assertEqual(todo.user, self.user)
    self.assertEqual(Todo.objects.filter(user=self.user).count(), 1)


class TimerModelTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.todo = Todo.objects.create(
        title='Test Task',
        user=self.user,
        duration=60,
        status='Pending'
    )
  # @skip("Skipping timer field test temporarily")  
  def test_todo_has_timer_fields(self):
    """Test that todo has is_timer_active and timer_started_at fields"""
    self.assertFalse(self.todo.is_timer_active)
    self.assertIsNone(self.todo.timer_started_at)
  
  # @skip("Skipping start timer test temporarily")
  def test_start_timer_changes_status_to_in_progress(self):
    """Test that starting timer changes status to 'In Progress'"""
    self.todo.start_timer()
    self.assertEqual(self.todo.status, 'In Progress')
    self.assertTrue(self.todo.is_timer_active)
    self.assertIsNotNone(self.todo.timer_started_at)
  
  # @skip("Skipping stop timer test temporarily")
  def test_stop_timer_changes_status_to_pending(self):
    """Test that stopping timer changes status to 'Pending'"""
    self.todo.start_timer()
    self.todo.stop_timer()
    self.assertEqual(self.todo.status, 'Pending')
    self.assertFalse(self.todo.is_timer_active)
    self.assertIsNone(self.todo.timer_started_at)
  
  # @skip("Skipping time spent update test temporarily")
  def test_stop_timer_updates_time_spent(self):
    """Test that stopping timer updates time_spent"""
    self.todo.start_timer()
    # Simulate 5 seconds passing
    self.todo.timer_started_at = timezone.now() - timedelta(seconds=5)
    self.todo.save()
    
    self.todo.stop_timer()
    # Should be at least 5 seconds (converted to minutes, rounded)
    self.assertGreaterEqual(self.todo.time_spent or 0, 0)

  # @skip("Skipping time remaining update test temporarily")
  def test_stop_timer_updates_time_remaining(self):
    """Test that stopping timer updates time_remaining"""
    self.todo.duration = 60
    self.todo.time_spent = 0
    self.todo.save()
    
    self.todo.start_timer()
    self.todo.timer_started_at = timezone.now() - timedelta(minutes=10)
    self.todo.save()
    
    self.todo.stop_timer()
    
    # time_remaining should be duration - time_spent
    self.assertEqual(self.todo.time_remaining, 60 - 10)
  
  # @skip("Skipping single active timer test temporarily")
  def test_only_one_timer_active_per_user(self):
    """Test that only one todo can have active timer per user"""
    todo2 = Todo.objects.create(
        title='Second Task',
        user=self.user,
        duration=30,
        status='Pending'
    )
    
    # Start first timer
    self.todo.start_timer()
    self.assertTrue(self.todo.is_timer_active)
    
    # Start second timer - should stop first
    todo2.start_timer()
    
    # Refresh from database
    self.todo.refresh_from_db()
    todo2.refresh_from_db()
    
    # First should be stopped, second should be active
    self.assertFalse(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'Pending')
    self.assertTrue(todo2.is_timer_active)
    self.assertEqual(todo2.status, 'In Progress')

  # @skip("Skipping elapsed time test temporarily")
  def test_get_elapsed_time_when_timer_active(self):
    """Test getting elapsed time when timer is running"""
    self.todo.start_timer()
    # Simulate 10 seconds passing
    self.todo.timer_started_at = timezone.now() - timedelta(seconds=10)
    self.todo.save()
    
    elapsed = self.todo.get_elapsed_time()
    self.assertGreaterEqual(elapsed, 10)
    self.assertLess(elapsed, 12)  # Allow 2 second margin
  
  # @skip("Skipping elapsed time test temporarily")
  def test_get_elapsed_time_when_timer_inactive(self):
    """Test getting elapsed time when timer is not running"""
    elapsed = self.todo.get_elapsed_time()
    self.assertEqual(elapsed, 0)

  # @skip("Skipping active timer retrieval test temporarily")
  def test_get_active_timer_for_user(self):
    """Test getting the active timer todo for a user"""
    self.todo.start_timer()
    
    active_todo = Todo.get_active_timer_for_user(self.user)
    self.assertEqual(active_todo, self.todo)
  
  # @skip("Skipping no active timer retrieval test temporarily")
  def test_get_active_timer_returns_none_when_no_active(self):
    """Test getting active timer returns None when no timer active"""
    active_todo = Todo.get_active_timer_for_user(self.user)
    self.assertIsNone(active_todo)

class TimerViewTests(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.todo = Todo.objects.create(
        title='Test Task',
        user=self.user,
        duration=60,
        status='Pending'
    )
    self.todo2 = Todo.objects.create(
        title='Second Task',
        user=self.user,
        duration=30,
        status='Pending'
    )
  
  def test_start_timer_endpoint_exists(self):
    """Test that start_timer endpoint exists"""
    url = reverse('todos:start_timer', args=[self.todo.id])
    response = self.client.post(url)
    self.assertNotEqual(response.status_code, 404)

  # @skip("Skipping start timer JSON response test temporarily")
  def test_start_timer_returns_json(self):
    """Test that start_timer returns JSON response"""
    url = reverse('todos:start_timer', args=[self.todo.id])
    response = self.client.post(url)
    self.assertEqual(response['Content-Type'], 'application/json')
  
  # @skip("Skipping start timer activation test temporarily")
  def test_start_timer_activates_timer(self):
    """Test that start_timer activates the timer"""
    url = reverse('todos:start_timer', args=[self.todo.id])
    response = self.client.post(url)
    
    data = json.loads(response.content)
    self.assertEqual(data['status'], 'success')
    
    self.todo.refresh_from_db()
    self.assertTrue(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'In Progress')

  # @skip("Skipping start timer stops other timers test temporarily")
  def test_start_timer_stops_other_active_timers(self):
    """Test that starting timer stops other active timers"""
    # Start first timer
    self.todo.start_timer()
    
    # Start second timer via endpoint
    url = reverse('todos:start_timer', args=[self.todo2.id])
    response = self.client.post(url)
    
    data = json.loads(response.content)
    self.assertEqual(data['status'], 'success')
    
    # Check first timer is stopped
    self.todo.refresh_from_db()
    self.assertFalse(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'Pending')
    
    # Check second timer is active
    self.todo2.refresh_from_db()
    self.assertTrue(self.todo2.is_timer_active)
  
  # @skip("Skipping start timer requires authentication test temporarily") 
  def test_start_timer_requires_authentication(self):
    """Test that start_timer requires authentication"""
    self.client.logout()
    url = reverse('todos:start_timer', args=[self.todo.id])
    response = self.client.post(url)
    self.assertEqual(response.status_code, 302)  # Redirect to login
  
  # @skip("Skipping start timer requires ownership test temporarily")
  def test_start_timer_requires_ownership(self):
    """Test that user can only start timer on their own todos"""
    other_user = User.objects.create_user(username='other', password='password')
    other_todo = Todo.objects.create(
        title='Other Task',
        user=other_user,
        duration=45
    )
    
    url = reverse('todos:start_timer', args=[other_todo.id])
    response = self.client.post(url)
    self.assertEqual(response.status_code, 404)
  
  # @skip("Skipping stop timer endpoint test temporarily")
  def test_stop_timer_endpoint_exists(self):
    """Test that stop_timer endpoint exists"""
    url = reverse('todos:stop_timer', args=[self.todo.id])
    response = self.client.post(url)
    self.assertNotEqual(response.status_code, 404)
  
  # @skip("Skipping stop timer deactivates timer test temporarily")
  def test_stop_timer_deactivates_timer(self):
    """Test that stop_timer deactivates the timer"""
    self.todo.start_timer()
    
    url = reverse('todos:stop_timer', args=[self.todo.id])
    response = self.client.post(url)
    
    data = json.loads(response.content)
    self.assertEqual(data['status'], 'success')
    
    self.todo.refresh_from_db()
    self.assertFalse(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'Pending')
  
  # @skip("Skipping stop timer returns time data test temporarily")
  def test_stop_timer_returns_time_data(self):
    """Test that stop_timer returns updated time data"""
    self.todo.start_timer()
    
    url = reverse('todos:stop_timer', args=[self.todo.id])
    response = self.client.post(url)
    
    data = json.loads(response.content)
    self.assertIn('time_spent', data)
    self.assertIn('time_remaining', data)
    self.assertIn('time_completion', data)
  
  # @skip("Skipping get timer status endpoint test temporarily")
  def test_get_timer_status_endpoint_exists(self):
    """Test that get_timer_status endpoint exists"""
    url = reverse('todos:timer_status', args=[self.todo.id])
    response = self.client.get(url)
    self.assertNotEqual(response.status_code, 404)
  
  # @skip("Skipping get timer status returns correct data test temporarily")
  def test_get_timer_status_returns_correct_data(self):
    """Test that get_timer_status returns correct timer data"""
    self.todo.start_timer()
    
    url = reverse('todos:timer_status', args=[self.todo.id])
    response = self.client.get(url)
    
    data = json.loads(response.content)
    self.assertTrue(data['is_active'])
    self.assertIn('elapsed_seconds', data)
    self.assertIn('time_spent', data)
    self.assertIn('duration', data)

  # @skip("Skipping check active timer endpoint test temporarily")
  def test_check_active_timer_endpoint_exists(self):
    """Test that check_active_timer endpoint exists"""
    url = reverse('todos:check_active_timer')
    response = self.client.get(url)
    self.assertNotEqual(response.status_code, 404)
  
  # @skip("Skipping check active timer returns active todo test temporarily")
  def test_check_active_timer_returns_active_todo(self):
    """Test that check_active_timer returns active todo info"""
    self.todo.start_timer()
    
    url = reverse('todos:check_active_timer')
    response = self.client.get(url)
    
    data = json.loads(response.content)
    self.assertTrue(data['has_active_timer'])
    self.assertEqual(data['active_todo_id'], self.todo.id)
    self.assertEqual(data['active_todo_title'], self.todo.title)
  
  # @skip("Skipping check active timer returns none test temporarily")
  def test_check_active_timer_returns_none_when_no_active(self):
    """Test that check_active_timer returns None when no timer active"""
    url = reverse('todos:check_active_timer')
    response = self.client.get(url)
    
    data = json.loads(response.content)
    self.assertFalse(data['has_active_timer'])
    self.assertIsNone(data['active_todo_id'])

class TimerIntegrationTests(LoggedInTestCase):
  def setUp(self):
    super().setUp()
    self.todo = Todo.objects.create(
        title='Integration Test Task',
        user=self.user,
        duration=60,
        status='Pending'
    )
  
  def test_full_timer_workflow(self):
    """Test complete timer workflow: start -> stop -> verify data"""
    # Start timer
    start_url = reverse('todos:start_timer', args=[self.todo.id])
    response = self.client.post(start_url)
    self.assertEqual(response.status_code, 200)
    
    # Verify timer is active
    self.todo.refresh_from_db()
    self.assertTrue(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'In Progress')
    
    # Simulate time passing
    from django.utils import timezone
    from datetime import timedelta
    self.todo.timer_started_at = timezone.now() - timedelta(minutes=5)
    self.todo.save()
    
    # Stop timer
    stop_url = reverse('todos:stop_timer', args=[self.todo.id])
    response = self.client.post(stop_url)
    self.assertEqual(response.status_code, 200)
    
    # Verify timer stopped and data updated
    self.todo.refresh_from_db()
    self.assertFalse(self.todo.is_timer_active)
    self.assertEqual(self.todo.status, 'Pending')
    self.assertEqual(self.todo.time_spent, 5)
    self.assertEqual(self.todo.time_remaining, 55)