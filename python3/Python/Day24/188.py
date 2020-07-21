"""
  驱动： https://npm.taobao.org/mirrors/chromedriver/
  下载对应谷歌版本放置到 Python 安装目录
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.maximize_window()

browser.get("http://cntao-ap-v82/login.html")

# browser.find_element_by_xpath("//input[@placeholder='请输入用户名']").send_keys("zhipeng.zhang")
# browser.find_element_by_xpath("//input[@placeholder='请输入密码']").send_keys("zhipeng.zhang")
# browser.find_element_by_tag_name("button").click()

browser.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys("zhipeng.zhang")
browser.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys("zhipeng.zhang")
browser.find_element(By.TAG_NAME, "button").click()


