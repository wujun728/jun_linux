""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 18:12
# @Author  : iByte

import os
import re
import time
import requests
from urllib import request
from bs4 import BeautifulSoup


class KuaiDaiLiOps(object):
    def __init__(self):
        self.session = requests.session()
        self.proxies = None
        self.timeout = 5
        self.time_interval = 3
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
        }

    def get_status(self, url):
        """
        获取状态
        :param url: 访问地址
        :return: 返回response或False
        """
        response = self.session.get(
            url=url,
            headers=self.headers,
            proxies=self.proxies,
            timeout=self.timeout,
            # verify=False,
            # allow_redirects=False
        )
        if response.status_code == 200:
            return response
        else:
            print("ERROR: 网络连接失败！ status: %s url: %s" % (response.status_code, url))
            return False

    def get_index(self, url):
        """
        访问首页，建立连接
        :param url:
        :return:
        """
        response = self.get_status(url)
        if response:
            # response.encoding = "utf-8"
            # html = response.text
            # print(html)
            #print("首页,建立连接...")
            return True
        else:
            print("ERROR: 首页访问失败！")
            return False

    def parse_page(self, url):
        """
        页数解析--只有10页
        :param url:
        :return:
        """
        response = self.get_status(url)
        if not response:
            return None
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        pages = soup.select("#listnav > ul > li > a")
        url_list = []
        for page in pages:
            # title = page.text
            href = page.get("href")
            get_url = re.findall(r"(https://.*?)/", url)
            url = get_url[0] + href
            url_list.append(url)

        return url_list

    def parse_html(self, url):
        """
        页面解析
        :param url:
        :return:
        """
        # print(url)
        response = self.get_status(url)
        if not response:
            return None
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        trs = soup.select("#freelist tbody > tr")
        ip_port_list = []
        for tr in trs:
            tds = tr.find_all("td")
            ip = port = hidden = ip_type = get_post_support = location = speed = last_verification_time = ""
            for i in range(len(tds)):
                # "IP": ["PORT", "匿名度", "类型", "get/post支持", "位置", "响应速度	", "最后验证时间"],
                ip = tds[0].text
                port = tds[1].text
                ip_port = ip + ":" + port + "\n"
                if not ip:
                    continue
                ip_port_list.append(ip_port)
        return ip_port_list

    @staticmethod
    def write_to_text(path, content):
        path = os.path.abspath(path)
        with open(path, 'a+', encoding='utf-8') as f:
            f.writelines(content)

    def main(self):
        # 首页
        url = "https://www.kuaidaili.com"
        self.get_index(url)

        # 页数解析
        url = "https://www.kuaidaili.com/ops/"
        url_list = self.parse_page(url)
        path = os.path.join(os.getcwd(), "IP.txt")
        path = os.path.abspath(path)
        # 翻页
        for url in url_list:
            ip_port_list = self.parse_html(url)  # 解析页面
            for ip_port in ip_port_list:
                # 设置代理ip访问方式，http和https
                # proxy = {'http': ip, 'https': ip}
                print(ip_port)


if __name__ == '__main__':
    kdl = KuaiDaiLiOps()
    while(True):
        kdl.main()




