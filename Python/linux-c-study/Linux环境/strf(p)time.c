#define _XOPEN_SOURCE
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
	struct tm *tm_ptr,timestruct;
	time_t the_time;
	char buf[256];
	char *result;
	(void)time(&the_time);
	tm_ptr=localtime(&the_time);

	//该函数将time函数返回的时间格式化成format指定的格式
	strftime(buf,256,"%A %d %B, %I:%S %p",tm_ptr);

	//打印格式化后的时间字符串
	printf("strftime gives:%s\n",buf);

	//自定义一个包含日期和时间的字符串
	strcpy(buf,"Thu 26 July 2007,17:53 will do fine");

	printf("calling strptime with: %s\n",buf);

	//清空tm_ptr
	tm_ptr=&timestruct;
	//将自定义的时间和日期的字符串按照给出的格式解析成一个tm结构体
	result = strptime(buf,"%a %d %b %Y, %R",tm_ptr);
	//输出strptime函数不能转换的剩余字符串
	printf("strptime consumed up to:%s\n",result);

	//打印tm结构体
	printf("strptime gives:\n");
	printf("date: %02d/%02d/%02d\n",
			tm_ptr->tm_year%100 ,tm_ptr->tm_mon+1,tm_ptr->tm_mday);
	printf("time: %02d:%02d\n",
			tm_ptr->tm_hour,tm_ptr->tm_min);
	exit(0);
}
/*
 * 在编译该文件的时候可能会出现警告，因为GNU库在默认情况下并未声明strptime函数
 * 需要在#include <time.h>之前加上以下语句，来使用X/Open的标准功能
 * #define _XOPEN_SOURCE
 *
 */
