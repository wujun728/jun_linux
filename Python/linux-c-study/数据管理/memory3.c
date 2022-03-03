/*
 * 滥用内存
 */
#include <stdlib.h>
#include <stdio.h>

#define ONE_K (1024)

int main()
{
	char *some_memory;
	char *scan_ptr;
	int i=0;

	some_memory=(char *)malloc(ONE_K);
	if(some_memory ==NULL) exit(EXIT_SUCCESS);

	scan_ptr=some_memory;
	while(1){
		printf("第-%d-次循环\n",i);
		*scan_ptr = '\0';
		scan_ptr++;
		i++;
	}
	exit(EXIT_SUCCESS);
}
/*
 * 当你读取超过系统分配给你的内存容量后
 * 系统为了保护其他部分的内存，会终止其运行
 */
