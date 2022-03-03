/* 
 * 有关二维字符数组的示例
 */
#include <stdio.h>

void main()
{
	char weekname[][10]={
		"Monday",
		"Tuseday",
		"Wednesday",
		"Thursday",
		"Friday",
		"Saturday",
		"Sunday"
	};
	int year;
	int month;
	int day;

	printf("请输入年份：");
	scanf("%d",&year);

	printf("请输入月份：");
	scanf("%d",&month);

	printf("请输入日期：");
	scanf("%d",&day);

	if((month == 1) || (month == 2)){
		month += 12;
		year--;
	}
	int index;
	index = (day+2*month+3*(month + 1)/5+year+year/4-year/100+year/400)%7;
	printf("%d/%d/%d 这一天是%s\n",year,month,day,weekname[index]);
}
/*
 * 上面的二维数组没有指定第一维的长度，这时该长度有初始化字符串常量的个数来决定
 * weekname[index]是一个一维数组的首地址，其字符数组长度为10
 * 二位数组在内存中的存储方式为：
 * weekname[0] -> |M|o|n|d|a|y|\0|\0|\0|\0|
 * weekname[1] -> |T|u|e|s|d|a|y|\0|\0|\0|
 * ......
 */
