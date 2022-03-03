#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 8888
#define BACKLOG 2

void process_conn_server(int s);

int main(){
	int ss,sc;/*ss是服务端socket描述符，sc为客户端socket描述符*/
	struct sockaddr_in server_addr;
	struct sockaddr_in client_addr;
	int err;
	pid_t pid;
	/*建立一个流式套接字*/
	ss=socket(AF_INET,SOCK_STREAM,0);
	if(ss<0){ /*出错*/
		printf("socket error!\n");
		return -1;
	}
	/*设置服务器地址*/
	bzero(&server_addr,sizeof(server_addr));/*清零*/
	server_addr.sin_family=AF_INET;/*协议族*/
	server_addr.sin_addr.s_addr=htonl(INADDR_ANY);/*本地地址*/
	server_addr.sin_port=htons(PORT);/*服务器端口*/
	/*绑定地址结构到套接字描述符*/
	err=bind(ss,(struct sockaddr *)&server_addr,sizeof(server_addr));
	if(err<0){
		printf("bind error\n");
		return -1;
	}
	/*设置侦听*/
	err=listen(ss,BACKLOG);
	if(err<0){
		printf("listen error\n");
		return -1;
	}
	/*主循环过程*/
	for(;;){
		socklen_t addrlen=sizeof(struct sockaddr);
		sc=accept(ss,(struct sockaddr *)&client_addr,&addrlen);
		/*接收客户端连接*/
		if(sc<0){
			continue;
		}
		process_conn_server(sc);
	}
}

void process_conn_server(int s){
	ssize_t size=0;
	char buffer[1024];/*数据缓冲区*/

	for(;;){
		size=read(s,buffer,1024);/*从套接字中读取数据到缓冲区*/
		if(size==0){
			return;
		}
		/*构建响应字符，并发送给客户端*/
		sprintf(buffer,"%d bytes altogether\n",size);
		write(s,buffer,strlen(buffer)+1);
	}
}
