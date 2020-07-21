# -*- coding: utf-8 -*-


# !/usr/bin/env python
#coding:utf8
import re

import MySQLdb

#日志的位置
logfile = open("access.log")
#使用的nginx默认日志格式$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"'
#日志分析正则表达式
#203.208.60.230
ipP = r"?P<ip>[\d.]*"
#以[开始,除[]以外的任意字符 防止匹配上下个[]项目(也可以使用非贪婪匹配*?) 不在中括号里的.可以匹配换行外的任意字符 *这样地重复是"贪婪的“ 表达式引擎会试着重复尽可能多的次数。#以]结束
#[21/Jan/2011:15:04:41 +0800]
timeP = r"""?P<time>\[[^\[\]]*\]"""
#以"开始, #除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?),#以"结束
#"GET /EntpShop.do?method=view&shop_id=391796 HTTP/1.1"
#"GET /EntpShop.do?method=view&shop_id=391796 HTTP/1.1"
requestP = r"""?P<request>\"[^\"]*\""""
statusP = r"?P<status>\d+"
bodyBytesSentP = r"?P<bodyByteSent>\d+"
#以"开始, 除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?),#以"结束
#"http://test.myweb.com/myAction.do?method=view&mod_id=&id=1346"
referP = r"""?P<refer>\"[^\"]*\""""
#以"开始, 除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?),以"结束
#"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
userAgentP = r"""?P<userAgent>\"[^\"]*\""""
#以(开始, 除双引号以外的任意字符 防止匹配上下个()项目(也可以使用非贪婪匹配*?),以"结束
#(compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
userSystems = re.compile(r'\([^\(\)]*\)')
#以"开始，除双引号以外的任意字符防止匹配上下个""项目(也可以使用非贪婪匹配*?),以"结束
userlius = re.compile(r'[^\)]*\"')
#原理：主要通过空格和-来区分各不同项目，各项目内部写各自的匹配表达式
access_format = r"(%s)\ -\ -\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)" % (ipP, timeP, requestP, statusP, bodyBytesSentP, referP, userAgentP)
print access_format
nginxLogPattern = re.compile(access_format, re.VERBOSE)

exit()
#数据库连接信息
# conn = MySQLdb.connect(host='192.168.1.22', user='test', passwd='pass', port=3306, db='python')
# cur = conn.cursor()
# sql = "INSERT INTO python.test VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

while True:
    line = logfile.readline()
    if not line: break
    matchs = nginxLogPattern.match(line)
    if matchs != None:
        allGroup = matchs.groups()
        ip = allGroup[0]
        time = allGroup[1]
        request = allGroup[2]
        status = allGroup[3]
        bodyBytesSent = allGroup[4]
        refer = allGroup[5]
        userAgent = allGroup[6]
        Time = time.replace('T', ' ')[1:-7]
        if len(userAgent) > 20:
            userinfo = userAgent.split(' ')
            userkel = userinfo[0]
            try:
                usersystem = userSystems.findall(userAgent)
                usersystem = usersystem[0]
                print usersystem
                userliu = userlius.findall(userAgent)
                value = [ip, Time, request, status, bodyBytesSent, refer, userkel, usersystem, userliu[1]]
                print value
            except IndexError:
                userinfo = userAgent
                value = [ip, Time, request, status, bodyBytesSent, refer, userinfo, "", ""]
        else:
            useraa = userAgent
            value = [ip, Time, request, status, bodyBytesSent, refer, useraa, "", ""]
    try:
        print str(value)
#        result = cur.execute(sql, value)
        #conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# conn.commit()
# conn.close()