from django.test import TestCase
from unittest import skip
from public_frontend.apps import PublicFrontendConfig
from django.apps import apps

# Create your tests here.

app_name = 'public_frontend'

class FrontendAppConfigTest(TestCase):

  def test_frontend_app_config(self):
    app_config = apps.get_app_config(app_name)
    assert isinstance(app_config, PublicFrontendConfig)
    assert app_config.name == app_name

""" Test templates rendering """
class IndexPageTest(TestCase):
  def test_index_page_returns_correct_response(self):
    response = self.client.get('/')

    self.assertTemplateUsed(response, 'public_frontend/index.html')
    self.assertEqual(response.status_code, 200)

  def test_index_page_has_correct_title(self):
    response = self.client.get('/')
    self.assertContains(response, '<title>Atlas Homepage</title>')

  def test_index_page_has_correct_menu(self):
    response = self.client.get('/')
    self.assertContains(response, '<a href="/">Home</a>')
    self.assertContains(response, '<a href="/features/">Features</a>')
    self.assertContains(response, '<a href="/about/">About</a>')
    self.assertContains(response, '<a href="/login/">Login</a>')
    self.assertContains(response, '<a href="/register/">Register</a>')


class AboutPageTest(TestCase):
  def test_about_page_returns_correct_response(self):
    response = self.client.get('/about/')

    self.assertTemplateUsed(response, 'public_frontend/about.html')
    self.assertEqual(response.status_code, 200)

  def test_about_page_has_correct_title(self):
    response = self.client.get('/about/')
    self.assertContains(response, '<title>Atlas About</title>')
  
  def test_about_page_has_correct_menu(self):
    response = self.client.get('/about/')
    self.assertContains(response, '<a href="/">Home</a>')
    self.assertContains(response, '<a href="/features/">Features</a>')
    self.assertContains(response, '<a href="/about/">About</a>')
    self.assertContains(response, '<a href="/login/">Login</a>')
    self.assertContains(response, '<a href="/register/">Register</a>')

class FeaturesPageTest(TestCase):
  def test_features_page_returns_correct_response(self):
    response = self.client.get('/features/')

    self.assertTemplateUsed(response, 'public_frontend/features.html')
    self.assertEqual(response.status_code, 200)

  def test_features_page_has_correct_title(self):
    response = self.client.get('/features/')
    self.assertContains(response, '<title>Atlas Features</title>')

  def test_features_page_has_correct_menu(self):
    response = self.client.get('/features/')
    self.assertContains(response, '<a href="/">Home</a>')
    self.assertContains(response, '<a href="/features/">Features</a>')
    self.assertContains(response, '<a href="/about/">About</a>')
    self.assertContains(response, '<a href="/login/">Login</a>')
    self.assertContains(response, '<a href="/register/">Register</a>')

""" Test pages functionality """

