'''
Created on 2018年10月10日

@author: Administrator
'''
class Person(object):
    name="zhangsan"
#     def __init__(self, name,age):
#         self.name=name
#         self.age=age
    @classmethod
    def test(cls):
        print("类方法")
    def test2(self):
        print("test2")
    @staticmethod
    def test3():
        print("test3")
# p=Person("lisi",12)
# p=Person()
# print(p.name)
# p.name="wangwu"
# print(p.name)
# print(Person.name)
# Person.name="maliu"
# print(Person.name)
# print(p.name)

p=Person()
p.test()
p.test2()
p.test3()
Person.test()
# Person.test2()
Person.test3()