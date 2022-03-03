#include <unistd.h>
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>
#include <stdlib.h>

void printdir(char *dir,int depth)
{
	DIR *dp;
	struct dirent *entry;
	struct stat statbuf;
	if((dp = opendir(dir))==NULL){//打开一个目录流
		fprintf(stderr,"can not open this directory:%s\n",dir);
		return;
	}
	chdir(dir);//将dir设为当前目录
	while((entry=readdir(dp))!=NULL){
		lstat(entry->d_name,&statbuf);//将当前路径信息保存到该结构体中
		if(S_ISDIR(statbuf.st_mode)){//判断该路径信息是否是一个目录
			//是目录的情况下，忽略掉"."和".."
			if(strcmp(".",entry->d_name)==0 ||
				strcmp("..",entry->d_name)==0){
				continue;
			}
			//输出目录名称
			printf("%*s%s/\n",depth,"",entry->d_name);
			//递归处理该目录
			printdir(entry->d_name,depth+4);
		}else{
			//不是目录的话则输出该文件信息
			printf("%*s%s(uid:%d,gid:%d)\n",depth,"",entry->d_name,statbuf.st_uid,statbuf.st_gid);
		}
	}
	chdir("..");
	closedir(dp);
	
}
int main(int argc,char *argv[])
{
	char *topdir=".";
	if(argc >= 2){
		topdir=argv[1];
	}
	printf("Directory scan of %s:\n----------------------------\n",topdir);
	printdir(topdir,0);
	printf("----------------------------\nDone.\n");
	exit(0);
}
