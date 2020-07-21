from abc import abstractmethod


# class Foo(object):
#     def __init__(self, name):
#         self.name = name
#         print('init %s' % self.name)
#
#     def __new__(cls, *args, **kwargs):
#         print('new')
#         return object.__new__(cls)
#
#     def __call__(self, *args, **kwargs):
#         self.name = args[0]
#         print(kwargs['d'])
#         print('call')
#
#     def run(self):
#         print(self.name)
#
#
# a = Foo('name')
#
# a('age', d=1)
#
# a.run()

# class MyType(type):
#     def __call__(cls, *args, **kwargs):
#         obj = cls.__new__(cls, *args, **kwargs)
#         print('-------------')
#         obj.__init__(*args, **kwargs)
#         return obj
#
#
# class Foo(metaclass=MyType):
#     def __init__(self, name):
#         print('============')
#         self.name = name
#
#     def run(self):
#         print(self.name)
#
#
# a = Foo(123)
# print(a)
# print(a.name)

# class MyType(type):
#     def __call__(cls, *args, **kwargs):
#         obj = cls.__new__(cls, *args, **kwargs)
#         if cls == Foo1:
#             obj.__init__(Foo())
#         if cls == Foo2:
#             obj.__init__(Foo1())
#         return obj
#
#
# class Foo(metaclass=MyType):
#     def __init__(self, *args):
#         print("foo")
#         self.name = 0
#
#     def f(self):
#         print(self.name)
#
#
# class Foo1(metaclass=MyType):
#     def __init__(self, *args):
#         print("foo1")
#         self.name = 1
#
#     def f1(self):
#         print(self.name)
#
#
# class Foo2(metaclass=MyType):
#     def __init__(self, *args):
#         print("foo2")
#         self.name = 2
#
#     def f2(self):
#         print(self.name)
#
#
# a = Foo2()
# a.f2()


class Mapper:
    __mapper_relation = {}

    @staticmethod
    def register(cls, value):
        Mapper.__mapper_relation[cls] = value

    @staticmethod
    def exit(cls):
        if cls in Mapper.__mapper_relation:
            return True
        return False

    @staticmethod
    def value(cls):
        return Mapper.__mapper_relation[cls]


class MyType(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        arg_list = list(args)
        if Mapper.exit(cls):
            value = Mapper.value(cls)
            arg_list.append(value)
        obj.__init__(*arg_list, **kwargs)
        return obj


class Head:
    def __init__(self):
        self.name = 'name'

class Foo(metaclass=MyType):
    def __init__(self, f):
        self.f = f

    def run(self):
        print(self.f)


class Bar(metaclass=MyType):
    def __init__(self, b):
        self.b = b

    def run(self):
        print(self.b)


Mapper.register(Foo, Head())
Mapper.register(Bar, Foo())

a = Foo()
print(a.f.name)
b = Bar()
print(b.b.f.name)
