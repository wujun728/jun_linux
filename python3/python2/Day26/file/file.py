""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/14 14:10
# @Author  : iByte
# !/usr/bin/python
# -*-coding:utf-8-*-       #指定编码格式，python默认unicode编码

import os
import operator

directory = "E:/demo"
os.chdir(directory)  # 切换到directory目录
cwd = os.getcwd()  # 获取当前目录即dir目录下
print("------------------------current working directory------------------")


def deleteBySize(minSize):
    """删除小于minSize的文件（单位：K）"""
    files = os.listdir(os.getcwd())  # 列出目录下的文件
    for file in files:
        if os.path.getsize(file) < minSize * 1000:
            os.remove(file)  # 删除文件
            print(file + " deleted")
    return


def deleteNullFile():
    '''删除所有大小为0的文件'''
    files = os.listdir(os.getcwd())
    for file in files:
        if os.path.getsize(file) == 0:  # 获取文件大小
            os.remove(file)
            print(file + " deleted.")
    return


def create():
    '''根据本地时间创建新文件，如果已存在则不创建'''
    import time
    t = time.strftime('%Y-%m-%d', time.localtime())  # 将指定格式的当前时间以字符串输出
    suffix = ".docx"
    newfile = t + suffix
    if not os.path.exists(newfile):
        f = open(newfile, 'w')
        print
        newfile
        f.close()
        print
        newfile + " created."
    else:
        print
        newfile + " already existed."
    return


hint = '''funtion:
            1   create new file
            2   delete null file
            3   delete by size
please input number:'''

if __name__ == '__main__':

    while True:
        option = input(hint)  # 获取IO输入的值
        if operator(option, '1') == 0:
            create()
        elif operator(option, '2') == 0:
            deleteNullFile()
        elif operator(option, '3') == 0:
            minSize = input("minSize(K):")
            deleteBySize(minSize)
        elif cmp(option, 'q') == 0:
            print
            "quit !"
            break
        else:
            print("disabled input ,please try again....")
