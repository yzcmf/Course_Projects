from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Safari()
driver.get("http://localhost:8000")
assert "GradeMe" in driver.title
elem = driver.find_element_by_name("login").click()
login = driver.find_element_by_class_name("Login")
assert login is not None
time.sleep(1)
assert "GradeMe" in driver.title
elem = driver.find_element_by_name("signup").click()
signup = driver.find_element_by_class_name("Register")
assert signup is not None
time.sleep(1)
assert "GradeMe" in driver.title
elem = driver.find_element_by_name("login").click()
time.sleep(1)
