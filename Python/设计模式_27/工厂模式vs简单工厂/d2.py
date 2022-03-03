#!/usr/bin/python
# -*- coding:UTF-8 -*-

__author__ = "王志鹏"

class LeiFeng():
    def buy_rice(self):
        pass

    def sweep(self):
        pass


class Student(LeiFeng):
    def buy_rice(self):
        print '大学生帮你买米'

    def sweep(self):
        print '大学生帮你扫地'


class Volunteer(LeiFeng):
    def buy_rice(self):
        print '社区志愿者帮你买米'

    def sweep(self):
        print '社区志愿者帮你扫地'


class LeiFengFactory():
    def create_lei_feng(self, type):
        map_ = {
            '大学生': Student(),
            '社区志愿者': Volunteer()
        }
        return map_[type]


if __name__ == '__main__':
    #简单工厂
    leifeng1 = LeiFengFactory().create_lei_feng('大学生')
    leifeng2 = LeiFengFactory().create_lei_feng('大学生')
    leifeng3 = LeiFengFactory().create_lei_feng('大学生')
    leifeng1.buy_rice()
    leifeng1.sweep()