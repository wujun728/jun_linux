/*
 * 请求全部物理内存
 */
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define A_MEGABYTE (1024*1024)
#define PHY_MEM_MEGS 1024	/* 你设备的真实内存大小  */

int main()
{
	char *some_memory;
	size_t size_to_allocate = A_MEGABYTE;
	int megs_obtained =0;

	while(1){
	//while(megs_obtained < (PHY_MEM_MEGS *2)){
		some_memory = (char *)malloc(size_to_allocate);
		if(some_memory != NULL){
			megs_obtained++;
			sprintf(some_memory,"hello world");
			printf("%s - now allcated %d Megabytes\n",some_memory,megs_obtained);
		}else{
			exit(EXIT_FAILURE);
		}
	}
	exit(EXIT_SUCCESS);
}
/*
 * 该程序通过循环不断循环来不断申请越来越多的内存，直到它分配了在PHY_MEM_MEGS定义的物理内存容量的2倍为止
 * 看上去该程序似乎消耗了物理内存中的每个字节，但该程序依然运行良好
 * 当然，你也可以将while的循环条件改成1，让程序无限制的申请内存
 * 当分配的内存的大小接近机器的物理内存容量的时候，运行速度明显慢了下来，还能明显的感觉到硬盘的操作
 * 当分配的内存大大的超出了物理内存的时候，系统为了保护自己的安全运行，会终止该程序的运行
 */
