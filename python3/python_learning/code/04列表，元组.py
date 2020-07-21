'''
Created on 2018年10月9日

@author: Administrator
'''
# a=["a","b","c",12,12.34,"a","v","b","a"]
# print(a)
# print(len(a))
# print(a[-1])
# print(a[::-1])
# a.append("e")
# print(a)
# b=["aa","bb","cc"]
# a.extend("f")
# a.extend(b)
# b.extend(a)
# print(a)
# print(b)
# a.insert(2, "hello")
# print(a)
# # del(a)
# # a.pop()
# a.remove("hello")
# print(a)
# if "a" not in a:
#     print("存在")
# else:
#     print("不存在")
# # print(a.index("f",2,6))
# print(a.count("a"))
# #list存放  有序，不唯一的数据，数据类型不必一致
# print(a)    
# c=[1,3,5,2,4]
# print(c)
# c.sort()
# print(c)
# c.reverse()
# print(c)
# for i,chrs in enumerate(c):
#     print("%d----%s"%(i,chrs))
# c[2]="abcdefg"
# print(c)

a=("a","c","b")
b=(1,2,3,4,5)
print(id(a))
print(id(b))
# a[2]="d"
a=b
print(id(a))
print(a)
t=(1,)
print(t)

t=("a","b",["A","B"])
print(t)
# t[2][0]="X"
# t[2][1]="Y"
# y=["X","Y"]
# t[2]=y
print(t)
print(t.index("a", ))
print(t.count("a"))

#dict
person={"aaa":12,"bbb":23,"ccc":34}
print(person)
print(person["aaa"])
abc={"a","b","c"}
print(abc)
person["aaa"]=100
print(person)
person["ddd"]=200
print(person)
del(person["bbb"])
# del(person)
print(person)
person.clear()
print(person)

# for key in person.keys():
#     print(key)
# for value in person.values():
#     print(value)
# for i in person.items():
#     print(i)    
# for key,value in person.items():
#     print(key,value)
a=set([1,2,3,4])
print(a)
    