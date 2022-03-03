__author__ = "小柒"
__blog__ = "https://blog.52itstyle.vip/"
import os
# 导入requests库
import requests
# 导入文件操作库
import codecs
from bs4 import BeautifulSoup


# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
           'cookie': 'network→www.douban.com→headers查看cookie'}
# 好评500条，中评500条，差评500条
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=m
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=l
server = 'https://movie.douban.com/subject/26266893/comments'
# 定义存储位置
global save_path
save_path = os.getcwd()+"\\Text\\"+'短评_好评.txt'
global page_max
# 好评 499*20=9980
page_max = 499  # 500 短评论，后面就看不到了，不知道是否豆瓣有意而为之给隐藏了,哈哈哈原来是没登录导致的。
global comments
comments = ''


# 获取短评内容
def get_comments(page):
    req = requests.get(url=page)
    html = req.content
    html_doc = str(html, 'utf-8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    comment = bf.find_all(class_="short")
    for short in comment:
        global comments
        comments = comments + short.text


# 写入文件
def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code)as f:
        f.write(content)


# 主方法
def main():
    for i in range(0, page_max):
        try:
            page = server + '?start='+str(i*20)+'&limit=20&sort=new_score&status=P&percent_type=h'
            get_comments(page)
            write_txt(save_path, comments, 'utf8')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()

