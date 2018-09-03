import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('/Users/zyx/Downloads/cs428/chromedriver')
service.start()
capabilities = {'chrome.binary': '/path/to/custom/chrome'}
driver = webdriver.Remote(service.service_url, capabilities)
# Add any failure cases , test 1000 cases around 1 second.
driver.get('http://localhost:8000/');
try:
    driver.find_element_by_name("login")
    print('Test Pass : element found')
except Exception as e:
    print('Exception found', format(e))
#time.sleep(5)
# driver.get('http://localhost:8000/');
try:
    #driver.find_element_by_class_name("Signup")
    driver.find_element_by_id("theme-blue")
    print('Test Pass : element found')
except Exception as e:
    print('Exception found', format(e))
#time.sleep(5)

driver.quit()


