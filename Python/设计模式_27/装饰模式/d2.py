#!/usr/bin/python
# -*- coding:UTF-8 -*-

__author__ = "王志鹏"

from functools import wraps
def decorator(func):
    @wraps(func)
    def inner_function():
        pass
    return inner_function

@decorator
def func():
    pass

print(func.__name__)

#输出： func