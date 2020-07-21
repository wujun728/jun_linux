# 列表推导式
# 列表推导式是Python最受喜欢的特性之一。它允许用户方便的从一个集合中过滤元素，形成列表，在传递参数的过程中还可以修改元素。
# 列表推导式形式：[ expr for val in collection if condition]

# 上面表达式等同于下面的形式
# collection = []
# result = []
# for val in collection:
#     if condition:
#         result.append(expr)

# 例1：给定一个字符串列表，我们可以过滤长度在2以及以下的字符串，并将其他字符串转换成大写。
strings = ['a', 'as', 'bat', 'car', 'dove', 'python']
list = [x.upper() for x in strings if x.__len__()>2]
print(list);

# 例2：用相似的方法，推导集合和字典
# dict_comp = {key-expr : value-expr for value in collection if condition}

# 例2：字典推导式
loc_mapping = {val : index for index, val in enumerate(strings)}
print(loc_mapping);
#输出  {'a': 0, 'as': 1, 'bat': 2, 'car': 3, 'dove': 4, 'python': 5}

# 例3：集合列表推导式  set_comp = {expr for value in collection if condition}
unique_lengths = {len(x) for x in strings}
print(unique_lengths);