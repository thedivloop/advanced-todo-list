from datetime import date
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from todos.apps import TodosConfig
from unittest import skip
from .forms import NewTodoForm
from .models import Todo

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
    self.todo = Todo.objects.create(title='First todo', user=self.user)

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