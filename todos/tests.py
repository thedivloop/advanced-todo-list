from django.test import TestCase

from .forms import NewTodoForm, UpdateTodoForm
from .models import Todo

# Create your tests here.

class TodosModelTest(TestCase):
  def test_todos_model_exists(self):
    todos = Todo.objects.count()

    self.assertEqual(todos,0)

  def test_mode_has_string_representation(self):
    todo = Todo.objects.create(title='First todo')

    self.assertEqual(str(todo), todo.title)

class IndexPageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(title='First todo')

  def test_index_page_returns_correct_response(self):
    response = self.client.get('/')

    self.assertTemplateUsed(response, 'todos/index.html')
    self.assertEqual(response.status_code, 200)

  def test_index_page_has_todos(self):
    response = self.client.get('/')

    self.assertContains(response, self.todo.title)

class DetailPageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(title='First todo', description='The description')
    self.todo2 = Todo.objects.create(title='Second todo', description='The description')

  def test_detail_page_returns_correct_response(self):
    response = self.client.get(f'/{self.todo.id}/')

    self.assertTemplateUsed(response, 'todos/detail.html')
    self.assertEqual(response.status_code, 200)

  def test_detail_page_has_correct_content(self):
    response = self.client.get(f'/{self.todo.id}/')

    self.assertContains(response, self.todo.title)
    self.assertContains(response, self.todo.description)
    self.assertNotContains(response, self.todo2.title)

class NewPageTest(TestCase):
  def setUp(self):
    self.form = NewTodoForm

  def test_new_page_returns_correct_response(self):
    response = self.client.get('/new/')

    self.assertTemplateUsed(response, 'todos/new.html')
    self.assertEqual(response.status_code, 200)

  def test_form_can_be_valid(self):
    self.assertTrue(issubclass(self.form, NewTodoForm))
    self.assertTrue('title' in self.form.Meta.fields)
    self.assertTrue('description' in self.form.Meta.fields)
  
    form = self.form({
      'title': 'The title',
      'description': 'The description'
    })

    self.assertTrue(form.is_valid)

  def test_new_page_form_rendering(self):
    response = self.client.get('/new/')

    self.assertContains(response, '<form')
    self.assertContains(response, 'csrfmiddlewaretoken')
    self.assertContains(response, '<label for')

    # Test invalid form

    response = self.client.post('/new/',{
      'title': '',
      'description': 'The description'
    })


    self.assertContains(response,'<ul class="errorlist">')
    self.assertContains(response,'This field is required.')

    # test valid form

    response = self.client.post('/new/',{
      'title': 'The title',
      'description': 'The description'
    })

    self.assertRedirects(response, expected_url='/')

    self.assertEqual(Todo.objects.count(), 1)

class UpdatePageTest(TestCase):
  def setUp(self):
    self.form = UpdateTodoForm
    self.todo = Todo.objects.create(title="First todo")

  def test_update_page_returns_correct_response(self):
    response = self.client.get(f'/{self.todo.pk}/update/')

    self.assertTemplateUsed(response, 'todos/update.html')
    self.assertEqual(response.status_code, 200)

  def test_form_can_be_valid(self):
    self.assertTrue(issubclass(self.form, UpdateTodoForm))
    self.assertTrue('title' in self.form.Meta.fields)
    self.assertTrue('description' in self.form.Meta.fields)
  
    form = self.form({
      'title': 'The title',
      'description': 'The description'
    }, instance=self.todo)

    self.assertTrue(form.is_valid)
    form.save()
    self.assertEqual(Todo.objects.get(pk=self.todo.pk).title, 'The title')

  def test_form_can_be_invalid(self):
    form = self.form({
      'title': '',
      'description': 'The description'
    }, instance=self.todo)

    self.assertFalse(form.is_valid())

  def test_update_page_form_rendering(self):
    response = self.client.get(f'/{self.todo.pk}/update/')

    self.assertContains(response, '<form')
    self.assertContains(response, 'csrfmiddlewaretoken')
    self.assertContains(response, '<label for')

    # Test invalid form

    response = self.client.post(f'/{self.todo.pk}/update/', {
      'id': self.todo.pk,
      'title': '',
      'description': 'The description'
    }, instance = self.todo)


    self.assertContains(response,'<ul class="errorlist">')
    self.assertContains(response,'This field is required.')

    # test valid form

    response = self.client.post(f'/{self.todo.pk}/update/',{
      'title': 'The title',
      'description': 'The description'
    })

    self.assertRedirects(response, expected_url='/')

    self.assertEqual(Todo.objects.count(), 1)
    self.assertEqual(Todo.objects.get(pk=self.todo.pk).title, 'The title')

class DeletePageTest(TestCase):
  def setUp(self):
    self.todo = Todo.objects.create(title="First todo")

  def test_delete_page_deletes_todo(self):
    self.assertEqual(Todo.objects.count(), 1)

    response = self.client.post(f'/{self.todo.pk}/delete/')

    self.assertRedirects(response, expected_url='/')
    self.assertEqual(Todo.objects.count(), 0)