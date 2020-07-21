import math
'''
    python函数
'''
# python内置了很多有用的函数

#1、 abs()函数，  求绝对值
print("-100的绝对值：", abs(-100));

# 2、max()函数， 求最大值  ,  min() 求最小值
print( max(0,1,3,5,6,7));
print( max(-5,-6,-8));

# 3、数据类型转换   int() 把其他类型转换成整数类型   float():转换为浮点数，  str(): 转换为字符串   bool() 转换为布尔类型
print(int("15"));
print(int(15.5));

#  函数名其实就是指向一个函数对象的引用，完全可以把函数名赋给一个变量，相当于给这个函数起了一个“别名”：

a = abs;  #相当于把  abs函数赋值给了 a
print("函数a求绝对值：", a(-1))

# 4、 hex()函数将整数转换为十六进制

# 5、自定义函数   在Python中，定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:，然后，在缩进块中编写函数体，函数的返回值用return语句返回
def abc(x):
    if not isinstance(x, (int, float)):   # isinstance 内置函数，用于检验字符的数据类型
        raise TypeError('bad operand type')  # 程序出现错误，python会自动引发异常，也可以通过raise显示地引发异常。一旦执行了raise语句，raise后面的语句将不能执行。

    if x>0:
        return x;
    else:
        return -x;

# 下面是调用自己的方法，一个是传入正确的参数，一个是错误的参数
print(abc(-100));
# print(abc("-100"));

# 6、定义空函数
def none(x):
    if x>0:
        pass   # pass语句什么都不做，那有什么用？实际上pass可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个pass，让代码能运行起来。
    else:
        pass

# 7、如果定义函数，返回多个值  比如在游戏中经常需要从一个点移动到另一个点，给出坐标、位移和角度，就可以计算出新的新的坐标：
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

# 如何使用呢
x, y = move(100, 100, 60, math.pi / 6)  # 这里使用两个参数进行接收
print(x, y)

# 但其实这只是一种假象，Python函数返回的仍然是单一值：
r = move(100, 100, 60, math.pi / 6)
print(r)
# 原来返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，
# 所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便。

# 7、 pow(）函数是求平方的函数


# 8、如何传入一个数组,  下面定义的参数是可以传入一个可变数组
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc(1, 2))

nums = [1, 2, 3]
calc(*nums)