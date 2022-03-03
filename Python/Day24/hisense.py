"""
  驱动： https://npm.taobao.org/mirrors/chromedriver/
  下载对应谷歌版本放置到 Python 安装目录
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.maximize_window()

browser.get("https://www.hisense.com/")

search_field1 = browser.find_element_by_id("form-search")
search_field1.click()
search_field2 = browser.find_element_by_name("q")
search_field2.send_keys("冰箱")
search_field2.submit()

# browser.find_element(By.XPATH, "//span[@data-index='4']").click()

browser.find_element(By.XPATH, "//div[@class='filter-banner']/span[1]").click()


