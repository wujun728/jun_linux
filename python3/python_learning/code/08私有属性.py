'''
Created on 2018年10月10日

@author: Administrator
'''
class Person(object):
    
    def __init__(self, name,age):
        self.__name=name
        self.age=age
    def setName(self,name):
        if len(name)>5:
            self.__name=name
        else:
            print("名字长度不符合规则")
    def getName(self):
        return self.__name
    def __test(self):
        print("test")
    def test2(self):
        self.__test()
p=Person("abcdefg",3)
# print(p.__name)
print(p.getName())
p.setName("abcd")
print(p.getName())
# p.__test()
p.test2()