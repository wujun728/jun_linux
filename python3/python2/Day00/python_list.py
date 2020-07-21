""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/14 13:37
# @Author  : iByte
# <Python 针对List的一些操作>


class PList:
    def python_list(self):
        list = [1, 4, 3, 3, "A", "B", "c", "A"]

        # 增加
        list.append("AA")  # 像末尾增加一个新元素
        list.insert(1, "B")  # 像指定索引位置插入元素
        list.extend(["D", "DD"])  # 新列表每个元素增加到list中

        # 修改
        # list[0] = "updata"  # 修改指定元素的值
        # list[1:] = "sss"  # 修改指定索引位置后的全部数据
        # list[-1]  # 取得倒数第一个元素值
        # list[1:3]  # 左包含,右边不包含 生成新的[]
        a = "a"
        print(a.title())  # 字母大写

        # list搜索
        print(list.index("D"))  # 指定元素的索引位置
        print("A" in list)  # 判断指定元素是否存在list中 返回 True/False

        # 删除
        print(list.pop(0))  # 删除指定索引位置元素并返回删除元素
        print(list.pop())  # 删除末尾元素
        del list[0]  # 删除指定索引位置元素
        list.remove("A")  # 删除指定元素 注:只会找到第一个相同元素删除, list 中没有找到值, Python 会引发一个异常

        # list排序
        list.sort(reverse=True)  # sort永久性排序,reverse=True 倒序
        _list = sorted(list, reverse=True)  # 临时性,reverse=True 倒序

        # list运算符
        list = list + ['example', 'new']  # 增加
        list += [1, 2] * 3  # list可以进行复制元素,并累加

        # list中规律增加字符串
        lists = ["A", "B", "C"]
        strlist = ";".join(lists)  # A;B;C
        print
        strlist

        # list 去重
        ids = [1, 4, 3, 3, 4, 2, 3, 4, 5, 6, 1]
        func = lambda x, y: x if y in x else x + [y]
        # lists = reduce(func, [[], ] + ids)
        print(lists)

        ## 创建数值列表
        number1 = list(range(1, 6))
        print(number1)

        number2 = list(range(1, 11, 2))
        print(number2)


if __name__ == '__main__':
    # pl = PList()
    # pl.python_list()

    list = [1, 4, 3, 3, 6, 7, 11, 3, 55, 6, 9]
    list.sort(reverse=True)
    print(list)
