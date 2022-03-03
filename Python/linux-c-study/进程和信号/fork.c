#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(){
	pid_t pid;
	char *message;
	int n;
	int exit_code;

	printf("fork program starting\n");
	pid=fork();
	switch(pid){
		case -1:
			perror("fork faild");
			exit(1);
		case 0:
			message = "this is child";
			n=3;
			exit_code=37;
			break;
		default:
			message="this is the parent";
			n=5;
			exit_code=0;
			break;
	}
	for(;n>0;n--){
		puts(message);
		sleep(1);
	}
	//下面代码有主进程执行
	if(pid != 0){
		int stat_val;
		pid_t child_pid;

		//返回子进程的pid，并设置进程状态
		child_pid = wait(&stat_val);

		printf("child has finished: PID = %d\n",child_pid);
		//处理子进程的状态，状态值保存在stat_val
		if(WIFEXITED(stat_val)){
			printf("子进程的退出码为 %d\n",WEXITSTATUS(stat_val));
		}else{
			printf("子进程异常终止!\n");
		}
	}
	exit(exit_code);
}
/*
 * 如果子进在父进程之前结束，它不会被立刻释放，而是成为僵尸进程
 * /
