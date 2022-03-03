#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void ouch(int sig){
	printf("OUCH! - I got signal %d\n",sig);
	//当前信号处理完成时，恢复信号的默认状态
	(void)signal(SIGINT,SIG_DFL);
}

int main(){
	(void)signal(SIGINT,ouch);
	while(1){
		printf("hello world!\n");
		sleep(1);
	}
}
