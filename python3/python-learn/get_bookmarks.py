#!/usr/bin/env python
#-*- coding=utf-8 -*-

from xml.dom import minidom
import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''
    date    2013-07-20 18:39:01
    desc    convert delicious xml file to boo markdown format
'''

def parse(xmlfile, outfile):
    dom = minidom.parse(xmlfile)
    root = dom.documentElement
    l = root.getElementsByTagName("post")
    f = open(outfile, "a")
    for i in l:
        link = i.getAttribute("href").decode('utf8')
        desc = i.getAttribute("description").decode('utf8')
        short = ""
        if len(desc) < 7:
            short = link[:25] + ">>"
        else:
            short = desc[:25] + ">>"
        record = "[" + short + "](" + link + " \"" + desc + "\")\n\n"
        f.write(record)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python get_bookmarks.py outfile"
        sys.exit(127)
    parse("delicious.xml", sys.argv[2].strip())
