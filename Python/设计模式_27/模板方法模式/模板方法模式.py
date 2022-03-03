#!/usr/bin/python
# -*- coding:UTF-8 -*-

__author__ = "王志鹏"

"""
大话设计模式
设计模式——模板方法模式
模板方法模式(Template Method Pattern):定义一个操作中的算法骨架，将一些步骤延迟至子类中.模板方法使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤
使用场景:当不变和可变的行为在方法的子类实现中混合在一起时,不变的行为就会在子类中重复出现，用模板方法模式把这些不变的行为搬到单一的地方,帮助子类摆脱重复不变的行为纠缠
"""


class TestPaperA:
    def question1(self):
        print "杨过得到,后来给了郭靖,炼成倚天剑,屠龙刀的玄铁可能是[]"
        print "a.球墨铸铁 b.马口铁 c.高速合金钢 d.碳素纤维"

        print "答案b"

    def question2(self):
        print "杨过, 程英, 陆无双铲除了情花,照成[]"
        print "a.使这种植物不在害人 b.使一种珍惜物种灭绝 c.破坏了生物圈的生态平衡 d.造成地区沙漠化"

        print "答案a"

    def question3(self):
        print "蓝凤凰致使华山师徒, 桃谷六仙呕吐不止如果你是大夫,会给他们开什么药?[]"
        print "a.阿司匹林 b.牛黄解毒片 c.氟哌酸 d.让他们和大量的生牛奶 e.以上都不对"

        print "答案c"


class TestPaperB:
    def question1(self):
        print "杨过得到,后来给了郭靖,炼成倚天剑,屠龙刀的玄铁可能是[]"
        print "a.球墨铸铁 b.马口铁 c.高速合金钢 d.碳素纤维"

        print "答案b"

    def question2(self):
        print "杨过, 程英, 陆无双铲除了情花,照成[]"
        print "a.使这种植物不在害人 b.使一种珍惜物种灭绝 c.破坏了生物圈的生态平衡 d.造成地区沙漠化"

        print "答案a"

    def question3(self):
        print "蓝凤凰致使华山师徒, 桃谷六仙呕吐不止如果你是大夫,会给他们开什么药?[]"
        print "a.阿司匹林 b.牛黄解毒片 c.氟哌酸 d.让他们和大量的生牛奶 e.以上都不对"

        print "答案c"


# 第进化版
class NewPaper:
    def question1(self):
        print "杨过得到,后来给了郭靖,炼成倚天剑,屠龙刀的玄铁可能是[]"+ self.answer1()
        print "a.球墨铸铁 b.马口铁 c.高速合金钢 d.碳素纤维"
        # print  self.answer1()
    def question2(self):
        print "杨过, 程英, 陆无双铲除了情花,照成[]" + self.answer2()
        print "a.使这种植物不在害人 b.使一种珍惜物种灭绝 c.破坏了生物圈的生态平衡 d.造成地区沙漠化"

    def question3(self):
        print "蓝凤凰致使华山师徒, 桃谷六仙呕吐不止如果你是大夫,会给他们开什么药?[]" + self.answer3()
        print "a.阿司匹林 b.牛黄解毒片 c.氟哌酸 d.让他们和大量的生牛奶 e.以上都不对"

    def answer1(self):
        return "cc"

    def answer2(self):
        return "vv"

    def answer3(self):
        return "bb"

class studentA(NewPaper):
    def answer1(self):
        return "答案?"

    def answer2(self):
        return '答案?'

    def answer3(self):
        return '答案?'


class studentB(NewPaper):
    def answer1(self):
        return "答案b"

    def answer2(self):
        return '答案c'

    def answer3(self):
        return '答案a'


if __name__ == '__main__':
    # a = TestPaperA()
    # a.question1()
    # a.question2()
    # a.question3()
    # print "==============================="
    # b = TestPaperB()
    # b.question1()
    # b.question2()
    # b.question3()
    # print "+++++++++++"
    studenta = studentA()

    studenta.question1()
    studenta.question2()
    studenta.question3()
    print "=======学生b========"
    studentb = studentB()
    studentb.question1()
    studentb.question2()
    studentb.question3()
