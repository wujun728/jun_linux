#include <stdlib.h>
#include <stdio.h>
extern char **environ;

int main()
{
	char **env = environ;
	printf("遍历输出系统环境变量：\n----------\n");
	while(*env){
		printf("%s\n",*env);
		env++;
	}
	printf("-----------\ndone\n");
	exit(0);
}
