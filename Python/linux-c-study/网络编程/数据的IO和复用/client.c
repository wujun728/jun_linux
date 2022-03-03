#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <signal.h>
#include "common.h"

#define PORT 8888
static int s;
void sig_proccess_client(int signo){
	printf("catch a exit signal\n");
	close(s);
	exit(0);
}

int main(int argc,char *argv[]){
	struct sockaddr_in server_addr;
	int err;

	if(argc == 1){
		printf("please input server address!\n");
		return 0;
	}
	/*挂接SIGINT信号，处理函数为sig_proccess()*/
	signal(SIGINT,sig_proccess);
	/*挂接SIGPIPE信号，处理函数为sig_pipe()*/
	signal(SIGPIPE,sig_pipe);
	/*创建流式套接字*/
	s = socket(AF_INET,SOCK_STREAM,0);
	if(s < 0){
		printf("socket error!\n");
		return -1;
	}

	/*设置服务器地址*/
	bzero(&server_addr,sizeof(server_addr));	/*将地址结构清零*/
	server_addr.sin_family = AF_INET;	/*将协议族设置为AF_INET*/
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);	/*将IP设为本机IP*/
	server_addr.sin_port = htons(PORT);
	inet_pton(AF_INET,argv[1],&server_addr.sin_addr);	/*将用户输入的字符串类型的IP转换成整型*/
	connect(s,(struct sockaddr *)&server_addr,sizeof(struct sockaddr));	/*连接服务器*/
	proccess_conn_client(s);
	close(s);
}
