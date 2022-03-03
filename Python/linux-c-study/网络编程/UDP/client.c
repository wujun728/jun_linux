#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#define PORT_SERV 8888
#define BUFF_LEN 256

void client_echo(int s,struct sockaddr* server){
	char buff[BUFF_LEN]="UDP test!";
	struct sockaddr_in from;	/*服务器地址*/
	socklen_t len=sizeof(*server);
	sendto(s,buff,BUFF_LEN,0,server,len);
	recvfrom(s,buff,BUFF_LEN,0,(struct sockaddr*)&from,&len);
	printf("recved:%s\n",buff);
}
int main(){
	int s;
	struct sockaddr_in addr_serv;
	s=socket(AF_INET,SOCK_DGRAM,0);
	memset(&addr_serv,0,sizeof(addr_serv));	/*清空地址结构*/
	addr_serv.sin_family=AF_INET;
	addr_serv.sin_addr.s_addr=htonl(INADDR_ANY);
	addr_serv.sin_port=htons(PORT_SERV);
	client_echo(s,(struct sockaddr*)&addr_serv);	/*处理过程*/
	close(s);
	return 0;
}
