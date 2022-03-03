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
importlib.reload(sys)


# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
# 爬图地址
mziTu = 'http://www.mzitu.com/'
# 定义存储位置
global save_path
save_path = ​'/mnt/data/mzitu'


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
            print("内页第几页：" + str(count))
            # 提取href
            href = a.attrs['href']
            print("套图地址：" + href)
            res_sub_1 = requests.get(href, headers=headers)
            soup_sub_1 = BeautifulSoup(res_sub_1.text, 'html.parser')
            # ------ 这里最好使用异常处理 ------
            try:
                # 获取套图的最大数量
                pic_max = soup_sub_1.find('div',class_='pagenavi').find_all('span')[6].text
                print("套图数量：" + pic_max)
                for j in range(1, int(pic_max) + 1):
                    # print("子内页第几页：" + str(j))
                    # j int类型需要转字符串
                    href_sub = href + "/" + str(j)
                    print(href_sub)
                    res_sub_2 = requests.get(href_sub, headers=headers)
                    soup_sub_2 = BeautifulSoup(res_sub_2.text, "html.parser")
                    img = soup_sub_2.find('div', class_='main-image').find('img')
                    if isinstance(img, bs4.element.Tag):
                        # 提取src
                        url = img.attrs['src']
                        array = url.split('/')
                        file_name = array[len(array)-1]
                        # print(file_name)
                        # 防盗链加入Referer
                        headers = {'Referer': href}
                        img = requests.get(url, headers=headers)
                        # print('开始保存图片')
                        f = open(file_name, 'ab')
                        f.write(img.content)
                        # print(file_name, '图片保存成功！')
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
        file = save_path + '/' + str(i)
        createFile(file)
        # 下载每页的图片
        print("套图页码：" + page)
        download(page, file)


if __name__ == '__main__':
    main()