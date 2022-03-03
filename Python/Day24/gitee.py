"""
  从零学Python：https://gitee.com/52itstyle/Python

  模拟登陆 码云

"""
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.maximize_window()

browser.get("https://gitee.com/login")

browser.find_element(By.ID, "user_login").send_keys("345849402@qq.com")
browser.find_element(By.ID, "user_password").send_keys("123456")
browser.find_element(By.NAME, "commit").click()
