#include <stdio.h>

enum nu1{
	a,
	b,
	c,
};
enum nu2{
	x=3,
	y=2,
	z=1,
};

void main()
{
	enum nu1 t;
	//枚举常量可以直接使用
	printf("枚举型常量a的值为:%d，b的值为:%d，c的值为:%d\n",a,b,c);
	printf("枚举型变量x的值为:%d，y的值为:%d，z的值为:%d\n",x,y,z);
	//也可以使用一下方式：
	t=b;
	printf("t的值为:%d\n",t);
}
/*
 * 枚举型常量可以使用默认值，从0开始，也可以指定相应的值
 * 要注意：
 * 在同一个作用域内，不能出现同名的枚举常量名
 */
