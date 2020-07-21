""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 15:01
# @Author  : iByte
import requests
import time
# 导入文件操作库
import os
import re
import bs4
from bs4 import BeautifulSoup
import sys
from mysql_DBUtils import mysql

# 写入数据库
def write_db(param):
    try:
        sql = "insert into  agent_ips(ip,port,degree,address,speed,lastCheckTime) "
        sql = sql + "VALUES(%(ip)s,%(port)s, %(degree)s,%(address)s,%(speed)s,%(lastCheckTime)s)"
        mysql.insert(sql, param)
    except Exception as e:
        print(e)


# 主方法
def main():
    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    page_max = 5
    # 爬图地址
    for i in range(1, int(page_max) + 1):
        print("第几页：" + str(i))
        if i == 1:
            house = 'https://www.kuaidaili.com/free/'
        else:
            house = 'https://www.kuaidaili.com/free/inha/' + str(i)
        res = requests.get(house, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        tr_max = soup.find('table', class_='table table-bordered table-striped').find_all('tr')
        for i, tr in enumerate( tr_max):
            try:
                # 第一行剔除
                if(i>1):
                    dailiIP_param = {}
                    td_line = tr.find_all('td')
                    for i, td in enumerate(td_line):
                        if (i == 1):
                            dailiIP_param["ip"] = td.text
                        if (i == 2):
                            dailiIP_param["port"] = td.text
                        if (i == 3):
                            dailiIP_param["degree"] = td.text
                        if (i == 4):
                            dailiIP_param["address"] = td.text
                        if (i == 5):
                            dailiIP_param["speed"] = td.text
                        if (i == 6):
                            dailiIP_param["lastCheckTime"] = td.text
                    write_db(dailiIP_param)
                    time.sleep(3)
            except Exception as e:
                print(e)
        mysql.end("commit")
    mysql.dispose()


if __name__ == '__main__':
    main()
