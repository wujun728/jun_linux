#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char *argv[])
{
	if(argc < 2){
		printf("argument error!!!\n");
		exit(1);
	}

	DIR *dirname;
	struct dirent *entry;
	int i=0;
	if((dirname=opendir(argv[1])) == (void *)0){
		printf("目录打开错误，请检查!!!\n");
	}
	
	while((entry=readdir(dirname))!=NULL){
		if(strcmp(".",entry->d_name)==0 ||
				strcmp("..",entry->d_name)==0){
			continue;
		}
		printf("%d.node:%d---name:%s\n",++i,(int)entry->d_ino,entry->d_name);
	}

}
/*
 * 更加直观的展示了文件目录扫描的过程，用法
 * ./dir.out /home/
 * 支持出于展示的目的，只能列出该文件夹下的文件及目录
 * 遍历目录详见printdir.c文件
 */
