#coding=utf-8
#!/usr/bin/python
# 导入requests库
import requests
# 导入文件操作库
import os
import bs4
from bs4 import BeautifulSoup
import sys
import importlib
import random
import time
importlib.reload(sys)


# 越多越好
meizi_headers = [
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
headers = {'User-Agent': random.choice(meizi_headers)}
# 爬图地址
mziTu = 'http://www.mzitu.com/'
# 定义存储位置
global save_path
save_path = 'F:\BeautifulPictures'


# 创建文件夹
def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    # 切换路径至上面创建的文件夹
    os.chdir(file_path)


# 下载文件
def download(page_no, file_path):
    global headers
    res_sub = requests.get(page_no, headers=headers)
    # 解析html
    soup_sub = BeautifulSoup(res_sub.text, 'html.parser')
    # 获取页面的栏目地址
    all_a = soup_sub.find('div',class_='postlist').find_all('a',target='_blank')
    count = 0
    for a in all_a:
        count = count + 1
        if (count % 2) == 0:
            headers = {'User-Agent': random.choice(meizi_headers)}
            print("内页第几页：" + str(count))
            # 提取href
            href = a.attrs['href']
            print("套图地址：" + href)
            res_sub_1 = requests.get(href, headers=headers)
            soup_sub_1 = BeautifulSoup(res_sub_1.text, 'html.parser')
            # ------ 这里最好使用异常处理 ------
            try:
                # 获取套图的最大数量
                pic_max = soup_sub_1.find('div', class_='pagenavi').find_all('span')[6].text
                print("套图数量：" + pic_max)
                for j in range(1, int(pic_max) + 1):
                    # 单位为秒，1-3 随机数
                    time.sleep(random.randint(1, 3))
                    headers = {'User-Agent': random.choice(meizi_headers)}
                    # print("子内页第几页：" + str(j))
                    # j int类型需要转字符串
                    href_sub = href + "/" + str(j)
                    print("图片地址："+href_sub)
                    res_sub_2 = requests.get(href_sub, headers=headers)
                    soup_sub_2 = BeautifulSoup(res_sub_2.text, "html.parser")
                    img = soup_sub_2.find('div', class_='main-image').find('img')
                    if isinstance(img, bs4.element.Tag):
                        # 提取src
                        url = img.attrs['src']
                        array = url.split('/')
                        file_name = array[len(array)-1]
                        # 防盗链加入Referer
                        headers = {'User-Agent': random.choice(meizi_headers), 'Referer': url}
                        img = requests.get(url, headers=headers)
                        print('开始保存图片', img)
                        f = open(file_name, 'ab')
                        f.write(img.content)
                        print(file_name, '图片保存成功！')
                        f.close()
            except Exception as e:
                print(e)


# 主方法
def main():
    res = requests.get(mziTu, headers=headers)
    # 使用自带的html.parser解析
    soup = BeautifulSoup(res.text, 'html.parser')
    # 创建文件夹
    createFile(save_path)
    # 获取首页总页数
    img_max = soup.find('div', class_='nav-links').find_all('a')[3].text
    # print("总页数:"+img_max)
    for i in range(1, int(img_max) + 1):
        # 获取每页的URL地址
        if i == 1:
            page = mziTu
        else:
            page = mziTu + 'page/' + str(i)
        file = save_path + '\\' + str(i)
        createFile(file)
        # 下载每页的图片
        print("套图页码：" + page)
        download(page, file)


if __name__ == '__main__':
    main()