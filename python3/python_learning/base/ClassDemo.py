# 类和对象测试
# import time
#
# class Persion :
#     def __init__(self, name, age):
# #         self.name = name;
# #         self.age = age;
#
#     def eat(self):
#         print("吃东西");
#     def work(self):
#         print("开始工作")
#
# persion = Persion("许志翔", 18);
#
# print(persion.name);
# print(persion.age);
#
# persion.eat();
# persion.work();

# class A(object):
#     def __init__(self, name):
#         self.__name = name
#         print("这是 init 方法")
#     def setName(self, name):
#         self.__name = name;
#     def getName(self):
#         return self.__name
#     def __new__(cls, name):
#         print("这是 new 方法")
#         return object.__new__(cls)
#
# a1 = A("张三");
# a1.setName("许志翔");
# print(a1.getName());

# class A:
#     def __init__(self):
#         print("这是 init 方法")
#     def __new__(cls):
#         print("这是 new 方法")
#         return object.__new__(cls)
#     def __del__(self):
#         print("这是 del方法");
#
# a = A();
# del a;

# #  继承
# #定义一个父类
# class Parent(object):
#     def __getParent(self):
#         return self.name;
#     def __init__(self, name):
#         self.name = name;
#     def eat(self):
#         print("1开始吃");
#
# class Parent2(object):
#     def play(self):
#         print("开始玩");
#
#     def eat(self):
#         print("2开始吃");
#
# class Child( Parent2, Parent):
#
#     def work(self):
#         super().eat();
#         print("开始工作", self.name);
#
# a = Child("许志翔");
# a.eat();
# a.work();
# a.play();


# class F1(object):
#     def show(self):
#         print('F1.show')
# class S1(F1):
#     def show(self):
#         print('S1.show')
# class S2(F1):
#     def show(self):
#         print('S2.show')
#
# def Func(obj):
#         print(obj.show())
# s1_obj = S1()
# Func(s1_obj)
# s2_obj = S2()
# Func(s2_obj)

# class People(object):
#     country = 'china'; #类属性
#
# print(People.country);
#
# people = People();
# print(people.country)
#
# people.country = "中国"
# print(people.country);
#
# print(People.country);

class People(object):
    country = 'china'#类方法，用classmethod来进行修饰

    @classmethod
    def getCountry(cls):
        return cls.country
    @classmethod
    def setCountry(cls,country):
        cls.country = country
p = People()
print( p.getCountry()) #可以用过实例对象引用
print( People.getCountry()) #可以通过类对象引用
p.setCountry('japan')
print( p.getCountry())
print( People.getCountry())


sum  = lambda arg1 ,arg2 : arg1 + arg2







