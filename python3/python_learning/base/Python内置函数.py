# 1、enumerate函数  当你索引数据时，使用enumerate的一个好方法是计算序列（唯一的）dict映射到位置的值
some_list = ['foo', 'bar', 'baz']
mapping = {}
# Python内建了一个enumerate函数，可以返回(i, value)元组序列
for i,v in enumerate(some_list):
    mapping[v] = i
print(mapping)

# 2、sorted函数可以从任意序列的元素返回一个新的排序好的列表
sort_list = sorted([1,5,2,4,7,6]);
print(sort_list);

# 3、zip函数可以将多个列表，元组或其他序列成对组合成一个元组列表
seq1 = ['foo', 'bar', 'baz']
seq2 = ['haha', 'heihei', 'gaga']
zipped = zip(seq1, seq2);
zip_list = list(zipped);
print(zip_list)

seq3,seq4 = zip(*zip_list);
print(seq3);
print(seq4);

# 4、reversed函数：从后向前迭代一个序列
reversed_list = list(reversed(range(0,10)));
print(reversed_list);