#include <stdio.h>

void fun()
{
	int a=3,b;
	printf("fun()函数里面的a值为：%d\n",a);
}

int main()
{
	int a=0,b;
	{
		int a=1;
		printf("main()函数里面被大括号封装的a的值为：%d\n",a);
	}
	fun();
	printf("main()函数里面的a值为：%d\n",a);

	return 0;
}
/*
 * 注意：
 * 如果在同一区域中出现同名变量，那么以在该区域有效且定义最接近该区的变量为准
 *
 */
