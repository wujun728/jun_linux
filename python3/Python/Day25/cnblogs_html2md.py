# -*- coding: utf-8 -*-
import codecs
import sys
import tomd
import random
import requests
from bs4 import BeautifulSoup
import mysql_DBUtils
from mysql_DBUtils import MyPymysqlPool


blog_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]


# 定义DB
mysql = MyPymysqlPool("dbMysql")


def reptile():
    page = 2
    for n in range(1, page):
        url = "https://www.cnblogs.com/yjmyzz/default.html?page=" + str(n)
        headers = {'User-Agent': random.choice(blog_headers)}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        count = soup.find_all(class_='postTitle')
        for c in count:
            try:
                # 获取博客地址
                href = c.find('a').attrs['href']
                headers = {'User-Agent': random.choice(blog_headers)}
                res = requests.get(href, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                # 获取博客内容
                content = soup.find('div', class_='blogpost-body')
                # 去掉博客外层的DIV
                content = content.decode_contents(formatter="html")
                # 获取博客标题
                title = soup.find('a', id='cb_post_title_url').text
                # 博客HTML转MD
                content = tomd.Tomd(content).markdown
                # 博客写入数据库
                write_db(title, content, href)
                print("已插入:{}".format(href))
            except Exception as e:
                print(e)


# 写入数据库
def write_db(title, content, url):
    sql = "INSERT INTO blog (title, content,url) VALUES(%(title)s, %(content)s, %(url)s);"
    param = {"title": title, "content": content, "url": url}
    mysql.insert(sql, param)


if __name__ == "__main__":
    reptile()



