#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <signal.h>
#include "common.h"

#define PORT 8888
#define BACKLOG 2	/*侦听队列长度*/
int main(){
	int ss,sc;
	struct sockaddr_in server_addr;
	struct sockaddr_in client_addr;	/*客户端地址结构*/
	int err;
	pid_t pid;

	signal(SIGINT,sig_proccess);
	signal(SIGPIPE,sig_pipe);

	ss = socket(AF_INET,SOCK_STREAM,0);
	if(ss < 0){
		printf("socket error\n");
		return -1;
	}

	bzero(&server_addr,sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	server_addr.sin_port = htons(PORT);
	/*绑定地址结构到套接字描述符*/
	err = bind(ss,(struct sockaddr *)&server_addr,sizeof(server_addr));
	if(err < 0){
		printf("bind error\n");
		return -1;
	}
	err = listen(ss,BACKLOG);	/*设置侦听队列长度*/
	if(err < 0){
		printf("listen error\n");
		return -1;
	}
	for(;;){
		int addrlen = sizeof(struct sockaddr);
		sc = accept(ss,(struct sockaddr *)&client_addr,&addrlen);
		if(sc < 0){
			continue;
		}
		/*建立一个新进程来处理到来的连接*/
		pid = fork();
		if(pid == 0){
			close(ss);
			proccess_conn_server(sc);
		}else{
			close(sc);
		}
	}

}
