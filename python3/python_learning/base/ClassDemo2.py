
class Demo(object):

    def __int__(self, name):
        self.__name = name;

    def eat(self):
        print("吃饭");

    def setName(self, newName):
        self.__name = newName;

    def getName(self):
        return self.__name


demo = Demo();
print(demo);
demo.setName("李四")
print(demo.getName())

