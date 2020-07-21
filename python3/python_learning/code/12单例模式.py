'''
Created on 2018年10月10日

@author: Administrator
'''
class Singleton:
    __instance=None
    
    def __new__(cls):
        if not cls.__instance:
            __instance=object.__new__(cls)
        return cls.__instance
a=Singleton()
b=Singleton()
print(id(a))
print(id(b))