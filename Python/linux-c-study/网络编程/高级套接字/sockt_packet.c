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
#include <string.h>

int fd;

void main(){
	fd=socket(AF_INET,SOCK_PACKET,htons(0x0003));
	char* ethname="eth0";
	int i;
	struct ifreq ifr;
	strcpy(ifr.ifr_name,ethname);
	i=ioctl(fd,SIOCGIFFLAGS,&ifr);
	if(i<0){
		close(fd);
		perror("can't get flags\n");
		return -1;
	}else{
		printf("success!!\n");
	}
	ifr.ifr_flags|=IFF_PROMISC;
	i=ioctl(fd,SIOCGIFFLAGS,&ifr);
	i=ioctl(fd,SIOCSIFFLAGS,&ifr);
	if(i<0){
		perror("promiscuous set error\n");
		return -2;
	}else{
		printf("success!!\n");
	}
}
