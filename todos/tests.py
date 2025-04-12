from datetime import date
from django.test import TestCase
from django.apps import apps
from .forms import NewTodoForm, UpdateTodoForm
from .models import Todo
from unittest import skip
from django.urls import reverse
from todos.apps import TodosConfig

app_name = 'todos'

class TodosAppConfigTest(TestCase):

  def test_todos_app_config(self):
    app_config = apps.get_app_config(app_name)
    assert isinstance(app_config, TodosConfig)
    assert app_config.name == app_name

# @skip("Skipping this test temporarily")
class TodosModelTest(TestCase):
  def test_todos_model_exists(self):
    todos = Todo.objects.count()

    self.assertEqual(todos,0)

  def test_mode_has_string_representation(self):
    todo = Todo.objects.create(title='First todo')

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
    )
    self.assertEqual(todo.title, "Test Task")
    self.assertEqual(todo.description, "Test description")
    self.assertEqual(todo.due_date, date(2025, 5, 1))
    self.assertEqual(todo.priority, "High")
    self.assertEqual(todo.status, "Pending")

# @skip("Skipping this test temporarily")
class IndexPageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(title='First todo')

  def test_index_page_returns_correct_response(self):
    response = self.client.get(f'/{app_name}/')

    self.assertTemplateUsed(response, 'todos/index.html')
    self.assertEqual(response.status_code, 200)

  def test_index_page_has_todos(self):
    response = self.client.get(f'/{app_name}/')

    self.assertContains(response, self.todo.title)

# @skip("Skipping this test temporarily")
class DetailPageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(title='First todo', description='The description')
    self.todo2 = Todo.objects.create(title='Second todo', description='The description')

  def test_detail_page_returns_correct_response(self):
    response = self.client.get(f'/{app_name}/{self.todo.id}/')

    self.assertTemplateUsed(response, 'todos/detail.html')
    self.assertEqual(response.status_code, 200)

  def test_detail_page_has_correct_content(self):
    response = self.client.get(f'/{app_name}/{self.todo.id}/')

    self.assertContains(response, self.todo.title)
    self.assertContains(response, self.todo.description)
    self.assertNotContains(response, self.todo2.title)

# @skip("Skipping this test temporarily")
class NewPageTest(TestCase):
  def setUp(self):
    self.url = f'/{app_name}/new/'
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
    self.assertRedirects(response, expected_url=f'/{app_name}/')
    self.assertEqual(Todo.objects.count(), 1)

# @skip("Skipping this test temporarily")
class UpdatePageTest(TestCase):
  def setUp(self):
    # self.form = UpdateTodoForm
    self.todo = Todo.objects.create(title='Original Title',
                                    description='Original Description',
                                    priority='Medium',
                                    status='Pending',)
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

  # # def test_form_can_be_valid(self):
  # #   self.assertTrue(issubclass(self.form, UpdateTodoForm))
  # #   self.assertTrue('title' in self.form.Meta.fields)
  # #   self.assertTrue('description' in self.form.Meta.fields)
  
  # #   form = self.form({
  # #     'title': 'The title',
  # #     'description': 'The description',
  # #     'priority': 'Medium',
  # #     'status': 'Pending',
  # #   }, instance=self.todo)

  # #   self.assertTrue(form.is_valid())
  # #   form.save()
  # #   self.assertEqual(Todo.objects.get(pk=self.todo.pk).title, 'The title')

  # # def test_form_can_be_invalid(self):
  # #   form = self.form({
  # #     'title': '',
  # #     'description': 'The description'
  # #   }, instance=self.todo)

  # #   self.assertFalse(form.is_valid())

  # # def test_update_page_form_rendering(self):
  # #   response = self.client.get(f'/{app_name}/{self.todo.pk}/update/')

  # #   self.assertContains(response, '<form')
  # #   self.assertContains(response, 'csrfmiddlewaretoken')
  # #   self.assertContains(response, '<label for')

  #   # Test invalid form

  #   response = self.client.post(f'/{app_name}/{self.todo.pk}/update/', {
  #     'id': self.todo.pk,
  #     'title': '',
  #     'description': 'The description'
  #   }, instance = self.todo)


  #   self.assertContains(response,'<ul class="errorlist"')
  #   self.assertContains(response,'This field is required.')

  #   # test valid form

  #   response = self.client.post(f'/{app_name}/{self.todo.pk}/update/',{
  #     'title': 'The title',
  #     'description': 'The description'
  #   })

  #   self.assertRedirects(response, expected_url=f'/{app_name}/')

  #   self.assertEqual(Todo.objects.count(), 1)
  #   self.assertEqual(Todo.objects.get(pk=self.todo.pk).title, 'The title')

# @skip("Skipping this test temporarily")
class DeletePageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(
        title='Test Todo',
        description='This is a test todo item',
        priority='Medium',
        status='Pending'
        )
    self.url = reverse('todos:delete', args=[self.todo.id])
    self.invalid_data = {'confirm': 'no'}
    self.valid_data = {'confirm': 'yes'}

  def test_delete_page_returns_correct_response(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'todos/delete.html')

  def test_delete_with_valid_data_redirects(self):
    response = self.client.post(self.url, self.valid_data)
    self.assertRedirects(response, reverse('todos:index'))
    self.assertEqual(Todo.objects.count(), 0)

  def test_delete_with_invalid_data_redirects(self):
    response = self.client.post(self.url, self.invalid_data)  
    self.assertRedirects(response, reverse('todos:index')) 
    self.assertEqual(Todo.objects.count(), 1)
