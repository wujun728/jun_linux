#include <sys/types.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//该函数讲一个字符串写入一个临时文件10000次，然后做一些算数运算产生CPU负载
void work()
{
	FILE *f;
	int i;
	double x=4.5;

	f=tmpfile();
	for(i=0;i < 10000;i++){
		fprintf(f,"Do some output\n");
		if(ferror(f)){
			fprintf(stderr,"Error writing to temporary file\n");
			exit(1);
		}
	}
	for(i=0;i<10000;i++){
		x=log(x*x + 3.21);
	}
}

//调用work函数，然后用getrusage函数获得它耗费CPU的时间，并显示出来
int main()
{
	struct rusage r_usage;
	struct rlimit r_limit;
	int priority;
	work();
	getrusage(RUSAGE_SELF,&r_usage);

	printf("CPU usage:User = %ld.%06ld,System = %ld.%06ld\n",
			r_usage.ru_utime.tv_sec,r_usage.ru_utime.tv_usec,
			r_usage.ru_stime.tv_sec,r_usage.ru_stime.tv_usec);

	//调用getpriority函数和getrlimit函数获得它的当前优先级和文件大小限制
	priority = getpriority(PRIO_PROCESS,getpid());
	printf("Current priority =%d\n",priority);

	getrlimit(RLIMIT_FSIZE,&r_limit);
	printf("Current FSIZE limit:soft = %ld,hard=%ld\n",
			r_limit.rlim_cur,r_limit.rlim_max);

	//用setrlimit函数设置文件大小限制，并执行work，这次work会执行失败
	r_limit.rlim_cur = 2048;
	r_limit.rlim_max = 4096;
	printf("Setting a 2K file size limit\n");
	setrlimit(RLIMIT_FSIZE,&r_limit);

	work();
	exit(0);

}
/*
 * 编译时要使用gcc -o limits.out limits.c -lm来连接数学函数库
 * 执行./limits.out时：
 * CPU usage:User = 0.003886,System = 0.003173
 * Current priority =0
 * Current FSIZE limit:soft = -1,hard=-1
 * Setting a 2K file size limit
 * File size limit exceeded
 * 提高优先级再运行时，nice ./limits.out
 * CPU usage:User = 0.004641,System = 0.003706
 * Current priority =10
 * Current FSIZE limit:soft = -1,hard=-1
 * Setting a 2K file size limit
 * File size limit exceeded
 * 明显的程序执行时间变长了
 */
