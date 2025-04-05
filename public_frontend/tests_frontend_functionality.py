# import os
# import pathlib
from unittest import TestCase, skip, main
from selenium import webdriver
from selenium.webdriver.common.by import By

# def file_uri(filename):
#   return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome()

class WebPageTests(TestCase):

  def setUp(self):
    driver.get("http://127.0.0.1:8000")

  def test_title(self):
    # driver.get(file_uri("/"))
    self.assertEqual(driver.title,"Atlas Homepage")

  def test_link_to_register_page(self):
    link_register = driver.find_element(By.ID,"register_link")
    link_register.click()
    self.assertEqual(driver.title,"Atlas Register")
  
  def test_link_to_login_page(self):
    link_login = driver.find_element(By.ID,"login_link")
    link_login.click()
    self.assertEqual(driver.title,"Atlas Login")


  @skip("skip")
  def test_increase(self):
    driver.get(file_uri("counter.html"))
    increase = driver.find_element(By.ID, "increase")
    increase.click()
    self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text,"1")
  
  @skip("skip")
  def test_decrease(self):
    driver.get(file_uri("counter.html"))
    decrease = driver.find_element(By.ID, "decrease")
    decrease.click()
    self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text,"-1")
  
  @skip("skip")
  def test_multiple_increase(self):
    driver.get(file_uri("counter.html"))
    increase = driver.find_element(By.ID, "increase")
    for i in range(3):
      increase.click()
    self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text,"3")

if __name__ == "__main__":
  main()