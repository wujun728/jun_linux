#!/bin/env python
from pymongo import MongoClient
import time

c = MongoClient()

db = c['v2ex']

cur_time = time.time() - 8 * 60 * 60

cur = db.topic.find({"created":{"$gt":cur_time}, "replies":{"$gt":0}}).sort("replies", -1).limit(8)

data = cur.next()

for data in cur:
    print 80 * '-'
    print "reply count:", data['replies']
    print "url:", data['url']
    print "create time:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(data['created']))
    print "title:", data['title']
    print "content:", data['content']
