#!/usr/bin/evn python
# -*- encoding: utf-8 -*-
import os
import tempfile


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")  # 去除尾部 \ 符号

    # 判断路径是否存在
    # 存在 True
    # 不存在 False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + u' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + u' 目录已存在'
        return False


# 定义要创建的目录
mkpath = u"E:/test/one/6月"
# 调用函数
mkdir(mkpath)

tempPath = tempfile.gettempdir()                       # 获得系统临时文件路径
modernFilePath = os.path.realpath(__file__)           # 获得当前脚本所在目录
filename = os.path.basename(modernFilePath)          # 获得文件名
filepath = os.path.dirname(modernFilePath)          # 文件路径
extensionName = os.path.splitext(modernFilePath)[1]# 获得扩展名(后缀)
