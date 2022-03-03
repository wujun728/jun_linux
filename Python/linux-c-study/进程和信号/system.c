#include <stdlib.h>
#include <stdio.h>

int main(){
	printf("Running ps with system\n");
	//后台执行的程序system会立刻返回
	system("ps ax &");
	//前台执行的程序system会等待进程执行结束后才返回
	//system("ps ax");
	printf("system函数执行结束\n");
	exit(0);
}
