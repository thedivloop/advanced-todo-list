# import os
# import pathlib
from unittest import TestCase, skip, main
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


class WebPageTests(TestCase):

  def setUp(self):
    self.driver = webdriver.Chrome(options=options)
    self.driver.get("http://127.0.0.1:8000")

  def test_title(self):
    self.assertEqual(self.driver.title,"Atlas Homepage")

  def test_link_to_register_page(self):
    link_register = self.driver.find_element(By.LINK_TEXT,"Register")
    link_register.click()
    self.assertEqual(self.driver.title,"Atlas Register")
  
  def test_link_to_login_page(self):
    link_login = self.driver.find_element(By.LINK_TEXT,"Login")
    link_login.click()
    self.assertEqual(self.driver.title,"Atlas Login")

  def test_content_login_page(self):
    link_login = self.driver.find_element(By.LINK_TEXT,"Login")
    link_login.click()
    self.assertIn('<h1>Login</h1>',self.driver.page_source)

  def tearDown(self):
    self.driver.quit()

class LoginPageTest(TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_login_form_rendering(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    # Check if login form exists
    self.assertTrue(self.driver.find_element(By.NAME, "username"))
    self.assertTrue(self.driver.find_element(By.NAME, "password"))
    self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']"))
  
  def test_login_valid_credentials(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    self.driver.find_element(By.NAME, "username").send_keys("babyman")
    self.driver.find_element(By.NAME, "password").send_keys("!@#$%^&*()")
    self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(self.driver, 2)
    # Assert that after login, the user is redirected to the home page
    # self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/dashboard/")
    self.assertIn('<h1>Dashboard</h1>',self.driver.page_source)
    self.assertIn('<a href="/logout',self.driver.page_source)

  def tearDown(self):
    self.driver.quit()

# @skip("skip")
class LogoutPageTest(TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def test_logout_redirect(self):
    self.driver.get("http://127.0.0.1:8000/login/")
    self.driver.find_element(By.NAME, "username").send_keys("babyman")
    self.driver.find_element(By.NAME, "password").send_keys("!@#$%^&*()")
    self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    logout_button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    logout_button.click()
    # self.driver.find_element(By.LINK_TEXT,"Logout").click()
    self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/login/")


  def tearDown(self):
    self.driver.quit()


if __name__ == "__main__":
  main()