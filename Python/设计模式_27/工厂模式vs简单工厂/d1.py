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
    def create_lei_feng(self):
        pass


class StudentFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Student()


class VolunteerFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Volunteer()


if __name__ == '__main__':
    myFactory = StudentFactory()

    leifeng1 = myFactory.create_lei_feng()
    leifeng2 = myFactory.create_lei_feng()
    leifeng3 = myFactory.create_lei_feng()

    leifeng1.buy_rice()
    leifeng1.sweep()