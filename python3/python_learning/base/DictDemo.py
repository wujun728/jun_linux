dic = {'name': "啊翔", "age": 18, "money": 5000, "height": 150}
print("字典中元素个数", len(dic))
print("字典中所有keys", dic.keys());
print("字典中所有values", dic.values());
print("返回元组列表", dic.items())

for key in dic.keys():
    pass
    print(key)

for key,value in dic.items():
    print(key,value)