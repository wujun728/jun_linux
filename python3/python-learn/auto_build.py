#-*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xlrd, os
import telnetlib
import string
from xlutils.copy import copy
import logging
from subprocess import Popen
import commands
from StringIO import StringIO
import time
import socket

DEFAULT_HOST = "1.2.3.4"
DEFAULT_USER = "user"
DEFAULT_PASS = "passwd"

LOG_SERV_ADDR = ('136.24.8.45', 1989)

STR_MAX_SIZE = 32700

EXPIRED_TIME = 300

OUTPUT_FILE = "output.xls"

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def parse_excel(filename):
    read_book = xlrd.open_workbook(filename);
    write_book = copy(read_book)
    read_sheets = read_book.sheets()
    for i in range(len(read_sheets)):
        parse_sheet(read_sheets[i], write_book.get_sheet(i))
    write_book.save(OUTPUT_FILE)

def parse_sheet(read_sheet, write_sheet):
    for i in range(read_sheet.nrows):
        if i < 1:continue # skip head
        bin_name = read_sheet.cell_value(i, 0).encode('gbk').split('.')[0]
        source_path = read_sheet.cell_value(i, 1).encode('gbk')
        bin_path = read_sheet.cell_value(i, 2).encode('gbk')
        build_log = build_program(source_path, bin_path, bin_name)
        build_flag = check_bin(bin_path, bin_name)
        is_running = check_running_on_product(bin_name)
        product_log = check_running_log(bin_name)
        remote_log  = check_remote_log(bin_name)
        print 80 * '-'
        logging.info(bin_name)
        logging.info(source_path)
        logging.info(bin_path)
        logging.info(build_log)
        logging.info(build_flag)
        logging.info(is_running)
        logging.info(product_log)
        logging.info(remote_log)
        print 80 * '-'
        # write result to xls out file
        write_sheet.write(i, 3, build_log[0:STR_MAX_SIZE])
        write_sheet.write(i, 4, build_flag)
        write_sheet.write(i, 5, is_running)
        write_sheet.write(i, 6, product_log)
        write_sheet.write(i, 7, remote_log)


def build_program(source_path, bin_path, bin_name):
    build_cmd = "cd " + source_path + " && make clean && make " + bin_name
    build_log = commands.getoutput(build_cmd)
    ret = []
    # skip chinese
    for i in range(len(build_log)):
        v = ord(build_log[i]) 
        if v < 0x20 or v > 0x7e:
            continue
        ret.append(build_log[i])
    return ''.join(ret)

def check_bin(bin_path, bin_name):
    f = os.path.join(bin_path, bin_name)
    if not os.path.exists(f):
        return "FAIL"
    diff = time.time() - os.path.getctime(f)
    if diff > EXPIRED_TIME:
        return "FAIL"
    return "SUCC"

def check_running_on_product(bin_name):
    cmd = "ps -ef|grep -v grep|grep " + bin_name
    ret = do(cmd)
    running_flag = "No"
    # skip first line
    if ret[ret.find('\n')+1:].find(bin_name) != -1:
       running_flag = "Yes" 
    return running_flag

def check_running_log(bin_name):
    #cmd = "l /ibss?/run/log/" + bin_name + ".log|awk '{sum+=$5}END{print sum}'"
    cmd = "l /ibss?/run/log/" + bin_name + ".log|awk '{print $5}'"
    ret = StringIO(do(cmd))
    ret_running_log = "NO LOG"
    line_sum = 0
    for line in ret.readlines():
        if line.isdigit():
            line_sum = line_sum + int(line)
    if line_sum > 0:
        ret_running_log = "HAS LOG"
    ret.close()
    return ret_running_log

def check_remote_log(program_name):
    serv_addr = LOG_SERV_ADDR
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serv_addr)
    cmd =  "find /crmbak -name %s.log.gz -mtime 30 2>/dev/null |xargs ls -l --block-size=1024 |grep %s.log.gz$ 2>/dev/null |awk '{sum+=$5}END{print sum}'" % (program_name, program_name)
    s.send(cmd)
    data = s.recv(1024)
    s.close()
    return data

def telnetdo(host, user, passwd, command):
    tn = telnetlib.Telnet()
    try:
        tn.open(host)
    except:
        logging.error("telnet open error")
        return
    tn.read_until("login:")
    tn.write(user.encode('UTF-8') + '\n')
    ReadPasswd=tn.read_until(":")
    if(string.find(ReadPasswd,"Password:") or string.find(ReadPasswd,"password:")):
        tn.write(passwd.encode('UTF-8') + '\n')
    else:
        logging.error("cannot input passwd")
        return
    finish_flag = ('>')
    tn.read_until(finish_flag)
    tn.write(command.encode('UTF-8') + '\r\n')
    result = tn.read_until(finish_flag)
    tn.close()
    return result

def do(cmd):
    return telnetdo(DEFAULT_HOST, DEFAULT_USER, DEFAULT_PASS, cmd)

if __name__ == '__main__':
    #res = check_running_log("R2319Cfm")
    #print res
    #print "-" * 80
    #res = check_running_on_product("R2319Cfm")
    #print res
    #res = build_program('/ibss1/run/cfile', '/ibss1/run/bin' , 'R2319Cfm')
    #print res
    #res = check_bin('/ibss1/run/bin', 'R2319Cfm')
    #print res.find("Last modified")
    #print res
    #cmd = "cd /ibss1/run/cfile && make clean && make R2319Cfm"
    #res = commands.getoutput(cmd)
    #print res
    update_excel("69.xls")
