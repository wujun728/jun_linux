#include <stdio.h>
#include <stdlib.h>

void main()
{
	int *pa = (int *)malloc(sizeof(int)*4);
	int i;
	for(i=0;i<4;i++){
		*(pa+i)=i+1;
		printf("*(pa+%d)=%d\n",i,*(pa+i));
	}
	free(pa);
	
	int a=100;
	if(pa!=NULL){
		pa=&a;
		printf("*pa的值为:%d\n",*pa);
	}

	//看看free()前和free()后的区别
	int *pb=(int *)malloc(sizeof(int));
	*pb=200;

	printf("*pb=%d\n",*pb);
	printf("使用free()函数之前pb = %d\n",pb);
	free(pb);
	//pb=NULL;
	printf("使用free()函数之后pb = %d\n",pb);
}

/*
 * 很明显，当用free()函数释放了pa所指向的内存单元，但pa的值并不为NULL，而是输出了100
 * 虽然使用了free函数释放了pb所指向的内存单元，但是其保存的地址并没有改变
 * 在使用完free函数之后，变量pa做指向的内存单元中的数据变为“垃圾数据”
 * 在指针操作中，要养成那些不在使用了的指针赋值为NULL的习惯，避免由于粗心带来的错误
 */
