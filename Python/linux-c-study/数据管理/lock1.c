#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>

int main()
{
	int file_desc;
	int save_errno;

	/* 打开/tmp/LCK.test这个用于测试的锁文件
	 * O_CREAT|O_EXCL这是一个原子操作，只有当文件不存在时才会执行成功 
	 */
	file_desc=open("/tmp/LCK.test",O_RDWR|O_CREAT|O_EXCL,0444);
	if(file_desc == -1){
		//错误号为17为File exists
		save_errno = errno;
		printf("Open failed with error %d\n",save_errno);
	}else{
		printf("Open successded\n");
	}
	exit(EXIT_SUCCESS);
}
