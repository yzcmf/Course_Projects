import time
from selenium import webdriver


# server run successfully

driver = webdriver.Chrome('/Users/zyx/Downloads/cs428/chromedriver');  # Optional argument, if not specified will search path.

driver.get('http://localhost:8000/');
time.sleep(15) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(15) # Let the user actually see something!
driver.quit()