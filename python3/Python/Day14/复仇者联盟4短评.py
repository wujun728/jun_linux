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
           'cookie': 'gr_user_id=e121d183-f3f8-4c4c-8f6f-deac2e134a81; bid=cxPQAI-Bxyg; __yadk_uid=LKQye5qAEvDkHM8U9WMRB4wIFawbSYDF; douban-fav-remind=1; ll="118221"; _vwo_uuid_v2=D1C242F03E5FD61A09E0C1FE3106F4D0B|a4215ebb0c89a5aa37fcb62c3b92eb47; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1556191176%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DmibLGNNQiMDN_yIgz35YwO_RZBoP_vJ7xXWiIA89BOe%26wd%3D%26eqid%3Db873911b00197b1f000000035cc197be%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.891945692.1490618347.1553510394.1556191177.25; __utmc=30149280; __utmz=30149280.1556191177.25.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; ct=y; dbcl2="65246615:vr+bvtStGzA"; ck=ppPi; __utmv=30149280.6524; _pk_id.100001.8cb4=ced92c32ea3c2dfe.1490618346.21.1556191552.1553510392.; __utmb=30149280.10.10.1556191177'}
# 好评500条，中评500条，差评500条
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=m
# https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P&percent_type=l
server = 'https://movie.douban.com/subject/26100958/comments'
# 定义存储位置
global save_path
save_path = os.getcwd()+"\\Text\\"+'复仇者联盟4短评_差评.txt'
global page_max
# 好评
page_max = 252  # 500 短评论，后面就看不到了，不知道是否豆瓣有意而为之给隐藏了,哈哈哈原来是没登录导致的。
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
            page = server + '?start='+str(i*20)+'&limit=20&sort=new_score&status=P&percent_type=l'
            get_comments(page)
            write_txt(save_path, comments, 'utf8')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()

