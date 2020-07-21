#!/bin/env python
import os, sys, time, logging

class Base(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        _repr = "{klass}({name})".format(klass=self.__class__.__name__, name=self.name)
        return _repr


class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class MyObject(ObjectDict):
    def __init__(self):
        pass


def main():
    o = MyObject()
    o.aa= 'bb'
    o.cc = 'dd'
    print o

    #base = Base("hello")
    #print base


if __name__ == '__main__':
    main()
