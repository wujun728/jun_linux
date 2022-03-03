#include <stdio.h>
//宏定义中这些算术运算要加括号，防止替换后，优先级被破坏
#define SUM (9+10)
//宏定义可以提高代码可读性和可移植性
#define INT_SIZE sizeof(int)
//宏名出现在字符串中，会被当成普通的字符串，而不会被替换
#define STR "test"

//这是一个完整的宏定义
//(void)(&_x==&_y)该语句会检查&x和&y的类型是否一致，不一致则会出错
//typeof(x) _x=(x);typeof(y) _y该语句则是防止x和y是同一个表达式
#define max1(x,y) ({ typeof(x) _x=(x);typeof(y) _y=(y);(void)(&_x==&_y);x>_y?_x:_y;})
//这是一个不完整的宏定义
#define max2(x,y) ((x)>(y)?(x):(y))

//宏定义可变参数
#define print1(...) printf(__VA_ARGS__)
//如果__VA_ARGS__前面不加##，当前面可变参数为空时，就会报错
#define print2(tmp,...) fprintf(stdout,tmp,##__VA_ARGS__)

//嵌套宏定义
#define Y 3
#define N_SUM (Y+Y+Y)

void main()
{
	printf("(9+10)*2=%d\n",SUM*2);
	printf("int在内存中占用 %ld 个字节\n",INT_SIZE);
	/*
	使用undef来设定宏的作用域
	#undef N
	#undef INT_SIZE
	下面这两句同样的代码会编译出错
	printf("(9+10)*2=%d\n",SUM*2);
	printf("int在内存中占用 %ld 个字节\n",INT_SIZE);
	*/
	printf("不要再字符串中使用宏，比如字符串中的STR是不会被替换成：%s\n",STR);

	printf("----------\n");

	//一般情况下，这两个宏都能得到正确结果
	int a=5,b=6;
	printf("max1:%d,%d max is %d\n",a,b,max1(a,b));
	printf("max2:%d,%d max is %d\n",a,b,max2(a,b));

	
	//但是有时可能会出错,max1会严格的检查参数类型，下面的语句max1就会编译报错，而max2则会有隐患
	char c='a';
	int d=6;
	//这一句因为参数类型不一致导致编译失败
	//printf("max1:%c,%d max is %d\n",c,d,max1(c,d));
	printf("max2:%c,%d max is %d\n",c,d,max2(c,d));
	
	
	//typeof(x) _x=(x);typeof(y) _y=(y)如果不加该语句得到的将会是意想不到的结果
	//比较x和y++的大小，其实质还是比较x和y，y++是在执行比较操作后才应该++操作
	int x=1,y=2;
	//在完整的宏定义下，输出最大值2后再执行y++，y=3
	printf("max1 result is %d\n",max1(x,y++));
	int x1=1,y1=2;
	//但不完整的宏定义下，先比较出最大的y=2，然后在执行y++，y=3,最后才输出3，但这样的结果很可能不是自己想要的
	printf("max2 result is %d\n",max2(x1,y1++));

	printf("----------\n");

	print1("print1:hello world\n");
	print2("print2:hello world,%s\n","test");

	printf("----------\n");

	printf("嵌套宏定义的和为:%d\n",N_SUM);
}
/*
 * 宏定义中
 * 不能用;结尾，否则;会一同被替换进表达式
 * 注意使用()来保护运算的优先级
 * 在带参宏定义中，要注意参数是否涉及自加自减运算，如果涉及最好进行参数替换，以免带来意想不到的结果
 *
 */
