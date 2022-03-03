/*
 * 普通指针与数组指针的区别
 */
#include <stdio.h>

int main(){
	char a[4];
	//分别定义了数组指针pa和普通指针pb
	char (*pa)[4],*pb;

	pa=&a;
	pb=&a[0];
	printf("char型数组指针pa所占用的内存大小为：%d\n",sizeof(*pa));
	printf("char型数组指针pb所占用的内存大小为：%d\n",sizeof(*pb));
	printf("pa=%x\tpa+1=%x\n",pa,pa+1);
	printf("pb=%x\tpb+1=%x\n",pb,pb+1);
}
/*
 * 在上面代码中，&a和&a[0]都是数组的首地址，但他们的类型并相同
 * 这是因为&a[0]仅表示数组中一个char型变量的地址，等同于普通的char型变量
 * 值得注意的是&a，现将char a[4]变形为char *(&a)[4]，可以发现&a是一个char *[4]型的指针，
 * 所以需要定义一个char (*pa)[4]来存放&a
 * 如果直接用pb=&a就会出现 warning: assignment from incompatible pointer type
 */
