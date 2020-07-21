'''
Created on 2018年10月10日

@author: Administrator
'''
class Dog(object):
    
    def run(self):
        print("running")
        #init不是构造器，只是完成对象的初始化操作,默认调用，可以在创建对象的时候写成参数
    def __init__(self,name,age):
        print("init被调用")
        self.name=name
        self.age=age
    def __new__(cls,name,age):
        print("new被调用")
        return object.__new__(cls)
    def __str__(self):
        return "name:%s---age:%s"%(self.name,self.age)
    def __del__(self):
        print("%s被回收"%self.name)
# dog=Dog("haha",12)
# dog.run()
# dog2=Dog("heihei",3)
# dog2.run()
# print(dog.name)
# print(dog.age)
# print(dog2.age)
# print(dog2.name)
# print(dog)
# print(dog2)
dog=Dog("haha",12)
dog2=dog
dog3=dog
print("dog2被删除")
del dog
print("dog3被删除")
del dog3
print("dog被删除")
del dog2
