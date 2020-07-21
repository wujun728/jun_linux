# -*- coding: utf-8 -*-

""""
查找文件只用到三个匹配符："*", "?", "[]"。"*"匹配0个或多个字符；"?"匹配单个字符；"[]"匹配指定范围内的字符，如：[0-9]匹配数字。
"""

import os
import glob

# 返回一个列表
print glob.glob(r'/home/sudongdong/*/*.sh')

# 返回一个可迭代的对象,<generator object iglob at 0x7f8eba1105f0>
print glob.iglob(r'/home/sudongdong/*/*.sh')
for file in glob.iglob(r'/home/sudongdong/*/*.sh'):
    print file