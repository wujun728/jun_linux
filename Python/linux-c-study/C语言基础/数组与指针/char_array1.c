#include <stdio.h>

#define M 20

void main()
{
	int i;
/* 
 * 数组初始化与输出  
 */
	//方式1-使用字符串常量列表初始化字符数组
	char arr1[M] = {'h','e','l','l','o',' ','w','o','r','l','d','!'};
	//方式2-使用字符串常量初始化字符数组
	char arr2[M] = {"hello world!"};
	//arr1输出-这样的输出结果中不包含任何空字符
	for(i=0;arr1[i] != '\0';i++){
		printf("%c",arr1[i]);
	}
	printf("\n");
	//arr2输出-同上
	for(i=0;arr2[i] != '\0';i++){
		printf("%c",arr2[i]);
	}
	printf("\n");
	//arr1与arr2如果这样输出：
	//注：在使用%s格式输出时，要得到正确结果，那么字符串必须以字符'\0'结尾
	printf("arr1-%s\n",arr1);
	printf("arr2-%s\n",arr2);
/*
 * 使用字符串常量列表与字符串常量初始化的不同
 */
	char arr3[] = {'h','e','l','l','o',' ','w','o','r','l','d','!'};
	char arr4[] = {"hello world!"};
	printf("采用字符串常量列表初始化的arr3数组长度为:%ld\n",sizeof(arr3));
	printf("采用字符串常量初始化的arr4数组长度为:%ld\n",sizeof(arr4));
/*
 * 虽然&arr[0]和arr的值相同，但所指内容并不同,这里使用arr4举例
 * &arr4[0]代表一个地址变量，32位计算机中地址变量由4字节大小保存
 * arr4则代表整个数组，可以将其视为char[13]这种特殊类型
 */
	printf("&arr[0]占用内存大小：%ld\n",sizeof(&arr4[0]));
	printf("arr占用内存大小：%ld\n",sizeof(arr4));

}
