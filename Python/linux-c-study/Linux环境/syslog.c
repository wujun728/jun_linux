#include <syslog.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
	FILE *f;
	f = fopen("not_here","r");
	if(!f){
		printf("unknow file,the messages will be output to log file!!\n");
		syslog(LOG_ERR|LOG_USER,"oh no -- %m\n");
	}
	exit(0);
}
/*
 * 该程序用于打开一个不存在的文件，然后将错误信息写入日志中
 * Sep 29 00:30:59 bogon syslog.out: oh no -- No such file or directory
 * 需要注意的是日志文件存放的位置，不同的操作系统存放位置可能不一样
 * 日志文件一般放在/var/log/目录中，有的系统中是messages文件，而在我的ubuntu中则是syslog文件
 *
 */
