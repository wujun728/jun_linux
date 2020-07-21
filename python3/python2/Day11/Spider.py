""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
import urllib.request
import time

if __name__ == '__main__':
    # 使用build_opener()是为了让python程序模仿浏览器进行访问
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    # 专刷某个页面
    print('开始：')
    tempUrl = 'https://www.cnblogs.com/visec479/p/5579798.html'
    for j in range(20000):
        try:
            opener.open(tempUrl)
            print('%d %s' % (j, tempUrl))
        except urllib.error.HTTPError:
            print('urllib.error.HTTPError')
            time.sleep(60)
        except urllib.error.URLError:
            print('urllib.error.URLError')
            time.sleep(60)
        time.sleep(60)
