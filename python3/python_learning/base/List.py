print("hello world")

# 对于单个字符的编码，Python提供了ord()函数获取字符的整数表示，chr()函数把编码转换为对应的字符：

# ord()函数获取字符的整数表示
print("A 的ASCII为", ord('A'))
print("中 的ASCII为", ord('中'))

# chr()函数把编码转换为对应的字符
print("66 表示的字符为", chr(66))
print("25991 表示的字符为", chr(25991))

######  List  ############

# Python内置的一种数据类型是列表：list。list是一种有序的集合，可以随时添加和删除其中的元素。
list = ["hello", "hi", "hey"];
print("list数组内容为:", list);
print("list数组长度为:", len(list));
print("list数组第1个元素为:", list[0]);

# 如果要取最后一个元素，除了计算索引位置外，还可以用-1做索引，直接获取最后一个元素：
print("list数组倒数第1个元素为:", list[-1]);

# append 追加到最后
list.append("preety good");
print("list数组增加元素:", list);

# insert插入到指定位置
list.insert(0, "better");
print("list数组增加元素:", list);

#使用pop删除最后一个元素,  也可以删除指定的元素  pop(1) : 表示下标为1的元素
list.pop();
print("使用pop()删除最后一个元素", list);

# 替换元素
list[0] = "哈哈哈";
print("将下标为0的元素进行替换", list);

# 在一个数组里面，可以在放入一个数组
p = ['asp', 'php']
s = ['python', 'java', p, 'scheme']

print("list中可以在存放一个list", s )

# list中数据类型也可以不一致
L = ['Apple', 123, True]
print("list中数据类型可以不一致", L )

# tuple
# 另一种有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改，比如同样是列出同学的名字：
# 现在，classmates这个tuple不能变了，它也没有append()，insert()这样的方法。其他获取元素的方法和list是一样的，你可以正常地使用classmates[0]，classmates[-1]，但不能赋值成另外的元素
# 不可变的tuple有什么意义？因为tuple不可变，所以代码更安全。如果可能，能用tuple代替list就尽量用tuple。
# tuple的陷阱：当你定义一个tuple时，在定义的时候，tuple的元素就必须被确定下来，比如：
t = (1, 2)
print(t)
