/*
 * 一维和二维动态数组创建的详细过程
 */
#include <stdio.h>
#include <stdlib.h>

//创建一维动态数组
int *create_array1(int length)
{	
	int i,*arr;
	printf("创建长度为 %d 的一维数组\n",length);
	if((arr=(int *)malloc(sizeof(int)*length)) == NULL){
		printf("内存分配失败！\n");
		return 0;
	}
	printf("creat_array1函数中的动态一维数组输出：\n");
	for(i=0;i<length;i++){
		arr[i]=i+1;
		printf("%d\t",arr[i]);
		if(0 == (i+1)%4) printf("\n");
	}
	printf("\ncreate_array1输出的首地址是:%d\n",arr);
	return arr;
}

//创建二维动态数组
int **create_array2(int rows,int cols)
{
	//原理和创建一维动态数组差不多
	//首先先创建一维动态数组，内个元素用来存储另外一个一维数组
	int i,j,**arr;
	printf("创建第一维长度为 %d ,第二位长度为 %d 的二维数组\n",rows,cols);
	//创建动态二维数组的第一维
	if((arr=(int **)malloc(rows*sizeof(int*)))==NULL){
		printf("分配第一维内存空间失败!\n");
		return 0;
	}
	//创建动态二维数组的第二维
	//要遵循从外向内的创建原则
	for(i=0;i<rows;i++){
		if((arr[i]=(int *)malloc(cols*sizeof(int)))==NULL){
			printf("分配第二维内存空间失败!\n");
			return 0;
		}
	}

	for(i=0;i<rows;i++){
		for(j=0;j<cols;j++){
			arr[i][j]=i*cols+j+1;
			printf("%d\t",arr[i][j]);
		}
		printf("\n");
	}
	printf("\ncreate_array2输出的首地址是:%x\n",arr);
	return arr;
}
int main()
{
	//一维动态数组
	int *array1,**array2;
	int length =10;
	array1=create_array1(10);
	printf("\nmain函数中输出array1首地址是:%x\n",array1);
	free(array1);

	//二维动态数组
	int rows=10,cols=10;
	int i;
	array2=create_array2(rows,cols);
	printf("\nmain函数中输出array2首地址是:%x\n",array2);
	//二维动态数组内存释放时，要遵循从内到外的原则
	for(i=0;i<rows;i++){
		free(array2[i]);
	}
	free(array2);

}
