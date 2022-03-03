#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#define PORT_SERV 8888
#define BUFF_LEN 256

void server_echo(int s,struct sockaddr* client){
	int n;
	char buff[BUFF_LEN];
	socklen_t len;
	while(1){
		len=sizeof(*client);	/*注意！*/
		/*从客户端接收数据*/
		n=recvfrom(s,buff,BUFF_LEN,0,client,&len);
		/*将数据发送给客户端*/
		sendto(s,buff,n,0,client,len);
	}
}
int main(){
	int s;
	struct sockaddr_in addr_serv,addr_clie;
	s=socket(AF_INET,SOCK_DGRAM,0);
	memset(&addr_serv,0,sizeof(addr_serv));	/*清空地址结构*/
	addr_serv.sin_family=AF_INET;
	addr_serv.sin_addr.s_addr=htonl(INADDR_ANY);
	addr_serv.sin_port=htons(PORT_SERV);
	bind(s,(struct sockaddr*)&addr_serv,sizeof(addr_serv));
	server_echo(s,(struct sockaddr*)&addr_clie);	/*处理过程*/
	return 0;
}
