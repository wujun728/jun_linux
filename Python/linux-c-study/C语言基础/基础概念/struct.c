#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct stu{
	char ID[11];
	char name[20];
	int sex;//1-男，0-女
};//注意结构体声明要用；结束

void main()
{
	struct stu stu1,*stu2;
	strcpy(stu1.ID,"1234567890");
	strcpy(stu1.name,"hello");
	stu1.sex=1;
	//在使用结构体指针时，要为其分配内存空间
	stu2=malloc(sizeof(struct stu));
	strcpy(stu2->ID,"0987654321");
	strcpy(stu2->name,"world");
	stu2->sex=0;
	printf("结构体stu在内存中的大小为：%d\n",sizeof(struct stu));
	printf("char ID[11],char name[20], int sex;占用内存之和为%d\n",11*sizeof(char)+20*sizeof(char)+sizeof(int));
	printf("stu1:ID:%s, name:%s, sex:%s\n",stu1.ID,stu1.name,stu1.sex==1?"男":"女");
	printf("stu2:ID:%s, name:%s, sex:%s\n",stu2->ID,stu2->name,stu2->sex==1?"男":"女");

}
/*
 * 在输出结果的时候，会发现结构体stu所占内存空间与它的成员变量所占内存之和不一样
 * 因为在其中占字节数最大的是int，为4个字节，char只占一个字节，所以该结构体是以4字节对齐的
 * 也就是stu的大小是4的整数倍，其中ID，name共有31个字节，并不是4的倍数，要考虑字节对齐的问题
 * 所以它们在内存中实际的大小为32个字节，在加上最后一个int一共36个字节
 * 而不是简单的将它的成员变量大小相加
 */
