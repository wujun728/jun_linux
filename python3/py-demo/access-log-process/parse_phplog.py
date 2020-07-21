# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import os
import argparse
import json

class LogPipe():
    """
    初始化
    logfile ：目标日志文件路径，绝对路径
    posfile : 读取位置记录文件
    """
    TRACE_SEPARATE = ' '
    POS_SEPARATE = '\t'
    NEW_LINE = '\n'

    posdict = {}
    posinfo = {}  # 当前目标文件的pos信息
    posformat = r'^(?P<filepath>[^\t]+)\t(?P<pos>[0-9a-fA-F]+)\t(?P<time>[0-9a-fA-F]+)$'  # 默认的pos文件格式

    def __init__(self, logfile, posfile, posformat=None):
        self.logfile = logfile
        self.posfile = posfile
        if posformat:
            self.posformat = posformat
        self.logtime = int(os.path.getatime(self.logfile))  # 日志文件更新时间

    def run(self, logformat):
        """
        从pos文件读取日志文件上次读取位置信息
        :return:
        """
        newlogs = ''
        self.posdict = self._getposdict()
        if not self.posdict.has_key(self.logfile):
            # print u'初次写入pos信息行'
            self.posdict[self.logfile] = {'pos': 0, 'time': 0}
            #self.updata_posinfo()

        self.posinfo = self.posdict[self.logfile]

        # 检测日志文件是否更新
        if self.logtime == self.posinfo['time']:
            # print u"文件未更新"
            return newlogs

        #根据目标日志文件中新增的行
        for logitem in self.readnewlines(self.logfile, self.posinfo['pos']):
            logitem = logitem.replace('\n', self.TRACE_SEPARATE)
            itemjson = self.linetojson(logitem, logformat) + self.NEW_LINE
            newlogs += itemjson
        self.updata_posinfo()
        return newlogs

    def readnewlines(self, tagetfile, lastpos):
        """
        行迭代读取目标文件产生的新行，迭代返回
        """
        with open(tagetfile, 'r') as logfile:
            logfile.seek(lastpos, 1)
            onelog = ''
            for line in logfile:
                if line == '\n':
                    yield onelog
                    onelog = ''
                else:
                    onelog += line
            yield onelog
            pos = logfile.tell()
            if lastpos < pos:
                lastpos = pos
        # 更新pos文件
        self.posdict[tagetfile] = {'pos': str(pos), 'time': str(self.logtime)}


    def _getposdict(self):
        """
        获取并解析pos文件中的信息
        :return:
        """
        lines = {}
        def singleline_process(line):
            linepattern = re.compile(self.posformat)
            matches = linepattern.match(line)
            if matches != None:
                linedict = matches.groupdict()
                lines[linedict['filepath']] = {'pos': int(linedict['pos']), 'time': int(linedict['time'])}

        with open(self.posfile) as f:
            for line in f:
                singleline_process(line)
        return lines

    def updata_posinfo(self):
        content = ''
        for linetuple in self.posdict.items():
            filepath = linetuple[0]
            pos = linetuple[1]['pos']
            time = linetuple[1]['time']
            content += (filepath + self.POS_SEPARATE + str(pos) + self.POS_SEPARATE + str(time) + self.NEW_LINE)
        with open(self.posfile, 'w') as f:
            f.write(content)

    def linetojson(self, item, logformat):
        """
        解析单行日志为json
        """
        jsonstr = ''
        itempattern = re.compile(logformat)
        matches = itempattern.match(item)
        if matches != None:
            linedict = matches.groupdict()
            jsonstr = json.dumps(linedict, ensure_ascii=False).encode('utf8')
        return jsonstr
    
if __name__ == "__main__":
    """
    入口调用
    example:
        python parse_phplog.py temp/phplog2.pos temp/phplog2.log
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("posfile", help=u"输入pos file路径")
    parser.add_argument("logfile", help=u"输入log file路径")
    args = parser.parse_args()
    posfile = args.posfile
    logfile = args.logfile

    posfile_format = r'^(?P<filepath>[^\t]+)\t(?P<pos>[0-9a-fA-F]+)\t(?P<time>[0-9a-fA-F]+)$'
    logformat = r'^\[(?P<app_name>[^\]]*)\]\[(?P<log_level>[^\]]*)\]\[(?P<timestamp>[^\]]*)\]\[(?P<server_ip>[^\]]*)\]\[(?P<server_host>[^\]]*)\]\[(?P<req_ip>[^\]]*)\]\[(?P<pid>[^\]]*)\]\[(?P<log_id>[^\]]*)\]\[(?P<method>[^\]]*)\]\[(?P<uri>[^\]]*)\]\[(?P<exec_time>[^\]]*)\]\[(?P<step_time>[^\]]*)\]\[(?P<code_line>[^\]]*)\](?P<back_trace>[^\n]*)$'

    if os.path.exists(logfile) != True:
        print 'Sorry, I cannot find the "%s" file.' % logfile
        exit()
    if os.path.exists(posfile) != True:
        print 'Sorry, I cannot find the "%s" file.' % logfile
        exit()

    posfilepath = os.path.abspath(posfile)
    logfilepath = os.path.abspath(logfile)

    logpipe = LogPipe(logfilepath, posfilepath, posfile_format)
    newlogs = logpipe.run(logformat)
    print newlogs

