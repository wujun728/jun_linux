""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""

#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 导入requests库
import requests
from bs4 import BeautifulSoup
import sys
import importlib

importlib.reload(sys)
# 导入文件操作库
import codecs

####
#  本案例只供参考,脚本抓取地址为注册中心地址 // 目前使用codecs完成客户端代理抓取网页信息，本地生成代理工具
####

# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'serviceName': 'labc-discovery-client',
           'X-SERVICE-NAME': '674f6671564c5a6d32596f70495833414b3152474d30577a4457784d58702b396b474164434e6f6e6143513d'}
server = 'http://192.168.50.25:8010'
# 注册中心地址
eureka = 'http://192.168.50.25:8010/discovery'
global save_path
# 定义存储位置
save_path = 'E:/python-test'


# 获取注册中心页面
def get_contents(eureka_url):
    req = requests.get(url=eureka_url)
    html = req.content
    html_doc = str(html, 'utf-8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    texts = bf.find_all('table', id='instances')
    return texts

# 写入文件
def write_txt(eureka_url, content, code):
    with codecs.open(eureka_url, 'a', encoding=code) as f:
        f.write(content)

# 主方法
def main():
    res = requests.get(eureka, headers=headers)
    html = res.content
    html_doc = str(html, 'utf-8')
    # 打印当前内容
    # print(html_doc)

    # 使用自带的html.parser 解析
    soup = BeautifulSoup(html_doc, 'html.parser')
    a = soup.find_all('table', id='instances')
    # 获取所有注册服务列表
    print(a)
    # for each in a:
    #     try:
    #         # chapter = server + each.get('href')
    #         # content = get_contents(chapter)
    #         chapter = save_path + "/" + each.string + ".txt"
    #         # write_txt(chapter, a, 'utf8')
    #     except Exception as e:
    #         print(e)


if __name__ == '__main__':
    main()
