# -*- coding:utf-8 -*-

import json,sys

#reload(sys)
#sys.setdefaultencoding('ascii')

def main():
    filename = 'sina_user.json'
    s = unicode(open(filename, 'r').read().decode('gbk'))

    obj = json.loads(s)

    users = obj['users']
    print len(users)
    for i in range(len(users)):
        print i
        print "\t", users[i]["name"].encode('gbk')
        print "\t", users[i]["location"].encode('gbk')
        print "\t", users[i]["created_at"].encode('gbk')
        print "-----------------------------------------------"

if __name__ == '__main__':
    main()
