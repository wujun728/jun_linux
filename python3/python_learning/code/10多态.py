'''
Created on 2018年10月10日

@author: Administrator
'''
class A(object):
    def show(self):
        print("a.show")
class B(A):
    def show(self):
        print("b.show")
class C(A):
    def show(self):
        print("c.show")
class D(object):
    def show(self):
        print("d.show")
a=A()
a.show()
b=B()
b.show()
d=D()
d.show()
