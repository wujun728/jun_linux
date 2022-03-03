#include <fcntl.h>
#include <stdlib.h>
int main()
{
	char c[1024];
	int in,out;
	int nread;

	in=open("file.in",O_RDONLY);
	out=open("file.out",O_WRONLY|O_CREAT,S_IRUSR|S_IWUSR);
	while(nread=read(in,c,sizeof(c))>0){
		write(out,c,nread);
	}
	exit(0);
}
/*
 * 未做优化的执行结果
 * real    0m38.885s
 * user    0m2.044s
 * sys     0m36.758s
 * 
 * 优化后的结果
 * real    0m0.111s
 * user    0m0.004s
 * sys     0m0.104s
 *
 */
