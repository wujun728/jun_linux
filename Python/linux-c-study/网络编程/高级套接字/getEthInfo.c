/*
 * 该示例程序用于获得linux环境下各种网络的配置信息
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if_arp.h>
#include <linux/sockios.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>

int s;

void printInfo(char* name){
	struct ifreq ifr;
	char *hw;	//保存硬件地址
	struct sockaddr_in* sin;	//保存IP地址
	char ip[16];	//字符串形式的IP地址

	printf("接口<%s>的参数信息:\n",name);
	/*获取MAC地址*/
	memcpy(ifr.ifr_name,name,sizeof(name));
	ioctl(s,SIOCGIFHWADDR,&ifr);
	hw=ifr.ifr_hwaddr.sa_data;
	printf("\tMAC:%02x:%02x:%02x:%02x:%02x:%02x\t",hw[0],hw[1],hw[2],hw[3],hw[4],hw[5]);

	/*获取IP地址*/
	sin=(struct sockaddr_in*)&ifr.ifr_addr;
	ioctl(s,SIOCGIFADDR,&ifr);
	inet_ntop(AF_INET,&sin->sin_addr.s_addr,ip,16);
	printf("\tIP address:%s\n",ip);


	/*输出结束*/
	printf("\n");
	printf("\n");

}
int main(int argc,char* argv[]){
	s=socket(AF_INET,SOCK_DGRAM,0);
	if(s<0){
		perror("socket() error");
		return -1;
	}
	if(argc==2){
		printInfo(argv[1]);
	}else{
		int i=0;
		unsigned char buf[2048];
		struct ifconf all_if;
		struct ifreq *ifr;
		all_if.ifc_len = sizeof(buf);
		all_if.ifc_buf=buf;
		ioctl(s, SIOCGIFCONF, &all_if); //获取所有接口信息
		ifr = (struct ifreq*)buf;
		for (i=(all_if.ifc_len/sizeof(struct ifreq)); i>0; i--)
		{
			printInfo(ifr->ifr_name);
			ifr++;
		}
	}

}
