#include <stdio.h>
#include <stdlib.h>
#define L_tmpname 20

int main()
{
	char tmpname[L_tmpname];
	char *filename;
	FILE *tmpfp;

	filename = tmpnam(tmpname);

	printf("临时文件名是:%s\n",filename);
	tmpfp = tmpfile();
	if(tmpfp)
		printf("临时文件打开成功！\n");
	else
		perror("tmpfile");
	exit(0);
}
/*
 * 系统在编译该文件时会给出一警告:
 * warning: the use of `tmpnam' is dangerous, better use `mkstemp'
 * 你要在生成临时文件名后尽快打开，以防止其他程序打开该同名文件
 * 所以应该使用tmpfile，最好使用mkstemp函数，尽可能的保证安全
 * #include <stdlib.h>
 * char *mktemp(char *template);
 * int mkstemp(char *template);
 * 其中template参数必须是一个以6个x字符结尾的字符串
 * mkstemp返回的是一个打开的、底层的文件描述符
 */
