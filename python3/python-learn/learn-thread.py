from threading import Thread
from Queue import Queue
import random, time
from bs4 import BeautifulSoup
import os, sys, urllib2
import urllib2,os,socket
import thread


'''
    date:   2014-03-07 20:50:15
    url:    http://www.dbmeizi.com
    desc:   using mulitithreading download pictures from dbmeizi.com
    email:  withfaker@gmail.com
'''

queue = Queue()
pic_path = os.path.join(os.curdir, "images")

class  ProducerThread(Thread):
    def run(self):
        page_loop()

class ConsumerThread(Thread):
    def run(self):
        while True:
            if queue.empty():
                thread.exit()
            url = queue.get()
            queue.task_done()
            fetch(url) 

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
    #print "BEGIN TO FETCH PAGE:[%s]" % page
    for girl in my_girl:
        link = girl.get('src')
        flink = 'http:' + link
        queue.put(flink)
    page = int(page) + 1
    page_loop(page)

#fetch pictures
def fetch(url):
    print "url:[%s]" % url
    p = os.path.join(os.curdir, pic_path, url[-11:])
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
    #print "fetch url done.[%s]" % url

if __name__ == '__main__':
    if not os.path.isdir(pic_path):
        os.mkdir(pic_path)
    ProducerThread(name="Producer1").start()
    ConsumerThread(name="Consumer1").start()
    ConsumerThread(name="Consumer2").start()
    ConsumerThread(name="Consumer3").start()
    ConsumerThread(name="Consumer4").start()
    ConsumerThread(name="Consumer5").start()
    #ConsumerThread(name="Consumer6").start()
    #ConsumerThread(name="Consumer7").start()
    #ConsumerThread(name="Consumer8").start()
    #ConsumerThread(name="Consumer9").start()
    #ConsumerThread(name="Consumer10").start()
