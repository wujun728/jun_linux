#!/usr/bin/python
# -*- coding:UTF-8 -*-

# 原型模式

import copy
__author__ = "王志鹏"

def printInfo(info):
    print unicode(info, 'utf-8').encode('UTF-8')


# 拷贝接口
class ICloneable:
    def shallowClone(self):
        return copy.copy(self)

    def deepClone(self):
        return copy.deepcopy(self)


# 工作经历
class WorkExperience(ICloneable):
    workData = ""
    company = ""
    pass


# 简历
class Resume(ICloneable):
    name = ""
    sex = '未知'
    age = 0
    work = None

    def __init__(self, name, work=WorkExperience()):
        self.name = name
        self.work = work;

    def setPersonInfo(self, sex, age):
        self.sex = sex
        self.age = age

    def setWorkExperience(self, workData, company):
        self.work.workData = workData
        self.work.company = company

    def display(self):
        printInfo('%s, %s, %d' % (self.name, self.sex, self.age))
        printInfo('%s, %s' % (self.work.workData, self.work.company))


def clientUI():
    a = Resume('大鸟')
    a.setPersonInfo('男', 29)
    a.setWorkExperience("1998-2000", "XX公司")

    # 浅拷贝
    # b = a.shallowClone()
    # b.setWorkExperience("2000-2006", "YY公司")

    # 深拷贝
    c = a.deepClone()
    # c.setWorkExperience("2006-2009", "ZZ公司")

    # a.display()
    # b.display()
    c.display()
    return
    #浅拷贝，所以对象没有被复制，导致新对象的修改影响了原来的就对象的值
    #深拷贝,所以不会影响之前的旧对象
if __name__ == '__main__':
    clientUI();
