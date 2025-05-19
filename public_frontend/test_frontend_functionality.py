# import os
# import pathlib
import random
from unittest import TestCase, skip, main
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage') # Prevents crashes due to limited shared memory in Docker

# def file_uri(filename):
#   return pathlib.Path(os.path.abspath(filename)).as_uri()

new_user_with_mismatched_passwords = {
  "username": "testuser123",
  "password1": "TestPassword123!",
  "password2": "DifferentPassword!"
}

new_user_with_invalid_username = {
  "username": "badtestuser123",
  "password1": "TestPassword123!",
  "password2": "TestPassword123!"
}

def delete_test_user(username):
  try:
    user = User.objects.get(username=username)
    user.delete()
    print("User deleted successfully.")
  except User.DoesNotExist:
    print("User does not exist.")

class WebPageTests(TestCase):

  def setUp(self):
    self.driver = webdriver.Chrome(options=options)
    self.driver.get("http://127.0.0.1:8000")

  def test_title(self):
    self.assertEqual(self.driver.title,"Atlas Homepage")

  def test_link_to_register_page(self):
    link_register = self.driver.find_element(By.LINK_TEXT,"REGISTER")
    link_register.click()
    self.assertEqual(self.driver.title,"Atlas Register")
  
  def test_link_to_login_page(self):
    link_login = self.driver.find_element(By.LINK_TEXT,"LOGIN")
    link_login.click()
    self.assertEqual(self.driver.title,"Atlas Login")

  def test_content_login_page(self):
    link_login = self.driver.find_element(By.LINK_TEXT,"LOGIN")
    link_login.click()
    self.assertIn('<h1>Login</h1>',self.driver.page_source)

  def tearDown(self):
    self.driver.quit()

class LoginPageTest(TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    unique_id = random.randint(1000, 9999)
    self.username = f"testuser{unique_id}"
    self.password = f"TestPassword{unique_id}!"
    self.password2 = f"TestPassword{unique_id}!"

  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_login_form_rendering(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    # Check if login form exists
    self.assertTrue(self.driver.find_element(By.NAME, "username"))
    self.assertTrue(self.driver.find_element(By.NAME, "password"))
    self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']"))
  
  def test_login_valid_credentials(self):
    self.driver.get("http://127.0.0.1:8000/register/")
    self.driver.find_element(By.NAME, "username").send_keys(self.username)
    self.driver.find_element(By.NAME, "password1").send_keys(self.password)
    self.driver.find_element(By.NAME, "password2").send_keys(self.password2)
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(self.driver, 5).until(EC.url_contains("/todos/"))
    self.driver.get("http://127.0.0.1:8000/logout")
    WebDriverWait(self.driver, 5).until(EC.url_contains("/login/"))
    # self.driver.get("http://127.0.0.1:8000/login/")
    try:
      WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    except:
      print("🚨 Login page did not load in time!")
      print("Current URL:", self.driver.current_url)
      print("Page Source:", self.driver.page_source)
      raise
    self.driver.find_element(By.NAME, "username").send_keys(self.username)
    self.driver.find_element(By.NAME, "password").send_keys(self.password)
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(self.driver, 5).until(EC.url_contains("/todos/"))
    # Assert that after login, the user is redirected to the home page
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/todos/")
    # TODO update the 2 below asserts to match the /todos/ page
    # self.assertIn('<h1>Dashboard</h1>',self.driver.page_source)
    # self.assertIn('<a href="/logout',self.driver.page_source)
    delete_test_user(self.username)

  def test_login_invalid_credentials(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    self.driver.find_element(By.NAME, "username").send_keys(new_user_with_invalid_username["username"])
    self.driver.find_element(By.NAME, "password").send_keys(new_user_with_invalid_username["password1"])
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(self.driver, 4)
    # Assert that after login, the user is redirected to the home page
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/login/")

    self.assertIn("errorlist nonfield",self.driver.page_source)

  def tearDown(self):
    self.driver.quit()

class RegisterPageTest(TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    unique_id = random.randint(1000, 9999)
    self.username = f"testuser{unique_id}"

  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_register_form_rendering(self):
    self.driver.get("http://127.0.0.1:8000/register/")
    self.assertTrue(self.driver.find_element(By.NAME, "username"))
    self.assertTrue(self.driver.find_element(By.NAME, "password1"))
    self.assertTrue(self.driver.find_element(By.NAME, "password2"))
    self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']"))

  def test_register_valid_user(self):
    self.driver.get("http://127.0.0.1:8000/register/")
    self.driver.find_element(By.NAME, "username").send_keys(self.username)
    self.driver.find_element(By.NAME, "password1").send_keys("TestPassword123!")
    self.driver.find_element(By.NAME, "password2").send_keys("TestPassword123!")
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(self.driver, 5).until(EC.url_contains("/todos/"))
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/todos/")
    delete_test_user(self.username)

  def test_register_mismatched_passwords(self):
    self.driver.get("http://127.0.0.1:8000/register/")
    self.driver.find_element(By.NAME, "username").send_keys("testmismatch")
    self.driver.find_element(By.NAME, "password1").send_keys("TestPassword123!")
    self.driver.find_element(By.NAME, "password2").send_keys("DifferentPassword!")
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(self.driver, 2)
    self.assertIn("password", self.driver.page_source.lower())
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/register/")

  def tearDown(self):
    self.driver.quit()


@skip("skip")
class LogoutPageTest(TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_logout_redirect(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    self.driver.find_element(By.NAME, "username").send_keys("babyman")
    self.driver.find_element(By.NAME, "password").send_keys("!@#$%^&*()")
    self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # TODO update the 2 below asserts to match the /todos/ page
    # logout_button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    # logout_button.click()
    # self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/login/")


  def tearDown(self):
    self.driver.quit()

class DashboardPageTest(TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_redirection_to_loginpage_ifnot_loggedin(self):
    self.driver.get("http://127.0.0.1:8000/dashboard/")
    WebDriverWait(self.driver, 2)
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/login/?next=/dashboard/")

# if __name__ == "__main__":
#   main()