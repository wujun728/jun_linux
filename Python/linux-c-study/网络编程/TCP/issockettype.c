/*
 *	套接字描述符判断函数
 *	是套接字返回1
 *	不是套接字返回0
 */
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/stat.h>

int issockettype(int fd){
	struct stat st;
	int err = fstat(fd,&st);	/*获得文件状态*/
	if(err<0){
		return -1;
	}
	if((st.st_mode & S_IFMT)==S_IFSOCK){	/*比较是否是套接字描述*/
		return 1;
	}else{
		return 0;
	}
}

int main(){
	int ret = issockettype(0);
	printf("value %d\n",ret);
	int s=socket(AF_INET,SOCK_STREAM,0);
	ret = issockettype(s);
	printf("value %d\n",ret);
	return 0;
}
