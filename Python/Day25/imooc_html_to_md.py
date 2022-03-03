# -*- coding: utf-8 -*-
import codecs
import sys
import random
import requests
from bs4 import BeautifulSoup
import html2text as ht

# 越多越好
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
# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': random.choice(blog_headers)}

save_file = 'F:/markdown.md'


def run():
    article = getHtml()
    text_maker = ht.HTML2Text()
    md = text_maker.handle(article)
    createFile(md)


def createFile(md):
    print('系统默认编码：{}'.format(sys.getdefaultencoding()))
    print('准备写入文件：{}'.format(save_file))
    # r+ 打开一个文件用于读写。文件指针将会放在文件的开头。
    # w+ 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # a+ 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    f = codecs.open(save_file, 'w+', 'utf-8')
    f.write(md)
    f.close()
    print('写入文件结束：{}'.format(f.name))


def getHtml():
    blog = "https://www.imooc.com/article/289897"
    res = requests.get(blog, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.find('div', id='article_content')
    print(article)
    article = article.decode_contents(formatter="html")
    return article


if __name__ == "__main__":
    run()


