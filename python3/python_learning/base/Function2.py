def fun(a, b, *c, **d):
    print(a);
    print(b);
    print(c);
    print(d);
# fun(1,2,3,4,5,m=1,n=2,k=3);

def fun2(a):
    a+=a;

a = 10;
fun2(a);
print(a);
b=[10,20];
fun2(b)
print(b)


bb = 100;
# def fun3():
#     bb += 100;
#     print("函数里的1", bb);
# print(bb)
def fun4():
    global bb;
    print(bb);
    bb += 100;
    print("函数里的2",bb);

# fun3();
#fun4();

sum = lambda arg1,arg2: arg1+arg2;
print(sum(10,20))

