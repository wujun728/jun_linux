#include <stdio.h>
#include <stdlib.h>

int main()
{
	int *n,*p;
	int i,n1,n2;
	
	printf("请输入所要创建的动态数组的长度是:");
	scanf("%d",&n1);

	if((n=(int *)malloc(n1*sizeof(int)))==NULL){
		printf("内存空间分配失败!\n");
		return 0;
	}

	for(i=0;i<n1;i++){
		n[i]=n1-i;
		printf("%d\t",n[i]);
		if(0 == (i+1)%4) printf("\n");
	}
	printf("\n输入需要扩展的动态数组的长度:");
	scanf("%d",&n2);

	//重新分配内存时，会先将n指向的内存区域复制到新的内存区域
	//再释放n指向的内存空间，并将新的内存空间首地址返回
	if((p=(int *)realloc(n,(n2)*sizeof(int)))==NULL){
		printf("内存重新分配失败\n");
		return 0;
	}
	for(i=0;i<n2;i++){
		p[i]=n2-i;
		printf("%d\t",p[i]);
		if(0 == (i+1)%4) printf("\n");
	}
	printf("\n");
	free(p);
	return 0;
}
