/* getenv函数和putenv函数包含在stdlib.h中*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
	//分别用于保存环境变量的名称和值
	char *var,*value;
	if(argc ==1 || argc > 3){
		fprintf(stderr,"usage: environ var [value]\n");
		exit(1);
	}
	var = argv[1];
	//读取指定环境变量的值
	value = getenv(var);
	if(value)
		printf("Variable %s has value %s\n",var,value);
	else
		printf("Variable %s has no value\n",var);

	//如果传给程序3个参数，则意味着需要修改指定的环境变量的值
	if(argc==3){
		char *string;
		value = argv[2];
		//分配存储空间，大小为字符串 var=value\0 的长度
		string = malloc(strlen(var)+strlen(value)+2);
		if(!string){
			fprintf(stderr,"out of memory!\n");
			exit(0);
		}
		//将其连接成"名称=值"的格式
		strcpy(string,var);
		strcat(string,"=");
		strcat(string,value);
		printf("Calling putenv with:%s\n",string);
		if(putenv(string) != 0){
			fprintf(stderr,"putenv falied\n");
			free(string);
			exit(1);
		}
		//返回修改后的环境变量的值
		value = getenv(var);
		if(value)
			printf("New Value of %s is %s\n",var,value);
		else
			printf("New value of %s is null??\n",var);
	}
	exit(0);
}
/*
 * 说明：
 * 这些操作只对本程序有用，该程序对环境变量所做的改变，并不会传递到程序之外
 * 因为变量的值不会从子程序传播到父进程(shell)
 */
