"""
  模拟搜索
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.maximize_window()

browser.get("https://www.baidu.com")

browser.find_element(By.ID, "kw").send_keys("科帮网")

browser.close()
browser.quit()
