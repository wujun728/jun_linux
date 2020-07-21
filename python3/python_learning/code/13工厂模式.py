'''
Created on 2018年10月10日

@author: Administrator
'''
class Person(object):
    def __init__(self, name):
        self.name=name
    def work(self,type_axe):
        print("%s开始工作了"%(self.name))
#         axe=StoneAxe()
#         axe=SteelAxe()
        axe=Factory.create_axe(type_axe)
        axe.cut_tree()
        
class Axe(object):
    def cut_tree(self):
        print("正在砍树")
class StoneAxe(Axe):
    def cut_tree(self):
        print("使用石头做的斧子砍树")
class SteelAxe(Axe):
    def cut_tree(self):
        print("使用钢斧头砍树")
class WaterAxe(Axe):
    def cut_tree(self):
        print("使用水砍树")
class Factory(object):
    @classmethod
    def create_axe(self,type_axe):
        if type_axe=="stone":
            return StoneAxe()
        elif type_axe=="steel":
            return SteelAxe()
        elif type_axe=="water":
            return WaterAxe()
        else:
            print("传入的参数不对")
p=Person("张三")
p.work("water")