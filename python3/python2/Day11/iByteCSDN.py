""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# -*- coding:UTF-8 -*-
import re
import time
import random
import requests
import urllib.request
from bs4 import BeautifulSoup

firefoxHead = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"
host = "https://blog.csdn.net"
url = "https://blog.csdn.net/li1669852599/article/details/{}"
codes = ["90262038"]

def parseIPList(url="http://www.xicidaili.com/"):
    IPs = []
    request = urllib.request.Request(url, headers=firefoxHead)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "lxml")
    tds = soup.find_all("td")
    for td in tds:
        string = str(td.string)
        if re.search(IPRegular, string):
            IPs.append(string)
    return IPs


def PV(code):
    s = requests.Session()
    s.headers = firefoxHead
    count = 0
    while True:
        count += 1
        print("正在进行第{}次访问\t".format(count))
        IPs = parseIPList()
        s.proxies = {"http": "{}:8080".format(IPs[random.randint(0, 40)])}
        s.get(host)
        r = s.get(url.format(code))
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all("span")
        #print(spans[2].string)
        time.sleep(random.randint(60,75))


def main():
    PV(codes[0])


if __name__ == "__main__":
    main()