#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/if_ether.h>
#include <net/if.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int fd;

void main(){
	fd=socket(AF_INET,SOCK_STREAM,htons(0x0003));
	char ef[ETH_FRAME_LEN];
	struct ethhdr* p_ethhdr;
	int n;
	p_ethhdr=(struct ethhdr*)ef;//使p_ethhdr指向以太网帧的帧头
	n=read(fd,ef,ETH_FRAME_LEN);
	printf("dest MAC:\n");
	for(int i=0;i<ETH_ALEN-1;i++){
		printf("%02x-",p_ethhdr->h_dest[i]);
	}
	printf("\n%02x\n",p_ethhdr->h_dest[ETH_ALEN-1]);
	printf("source MAC:\n");
	for(int i=0;i<ETH_ALEN-1;i++){
		printf("%02x-",p_ethhdr->h_source[i]);
	}
	printf("\n%02x\n",p_ethhdr->h_dest[ETH_ALEN-1]);
	printf("protocol:0x%04x\n",ntohs(p_ethhdr->h_proto));


}
