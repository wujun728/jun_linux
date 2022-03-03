#include <syslog.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
	int logmask;

	openlog("logmask",LOG_PID|LOG_CONS,LOG_USER);
	syslog(LOG_INFO,"informative message,pid= %d",getpid());
	syslog(LOG_DEBUG,"debug message, should apper");
	//设置日志掩码，低于LOG_NOTICE优先级的日志将会丢弃
	logmask=setlogmask(LOG_UPTO(LOG_NOTICE));
	syslog(LOG_DEBUG,"debug message, should not apper");
	exit(0);
}
/*
 * 在日志中应该看到如下两条日志：
 * Sep 29 02:03:49 bogon logmask[1869]: informative message,pid= 1869
 * Sep 29 02:03:49 bogon logmask[1869]: debug message, should apper
 * 可见由于LOG_DEBUG的优先级低于LOG_NOTICE，所以最后一条日志信息不会出现在日志文件中
 */
