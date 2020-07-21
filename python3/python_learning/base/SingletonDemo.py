
# 单例模式

# class Singleton:
#
#     # 定义一个私有变量
#     __instance = None;
#     __first_init = False
#
#     def __int__(self, age, name):
#         if not self.__first_init:
#             self.name = name;
#             self.age = age;
#
#     def __new__(cls, age, name):
#         # 如果类数字能够__instance没有或者没有赋值
#         # 那么创建一个对象，并且赋值为这个对象的引用，保证下次调用这个方法时，能够知道之前已经创建过了，确保只有一个对象存在。
#
#         if not cls.__instance:
#             cls.__instance = object.__new__(cls);
#         return cls.__instance;
#
#     def __str__(self):
#         msg = self.name + "_" + self.age;
#         return msg;
#
# a = Singleton(18, "bin");
# b = Singleton(8, "bin");
# print(a.age);
# print(b.age);


class  Test:
    index = "z";

    def print_index(self):
        print(self.index);

    @classmethod
    def print_class_index(cls):
        print(cls.index);

    @classmethod
    def set_class_index(cls, name):
        cls.index = name;

    def set_index(self, name):
        self.index = name;

test = Test();
test.set_class_index("B")
print(Test.index);
test.set_index("A")
print(test.index);
print(test.print_class_index());

test2 = Test();
print(Test.index);
print(test2.index);
print(test2.print_class_index());





