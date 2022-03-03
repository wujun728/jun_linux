# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os, shutil


class OperatingFile:
    def creatFile(self, path):
        f = file(path, "w+")
        f.close()

    def readFile(self, path):
        #方法一
        f = open("E:/aa.txt")
        line = f.readline()
        while line:
            print line
            line = f.readline()
        f.close()

        # 方法二
        for line2 in open(path):
            print line2

        # 方法三
        f2 = open(path, "r")
        lines = f2.readlines()
        for line3 in lines:
            print line3

    def writeFile(self, path):
        # 写入文件,会删除原文件内容,文件不存在将创建
        fo = open(path, "w")
        fo.write("www.runoob.com!\nVery good site!\n")
        fo.close()

        # 以二进制,追加写入
        fo = open(path, "ab+")
        fo.write("这里是追加写入!")
        fo.close()

    def updataFileNme(self, path):
        os.rename(path, "E:/bb.txt")

    def delFile(self, path):
        os.remove("E:/bb.txt")

    def mymovefile(self, srcfile, dstfile):
        if not os.path.isfile(srcfile):
            print "%s not exist!" % (srcfile)
        else:
            fpath, fname = os.path.split(dstfile) # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath) # 创建路径
                shutil.move(srcfile, dstfile) # 移动文件
                print "move %s -> %s" % (srcfile, dstfile)

    def mycopyfile(self, srcfile, dstfile):
        if not os.path.isfile(srcfile):
            print "%s not exist!" % (srcfile)
        else:
            fpath, fname = os.path.split(dstfile) # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath) # 创建路径
                shutil.copyfile(srcfile, dstfile) # 复制文件
                print "copy %s -> %s" % (srcfile, dstfile)

    def makedir(self,path):
        isExists = os.path.exists(path)

        if not isExists:
            os.makedirs(path)
            print path + u' 创建成功'
            return True
        else:
            print path + u' 目录已存在'
            return False

    def discern(self,path):
        for filename in os.listdir(path):
            print filename

    def main(self):
        path = "E:/aa.txt"

        # 创建文件
        self.creatFile(path)

        # 写入文件
        self.writeFile(path)

        # 读取文件
        self.readFile(path)

        # 重命名文件
        self.updataFileNme(path)

        # 删除文件
        self.delFile(path)

        # copy文件/移动文件
        srcfile="/aa/a.txt"
        dstfile="/aa/aa/copyAA.txt"
        self.mycopyfile(srcfile,dstfile)
        #移动
        dstfile = "/aa/aa/a.txt"
        self.mymovefile(srcfile,dstfile)

        #文件夹自动创建与识别
        self.makedir(path)
        #识别文件目录
        _path=u"/aa"
        self.discern(_path)


if __name__ == '__main__':
    operatingfile = OperatingFile()
    operatingfile.main()