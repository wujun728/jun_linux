# -*- coding: utf-8 -*-

import os

# 列出当前目录
def ls():
    for item in os.listdir(os.getcwd()):
        print item

# 切换到指定目录
def cd(dir):
    os.chdir(dir)

# 查看当前路径
def pwd():
    print os.getcwd()
