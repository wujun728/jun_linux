#include <stdio.h>
void print()
{
	static int a=1;
	int b=1;
	printf("静态局部变量a=%d\n",a++);
	printf("非静态局部变量b=%d\n",b++);
}

int main()
{
	int i=0;
	while(i<10){
		print();
		printf("--------------\n");
		i++;
	}
}
/*
 * 静态变量的生存期从程序开始到程序结束，它是静态存储
 * 但这并不会改变它的作用域
 * 它只能在被定义的源程序文件中使用，不能被其他文件使用
 *
 */
