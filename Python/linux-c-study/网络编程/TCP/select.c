#include <stdio.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
int main(){
	fd_set rd;
	struct timeval tv;
	int err;
	FD_ZERO(&rd);
	FD_SET(0,&rd);
	tv.tv_sec=5;
	tv.tv_usec=0;
	err=select(1,&rd,NULL,NULL,&tv);
	if(err=-1){
		perror("select()");
	}else if(err){
		printf("data is available now.\n");
	}else{
		printf("no data within five seconds.\n");
	}
	return 0;
}
