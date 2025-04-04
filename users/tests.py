from django.test import TestCase
from unittest import skip
from django.apps import apps
# Create your tests here.

# app_name = f'{apps.get_containing_app_config(__name__).name}/'

class LoginPageTest(TestCase):
  def test_login_page_returns_correct_response(self):
    response = self.client.get('/login/')

    self.assertTemplateUsed(response, 'users/login.html')
    self.assertEqual(response.status_code, 200)

  def test_login_page_has_correct_title(self):
    response = self.client.get('/login/')
    self.assertContains(response, '<title>Atlas Login</title>')

class RegisterPageTest(TestCase):
  def test_register_page_returns_correct_response(self):
    response = self.client.get('/register/')

    self.assertTemplateUsed(response, 'users/register.html')
    self.assertEqual(response.status_code, 200)

  def test_register_page_has_correct_title(self):
    response = self.client.get('/register/')
    self.assertContains(response, '<title>Atlas Register</title>')