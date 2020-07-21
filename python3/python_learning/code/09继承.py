'''
Created on 2018年10月10日

@author: Administrator
'''
# class Animal(object):
#     def __init__(self,name):
#         self.name=name
#     def eat(self):
#         print("吃的很开心")
# class Cat(Animal):
#     def __init__(self, name,age):
#         Animal.__init__(self, name)
#         self.age=age
#     def run(self):
#         print("running")
# cat=Cat("哈哈",12)
# cat.run()
# cat.eat()
# print(cat.name)
# print(cat.age)
# class Animal(object):
#     def __init__(self, name='动物', color='白色'): 
#         self.__name = name 
#         self.color = color
#     def __test(self): 
#         print(self.__name) 
#         print(self.color) 
#     def test(self): 
#         print(self.__name) 
#         print(self.color) 
# class Dog(Animal):
#     def dogTest1(self):
# #         print(self.__name) 
#         #不能访问到父类的私有属性 
#         print(self.color) 
#     def dogTest2(self):
# #         self.__test() 
#         #不能访问父类中的私有方法 
#         self.test() 
# A = Animal() 
# #print(A.__name) 
# #程序出现异常，不能访问私有属性 
# print(A.color) 
# #A.__test() 
# #程序出现异常，不能访问私有方法 
# A.test() 
# print("------分割线-----") 
# D = Dog(name = "小花狗", color = "黄色") 
# D.dogTest1() 
# D.dogTest2() 

class A(object):
    def test(self):
        print("---A---")
# class B(object):
#     def test(self):
#         print("---B---")
class C(A):
    def test(self):
#         A.test(self)
#         super(C,self).test()
        super().test()
    pass
c=C()
c.test()
print(C.__mro__) 