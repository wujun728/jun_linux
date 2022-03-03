/*
 * 简单的内存分配程序
 */
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

//定义1M的空间大小
#define A_MEGABYTE (1024*1024)

int main()
{
	char *some_memory;
	int megabyte = A_MEGABYTE;
	int exit_code = EXIT_FAILURE;

	some_memory = (char *)malloc(megabyte);
	if(some_memory != NULL){
		sprintf(some_memory,"hello world!\n");
		printf("%s",some_memory);
		exit_code = EXIT_SUCCESS;
	}
	free(some_memory);
	exit(exit_code);
}
