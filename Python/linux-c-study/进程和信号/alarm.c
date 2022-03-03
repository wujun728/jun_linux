#include <sys/types.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

static int alarm_fired=0;

void ding(int sig){
	alarm_fired = 1;
}

int main(){
	pid_t pid;
	printf("alarm application starting\n");

	//创建子进程
	pid = fork();
	switch(pid){
		case -1:
			perror("fork failed!\n");
			exit(1);
		case 0://子进程
			sleep(5);
			printf("i am sub\n");
			kill(getppid(),SIGALRM);
			exit(0);
	}
	printf("waiting for alarm to go off\n");
	(void)signal(SIGALRM,ding);
	//挂起父进程，直到接收到子进程的信号
	pause();
	if(alarm_fired)
		printf("ding\n");
	printf("done\n");
	exit(0);
	
}


