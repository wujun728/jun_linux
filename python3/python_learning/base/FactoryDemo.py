# 工厂模式


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self, type_axe):
        print( self.name + "开始工作了")
        axe = Factory.create_axe(type_axe);
        axe.cut_tree();

class Axe(object):
    def cut_tree(self):
        print("正在砍树");

class StoneAxe(Axe):
    def __init__(self, name):
        self.name = name;
    def cut_tree(self):
        print("使用石头做的斧头砍树");

class SteeAxe(Axe):
    def __init__(self, name):
        self.name = name;
    def cut_tree(self):
        print("使用钢斧头砍树");

class WaterAxe(Axe):
    def __init__(self, name):
        self.name = name;
    def cut_tree(self):
        print("使用水砍树");

class Factory(object):

    @staticmethod
    def create_axe(type):
        if type == "sthone":
            return StoneAxe("花岗岩斧头");
        elif type == "steel":
            return SteeAxe("加爵斧头");
        elif type == "water":
            return WaterAxe("水斧头");
        else:
            print("传入的类型不同");

p = Person("张三", 18);
p.work("sthone");