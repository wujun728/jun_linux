# -*- coding: utf-8 -*-
'''
Created on 2015-3-30

@author: Nob
'''

import requests

s = requests.session()
data = {
    "redir":"https://movie.douban.com/",
    "form_email":"tong695@163.com",
    "form_password":"nobcan",
    "captcha-solution":"smell",
    "captcha-id":"uNESfdDU8JjWODBym5Zyy3C3:en"
}

resp = s.post('https://accounts.douban.com/login', data)
print resp.elapsed
print resp.content
# print s.get('http://www.douban.com/').content