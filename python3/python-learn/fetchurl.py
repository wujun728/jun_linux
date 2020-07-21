# -*- encoding=utf-8 -*-
from bs4 import BeautifulSoup
import os, sys, urllib2
import urllib2,os,socket

'''
    date:   2014-03-03 18:13:33
    url:    http://www.dbmeizi.com
    desc:   fetch all images from dbmeiz.com
    email:  withfaker@gmail.com
'''

socket.setdefaulttimeout(10)

#load into list from file
file = 'urls.txt'
l = open(file, 'r').readlines()
for i in range(len(l)):
    l[i] = l[i].strip()


#get all urls
def page_loop(page=0):
    url = 'http://www.dbmeizi.com/?p=%s' % page
    try:
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content)
    except:
        print "internal error:[%s]" % url
        page_loop(int(page)+1)

    my_girl = soup.find_all('img')
    if my_girl == []:
        print 'finished!'
        sys.exit(0)
    print "BEGIN TO FETCH PAGE:[%s]" % page
    for girl in my_girl:
        link = girl.get('src')
        flink = 'http:' + link
        if flink in l:
            #print "already exists:[%s]" % flink
            continue
        f = open(file, 'ab')
        f.write(flink.strip() + '\n')
        l.append(flink.strip())
        f.close()
        try:
            fetch(flink.strip())
        except:
            print "fetch error![%s]" % flink
            continue
    page = int(page) + 1
    page_loop(page)

#fetch pictures
def fetch(url):
    p = os.path.join(os.curdir, 'pics', url[-11:])
    if os.path.isfile(p):
        st = os.stat(p)
        if st.st_size > 0:
            print "file[%s] is already exists." % url[-11:]
            return
        else:
            print "file[%s] exists. but size is too small." % url[-11:]
    req = urllib2.Request(url)
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Encoding','gzip,deflate,sdch')
    req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')
    req.add_header('Cache-Control','max-age=0')
    req.add_header('Connection','keep-alive')
    req.add_header('Referer','https://www.dbmeizi.com')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1660.0 Safari/537.36')
    try:
        resp = urllib2.urlopen(req)
    except:
        print "internal error:[%s]" % url
        return
    f = open(p, 'wb')
    f.write(resp.read())
    f.close()
    resp.close()
    print "fetch url done.[%s]" % url

if __name__ == '__main__':
    if not os.path.isdir('pics'):
        os.mkdir('pics')
    page_loop()

