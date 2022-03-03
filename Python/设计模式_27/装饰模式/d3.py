#!/usr/bin/python
# -*- coding:UTF-8 -*-
from functools import wraps

__author__ = "王志鹏"


def decorator(func):
    @wraps(func)  # 防止丢失自身信息
    def inner_function():
        pass
    return inner_function


@decorator
def func():
    pass


print(func.__name__)

# 输出： inner_function
