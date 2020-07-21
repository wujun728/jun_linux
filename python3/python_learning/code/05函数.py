'''
Created on 2018年10月9日

@author: Administrator
'''
# def test():
#     print("python真简单")
# test()
# 
# def add(a,b):
#     print(a+b)
# add(1,2)
# 
# def add2(a,b=2):
#     print(a+b)
# add2(1)
# x=3
# y=5
# add2(x,y)
# 
# def function(a,b,*args,**kwargs):
#     print(a)
#     print(b)
#     print(*args)
#     for i in kwargs.items():
#         print(i)
# function(1,2,3,4,5,6,7,8,m=7,x=9,y=10)

# def add3(a):
#     a+=a
# # a=10
# # a=[1,2]
# a=(1,2)
# add3(a)
# print(a)

# def func(a,b):
#     c=a+b
#     return c
# print(func(2,3))
# 
# def func2(a):
#     b=100+a
#     c=200+a
#     return b,c
# b,c=func2(200)
# print(b)
# print(c)

# a=10
# def func():
#     global a
#     a=a+10
#     print(a)
# func()  
# print(a) 
# a=100
# print(id(a))
# def test1():
#     a=10
#     print(a)
#     a=20
#     print(a)
# def test2():
#     global a
#     a+=100
#     print(a)
#     print(id(a))
# # test1()
# test2()
# print(a)
# print(id(a))

# b=10
# def test():
#     c=b
#     print(b)
#     print(c)
# test()

def createNum(a):
    arr=[]
    def getNum(b):
        if b<2:
            return 1
        else:
            return getNum(b-1)+getNum(b-2) 
    for i in range(0,a):
        arr.append(getNum(i))
    print(arr)
createNum(20)  

sum=lambda a,b,c:a+b+c
print(sum(1,2,3))

def test(a,b,opt):
    print(a)
    print(b)
    print("result:%d"%opt(a,b))
test(1,2,lambda a,b:a+b)

stus = [ {"name":"zhangsan", "age":18}, {"name":"lisi", "age":19}, {"name":"wangwu", "age":17} ]
stus.sort(key=lambda x:x["age"])
print(stus)







