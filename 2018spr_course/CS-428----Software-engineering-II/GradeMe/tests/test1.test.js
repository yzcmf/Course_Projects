"use strict";


var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.safari()).
   build();

driver.get("http://localhost:8000");

var elem = driver.find_element_by_name("login").click();
var login = driver.find_element_by_class_name("Login");
time.sleep(1);
elem = driver.find_element_by_name("signup").click();
var signup = driver.find_element_by_class_name("Register");
time.sleep(1);
elem = driver.find_element_by_name("login").click();
time.sleep(1);
