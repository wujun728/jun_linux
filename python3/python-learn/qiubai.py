#!/usr/bin/env python
#-*- encoding=UTF-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2014 mktime

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
    urls:   ['http://blog.knownsec.com/2012/04/about-content-encoding-gzip/',
             'http://git.oschina.net/mktime/python-learn']
'''

import re
import socket
import httplib
import urllib2
import zlib
import sys
import random
import time
import sqlite3
import md5
import os
from Queue import Empty
import multiprocessing

download_queue = multiprocessing.Queue()

item_queue = multiprocessing.Queue()

socket.setdefaulttimeout(10)

CACHE_PATH = 'I:/cache'

EXPIRE_SECOND = 600

if not os.path.isdir(CACHE_PATH):
    os.mkdir(CACHE_PATH)

def time_cost(foo):
    def calc_costs(*args, **kwargs):
        begin = time.time()
        result = foo(*args, **kwargs)
        end = time.time()
        print "[%f] seconds [%s] it costs." % ((end - begin), foo.__name__)
        return result
    return calc_costs


def make_request(url, is_gzip = True):
    req = urllib2.Request(url)
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    if is_gzip:
        req.add_header('Accept-Encoding','gzip,deflate,sdch')
    req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')
    req.add_header('Cache-Control','max-age=0')
    req.add_header('Connection','keep-alive')
    req.add_header('Referer',url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1660.0 Safari/537.36')
    return req


def get_url_content(url):
    cache_path = os.path.join(CACHE_PATH, hash_url(url))
    if os.path.isfile(cache_path):
        st_mtime = os.stat(cache_path).st_mtime
        if (time.time() - st_mtime) < EXPIRE_SECOND:
            return get_cache(url)
    while True:
        try:
            req = make_request(url)
            resp = urllib2.urlopen(req)
        except socket.error, e:
            print "SocketError when urlopen[%s]." % e.message
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
            print '<' * 80
            print e.read()
            print '>' * 80
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        except urllib2.URLError, e:
            print "URLError:", e.reason
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        except httplib.BadStatusLine, e:
            print "BadStatusLine:", e.message
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        except:
            print "Unknown error:", e.message
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        try:
            html_data = resp.read()
        except socket.timeout, e:
            print "Error when reading:[%s]." % e.message
            resp.close()
            t = random.randrange(10, 15)
            print "Try again after [%d] seconds." % t
            time.sleep(t)
            continue
        break
    resp.close()
    is_gzip = (resp.info().getheader('Content-Encoding') == 'gzip') if True else False
    if is_gzip:
        html_data = get_compressed_data(html_data)
    save_cache(url, html_data)
    return html_data


def save_cache(url, content):
    cache_path = os.path.join(CACHE_PATH, hash_url(url))
    open(cache_path, 'w').write(content)


def delete_cache(url):
    cache_path = os.path.join(CACHE_PATH, hash_url(url))
    os.remove(cache_path)


def get_cache(url):
    cache_path = os.path.join(CACHE_PATH, hash_url(url))
    return open(cache_path, 'r').read()


def hash_url(url):
    m = md5.md5()
    m.update(url)
    return m.hexdigest().upper()


def get_compressed_data(s):
    return zlib.decompress(s, 16 + zlib.MAX_WBITS)


def parse_qiubai(item_queue, html_data):
    pattern = r'<div.+?<div class="content" title="(.+?)">[\r\n\s]+(.+?)[\r\n\s]+</div>[\r\n\s]+(?:<div class="thumb">.+?<img src="(.+?)" alt="(.+?)" />)?.*?</div>.+?class="up">.+? id="up-(.+?)".+?>(.+?)</a>.+?class="down">.+?>(.+?)</a>.+?class="comment">.+?>(.+?)</a>'
    m = re.compile(pattern, re.DOTALL)
    content_arr = m.findall(html_data)
    total_items = len(content_arr)
    for i in range(total_items):
        _comment_cnt = '0'
        if content_arr[i][7].isdigit():
            _comment_cnt = content_arr[i][7].replace('\'', '')
        item = dict(
            created     = content_arr[i][0].replace('\'', ''),
            content     = content_arr[i][1].decode('UTF-8').replace('\'', ''),
            img_src     = content_arr[i][2].replace('\'', ''),
            img_desc    = content_arr[i][3].decode('UTF-8').replace('\'', ''),
            id          = content_arr[i][4].replace('\'', ''),
            vote_up     = content_arr[i][5].replace('\'', ''),
            vote_down   = content_arr[i][6].replace('\'', ''),
            comment_cnt = _comment_cnt
        )
        item_queue.put(item)


def calc_finger(item):
    data = item['id'] + item['img_src'] + item['created']
    m = md5.md5()
    m.update(data)
    return m.hexdigest()[0:16]


def do_download(download_queue, item_queue, url):
    next_page = url
    while True:
        html_data = get_url_content(next_page)
        print "download:[%s]" % next_page
        save_cache(url, html_data)
        download_queue.put(next_page)
        pattern = r'<div class="pagebar clearfix">.+?<a class="next" href="(.+?)".+?</div>'
        m = re.compile(pattern, re.DOTALL)
        link_next_page = m.findall(html_data)
        if len(link_next_page) > 0:
            next_page = 'http://www.qiushibaike.com' + link_next_page[0]
            continue
        else:
            print "*******downloader becomming a parser*******"
            do_parse(download_queue, item_queue)
    sys.exit(0)


class Recorder:
    def __init__(self):
        self.conn = sqlite3.connect('./qiubai.db', check_same_thread = False)
        self.cur = self.conn.cursor()

    def save_item(self, item):
        finger = calc_finger(item)
        if self.is_existed_finger(finger):
            return False
        sql = "insert into t_qiushi (id, content, img_src, img_desc, vote_up, vote_down, comment_cnt, created, finger) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item['id'], item['content'], item['img_src'], item['img_desc'], item['vote_up'], item['vote_down'], item['comment_cnt'], item['created'], finger)
        try:
            self.cur.execute(sql)
        except:
            print 'Save data error.[%s]' % sql
            return False
        try:
            self.conn.commit()
        except sqlite3.OperationalError, e:
            print "Error when commit:[%s]." % e.message
        return True

    def is_existed_finger(self, finger):
        sql = "select count(1) from t_qiushi where finger = '%s'" % finger
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        cnt = int(rows[0][0])
        return True if cnt > 0 else False


def do_parse(download_queue, item_queue):
    while True:
        try:
            url = download_queue.get_nowait()
        except Empty, e:
            print "download_queue is empty, sleep a while."
            time.sleep(random.random())
            continue
        parse_qiubai(item_queue, open(os.path.join(CACHE_PATH, hash_url(url))).read())
        delete_cache(url)
        print "parsed:[%s]" % url


def do_save(item_queue):
    recorder = Recorder()
    while True:
        try:
            item = item_queue.get_nowait()
        except Empty, e:
            print "item_queue is empty. sleep a while."
            time.sleep(random.randrange(10, 20))
            continue
        recorder.save_item(item)


#TODO: 1. when downloader is finished, how to notice parser ?
#      2. when parser is finished, how to notice recorder ?
# parser: if download_queue is empty and downloader is dead, then quit.
# recorder: if item_queue is empty and parser is dead, then quit.
def start_qiubai():
    downloader = multiprocessing.Process(target = do_download, 
            args=(download_queue, item_queue, 'http://www.qiushibaike.com',))

    parser1 = multiprocessing.Process(target = do_parse, 
            args=(download_queue, item_queue))

    parser2 = multiprocessing.Process(target = do_parse, 
            args=(download_queue, item_queue))

    saver   = multiprocessing.Process(target = do_save,
            args=(item_queue, ))

    downloader.start()
    parser1.start()
    parser2.start()
    saver.start()


if __name__ == '__main__':
    start_qiubai()
