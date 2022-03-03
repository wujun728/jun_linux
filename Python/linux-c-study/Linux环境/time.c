#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
	struct tm *tm_ptr;
	time_t the_time;

	//time函数基本用法，将当前时间写入the_time指向的内存
	(void)time(&the_time);
	//gmtime函数的基本用法
	tm_ptr=localtime(&the_time);
	printf("time函数返回的时间值是：%ld\n",the_time);
	printf("gmtime函数返回的时间：\n");
	printf("date: %02d/%02d/%02d\n",
			tm_ptr->tm_year%100,tm_ptr->tm_mon+1,tm_ptr->tm_mday);
	printf("time: %02d:%02d:%02d\n",
			tm_ptr->tm_hour,tm_ptr->tm_min,tm_ptr->tm_sec);
	exit(0);

}
/*
 * gmtime函数能够将time返回的值解析成tm结构体，但这里有点问题
 * 如果在格林尼治标准时间之外的时区，或者所在地方用了夏令时
 * 那么这个时间个日期很有可能是不对的
 *
 * 需要使用localtime函数来解决这个问题
 */
