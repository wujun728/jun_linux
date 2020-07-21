# Python内置了字典：dict的支持，dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d.get("Michael"));
# 如果这个值为空的话，就调用后面默认的值
print(d.get("Hei", -1));

# 删除Michael这个值
d.pop("Michael")
print(d);

#和list比较，dict有以下几个特点：
# 查找和插入的速度极快，不会随着key的增加而变慢；
# 需要占用大量的内存，内存浪费多。

# 而list 具有下面特点
#查找和插入的时间随着元素的增加而增加；
#占用空间小，浪费内存很少。

# set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
s = set([1, 2, 3]);
print("s的值为" , s);

# 增加一个已经存在的元素，会继续不存在
s.add(3);

print(s);