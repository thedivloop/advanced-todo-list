from django.contrib.auth.models import User
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from unittest import skip
from django.apps import apps
# Create your tests here.

# app_name = f'{apps.get_containing_app_config(__name__).name}/'

class LoginPageTest(TestCase):

  def test_login_get_request_renders_form(self):
    response = self.client.get(reverse("users:login"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'users/login.html')
    self.assertContains(response, '<form')
    self.assertContains(response, 'username')
    self.assertContains(response, 'password')
    self.assertContains(response, '<title>Atlas Login</title>')

  def test_login_post_valid_credentials_redirects_to_dashboard(self):
    # Create a user first
    User.objects.create_user(username='testuser', password='testpass123')

    response = self.client.post(reverse('users:login'), {
        'username': 'testuser',
        'password': 'testpass123'
    })
    self.assertRedirects(response, reverse('users:dashboard'))

    # Optionally confirm user is authenticated
    user = auth.get_user(self.client)
    self.assertTrue(user.is_authenticated)

  def test_login_post_invalid_credentials_shows_errors(self):
    response = self.client.post(reverse('users:login'), {
        'username': 'wrong',
        'password': 'wrongpass'
    })

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'users/login.html')
    self.assertContains(response, '<ul class="errorlist')

  def test_authenticated_user_access_login_redirects(self):
    User.objects.create_user(username='testuser', password='testpass123')
    self.client.login(username='testuser', password='testpass123')

    response = self.client.get(reverse('users:login'))
    self.assertRedirects(response, reverse('users:dashboard'))  


class RegisterPageTest(TestCase):

  def test_register_page_returns_correct_response(self):
    response = self.client.get('/register/')

    self.assertTemplateUsed(response, 'users/register.html')
    self.assertEqual(response.status_code, 200)

  def test_register_page_has_correct_title(self):
    response = self.client.get('/register/')
    self.assertContains(response, '<title>Atlas Register</title>')

class DashboardPageTest(TestCase):

  def test_redirection_to_loginpage_ifnot_loggedin(self):
    response = self.client.get('/dashboard/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/login/?next=/dashboard/')  