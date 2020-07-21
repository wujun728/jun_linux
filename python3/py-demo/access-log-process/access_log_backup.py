#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
access-log-backup - Read web server access log file and parse and backup to mongodb.
调用示例:
    python access_log_backup.py api api c:/usr/temp/api.log

导入日志示例：
- - 10.159.95.148 - [07/Jan/2015:00:01:05 +0800] "GET /mo/car/yQi0kiEXuhhu HTTP/1.0" 200 95387 "-" "Mozilla/5.0 ..." "115.28.203.70" 0.470 "00d0fc152227a402034f5074d1f484b9" "-"
导入生成的mongodb document：
{
   "_id": ObjectId("54b1067de77989a5350018de"),
   "http_x_real_ip": "-",
   "http_clientip": "-",
   "remote_addr": "192.168.1.72",
   "remote_user": "-",
   "time_local": "10/Jan/2015:19:01:15 +0800",
   "http_method": "GET",
   "path": "/mo/car/yQi0kiEXuhhu",
   "http_code": "304",
   "bytes_size": "0",
   "referer": "-",
   "user_agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
   "http_x_forwarded_for": "-",
   "request_time": "0.000",
   "sent_http_log_id": "-",
   "sent_http_uv_id": "-",
   "time": ISODate("2015-01-10T11:01:15.0Z")
}

"""

__author__ = 'Nob (sddenter@gmail.com)'
__version__ = '1.0'

import time
import os
import sys
import re
import argparse
from pymongo import MongoClient

#根据 nginx access-format 自定义的正则
access_main_format = r'^(?P<http_x_real_ip>[^ ]*) (?P<http_clientip>[^ ]*) (?P<remote_addr>[^ ]*) ' \
                     '(?P<remote_user>[^ ]*) \[(?P<time_local>[^\]]*)\] "(?P<http_method>\S+)(?: +(?P<path>[^\"]*) +\S*)?" ' \
                     '(?P<http_code>[^ ]*) (?P<bytes_size>[^ ]*)(?: "(?P<referer>[^\"]*)" "(?P<user_agent>[^\"]*)") ' \
                     '"(?P<http_x_forwarded_for>[^\"]*)" (?P<request_time>[^ ]*) "(?P<sent_http_log_id>[^\"]*)" ' \
                     '"(?P<sent_http_uv_id>[^\"]*)"?$'
access_api_format = r'^(?P<http_x_real_ip>[^ ]*) (?P<http_clientip>[^ ]*) (?P<remote_addr>[^ ]*) (?P<remote_user>[^ ]*) \[(?P<time_local>[^\]]*)\] "(?P<http_method>\S+)(?: +(?P<path>[^\"]*) +\S*)?" (?P<http_code>[^ ]*) (?P<bytes_size>[^ ]*)(?: "(?P<referer>[^\"]*)" "(?P<user_agent>[^\"]*)") "(?P<http_x_forwarded_for>[^\"]*)" (?P<request_time>[^ ]*) "(?P<sent_http_log_id>[^\"]*)" "(?P<sent_http_uv_id>[^\"]*)" "(?P<platform_pp>[^\"]*)" "(?P<build_pp>[^\"]*)" "(?P<system_version_pp>[^\"]*)" "(?P<system_sdk_pp>[^\"]*)" "(?P<screen_width_pp>[^\"]*)" "(?P<screen_height_pp>[^\"]*)" "(?P<screen_density_pp>[^\"]*)" "(?P<channel_id_pp>[^\"]*)" "(?P<mobile_model_pp>[^\"]*)" "(?P<network_pp>[^\"]*)" "(?P<uuid>[^\"]*)" "(?P<imei>[^\"]*)"?$'


def read_logfile(filename, re_format, write_callback):
    """
    读取文件每行记录，并进行回调处理
    :param filename:
    :param re_format:
    :param write_callback:
    :return:
    """
    line_count = 0
    with open(filename) as logfile:
        for line in logfile:
            logdict = parse_single_line(line, re_format)
            if logdict == None:
                continue
            write_callback(logdict)
            line_count += 1
    return line_count


def parse_single_line(line, re_format):
    """
    解析一行日志
    :param line:
    :param re_format:
    :return:
    """
    access_log_pattern = re.compile(re_format)
    matches = access_log_pattern.match(line)
    if matches != None:
        groups = matches.groupdict()
        return groups
    return None


def main(filename, re_format, mongo):
    """
    核心方法：打开mongo连接，读取文件，写入mongo
    :param filename:
    :param re_format:
    :param mongo_server:
    :return:
    """
    starttime = time.time()
    with MongoClient(mongo['server']) as client:
        db = client[mongo['dbname']]
        collection = db[mongo['collection']]

        def write_callback(document):
            collection.insert(document)
            pass

        line_count = read_logfile(filename, re_format, write_callback)
    spend = int(time.time() - starttime)
    print "tatal: %d , spend: %d s" % (line_count, spend)


if __name__ == "__main__":
    """
    入口调用
    example:
    python access_log_backup.py api api c:/usr/temp/api.log

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("logtype", help=u"[api | main]日志类型,取值对应nginx.conf中配置的日志name")
    parser.add_argument("logcollection", help=u"存放日志的mongodb集合，请和td-agent.conf中的配置对应")
    parser.add_argument("logfile", help=u"nginx访问日志文件路径")
    args = parser.parse_args()
    logtype = args.logtype
    logcollection = args.logcollection
    logfile = args.logfile
    
    if logtype == 'api':
        re_format = access_api_format
    elif logtype == 'main':
        re_format = access_main_format
    else:
        parser.print_help()
        exit()
    if os.path.exists(logfile) != True:
        print 'Sorry, I cannot find the "%s" file.' % logfile
        exit()

    mongo_config = {
        'server': "mongodb://localhost:27017",
        'dbname': "nginxlogs",
        'collection': logcollection,
    }
    print "runing ..., wait please!"
    main(logfile, re_format, mongo_config)