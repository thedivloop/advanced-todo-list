from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from users.apps import UsersConfig
from common.constants import LOGIN_URL, REGISTER_URL, DASHBOARD_URL, LOGOUT_URL, LOGIN_TEMPLATE, REGISTER_TEMPLATE, TODOS_URL

# Create your tests here.

app_name = 'users'

def create_test_user(username='testuser', password='testpass123'):
  return User.objects.create_user(username=username, password=password)


class UsersAppConfigTest(TestCase):

  def test_users_app_config(self):
    app_config = apps.get_app_config(app_name)
    assert isinstance(app_config, UsersConfig)
    assert app_config.name == app_name

class LoginPageTest(TestCase):

  def setUp(self):
    create_test_user()

  def test_login_get_request_renders_form(self):
    response = self.client.get(LOGIN_URL)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, LOGIN_TEMPLATE)
    self.assertContains(response, '<form')
    self.assertContains(response, 'username')
    self.assertContains(response, 'password')
    self.assertContains(response, '<title>Atlas Login</title>')

  def test_login_post_valid_credentials_redirects_to_dashboard(self):
    response = self.client.post(LOGIN_URL, {
        'username': 'testuser',
        'password': 'testpass123'
    })
    self.assertRedirects(response, TODOS_URL)

    # Optionally confirm user is authenticated
    user = auth.get_user(self.client)
    self.assertTrue(user.is_authenticated)

  def test_login_post_invalid_credentials_shows_errors(self):
    response = self.client.post(LOGIN_URL, {
        'username': 'wrong',
        'password': 'wrongpass'
    })

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, LOGIN_TEMPLATE)
    self.assertContains(response, '<ul class="errorlist')

  def test_authenticated_user_access_login_redirects(self):
    self.client.login(username='testuser', password='testpass123')

    response = self.client.get(LOGIN_URL)
    self.assertRedirects(response, TODOS_URL)

  def test_login_post_without_csrf_token_should_fail(self):
    client = Client(enforce_csrf_checks=True)
    response = client.post(LOGIN_URL, {
        'username': 'testuser',
        'password': 'testpass123'
    })

    self.assertEqual(response.status_code, 403)  # Forbidden due to missing CSRF token



class RegisterPageTest(TestCase):
  

  def test_register_page_renders_form(self):
    response = self.client.get(REGISTER_URL)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, REGISTER_TEMPLATE)
    self.assertContains(response, '<title>Atlas Register</title>')
    self.assertContains(response, '<form')
    self.assertContains(response, 'name="username"')
    self.assertContains(response, 'name="password1"')
    self.assertContains(response, 'name="password2"')

  def test_valid_user_registration_creates_user_and_redirects(self):
    response = self.client.post(REGISTER_URL, {
      'username': 'newuser',
      'password1': 'SuperSecret123',
      'password2': 'SuperSecret123'
    })

    self.assertRedirects(response, DASHBOARD_URL)
    self.assertTrue(User.objects.filter(username='newuser').exists())

  def test_register_with_mismatched_passwords_shows_error(self):
    response = self.client.post(REGISTER_URL, {
        'username': 'newuser',
        'password1': 'PasswordOne123',
        'password2': 'PasswordTwo123'
    })

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "The two password fields didn’t match")

  def test_register_with_existing_username_fails(self):
    User.objects.create_user(username='existing', password='SomePass123')

    response = self.client.post(REGISTER_URL, {
        'username': 'existing',
        'password1': 'AnotherPass123',
        'password2': 'AnotherPass123'
    })

    self.assertContains(response, "A user with that username already exists")

  def test_register_form_has_csrf_token(self):
    response = self.client.get(REGISTER_URL)
    self.assertContains(response, 'csrfmiddlewaretoken')

  def test_password_too_weak_is_rejected(self):
    response = self.client.post(REGISTER_URL, {
      'username': 'weakpassuser',
      'password1': '123',
      'password2': '123'
    })

    self.assertContains(response, "This password is too short")

class LogoutPageTest(TestCase):

  def setUp(self):
    create_test_user()

  def test_logout_redirects_to_login(self):
    self.client.login(username='testuser', password='testpass123')

    response = self.client.get(LOGOUT_URL)
    self.assertRedirects(response, LOGIN_URL)

    # Check if user is logged out
    user = auth.get_user(self.client)
    self.assertFalse(user.is_authenticated)

class DashboardPageTest(TestCase):

  def test_redirection_to_loginpage_ifnot_loggedin(self):
    response = self.client.get('/todos/')
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/login/?next=/todos/')  