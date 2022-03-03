#include <stdio.h>

union un{
	char a;
	int b;
};

void main()
{
	union un x;
	printf("共同体union所占内存大小为:%d\n",sizeof(x));
	x.a='A';
	x.b=97;
	printf("x.a is %c,x.b is %d\n",x.a,x.b);
}
/*
 * 共同体所占的内存空间为其中占内存最大的成员所占的内存大小，为4个字节
 * 共同体是共享内存空间的，后面的赋值会覆盖前面的赋值
 * 而在上面的赋值时，共同体x实际只存放了整数97，恰好只用了4个字节中的最低一位
 * 同时x的成员变量a占用的也是4个字节中最低的字节，所以a的值为97对应的'a'
 */
