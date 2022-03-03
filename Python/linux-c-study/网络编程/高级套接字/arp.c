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

#define LOCAL_IP "192.168.1.109"
#define DEST_IP "192.168.1.107"
struct arppacket{
	unsigned short ar_hrd;	//硬件类型
	unsigned short ar_pro;	//协议类型
	unsigned char ar_hln;	//硬件地址长度
	unsigned char ar_pln;	//协议地址长度
	unsigned short ar_op;	//arp操作码
	unsigned char ar_sha[ETH_ALEN];	//发送方MAC地址
	unsigned char* ar_sip;	//发送方IP
	unsigned char ar_tha[ETH_ALEN];	//目的MAC地址
	unsigned char* ar_tip;	//目的IP地址
};

int main(){
	char ef[ETH_FRAME_LEN];	//以太网帧缓冲区
	struct ethhdr* p_ethhdr;	//以太网头部指针
	char eth_dest[ETH_ALEN]={0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};
	char eth_source[ETH_ALEN]={0x00,0x50,0x56,0x2f,0x32,0x09};	//源以太网地址
	
	int fd;
	fd=socket(AF_INET,SOCK_PACKET,htons(0x003));
	/*使p_ethhdr指向以太网的帧头*/
	p_ethhdr=(struct ethhdr*)ef;
	/*复制目的以太网地址*/
	memcpy(p_ethhdr->h_dest,eth_dest,ETH_ALEN);
	/*复制源以太网地址*/
	memcpy(p_ethhdr->h_source,eth_source,ETH_ALEN);
	/*设置协议类型，以太网0x0806*/
	p_ethhdr->h_proto=htons(0x0806);

	struct arppacket* p_arp;
	p_arp=(struct arppacket*)(ef+ETH_HLEN);	//定位ARP包地址
	p_arp->ar_hrd=htons(0x1);	//arp硬件类型
	p_arp->ar_pro=htons(0x0800);	//协议类型
	p_arp->ar_hln=6;	//硬件地址长度
	p_arp->ar_pln=4;	//IP地址长度

	memcpy(p_arp->ar_sha,eth_source,ETH_ALEN);
	p_arp->ar_sip=(unsigned char*)inet_addr(LOCAL_IP);
	memcpy(p_arp->ar_tha,eth_dest,ETH_ALEN);
	p_arp->ar_tip=(unsigned char*)inet_addr(DEST_IP);
	int i=0;
	for(i=0;i<8;i++){
		write(fd,ef,ETH_FRAME_LEN);
		sleep(1);
	}
	close(fd);
	return 0;
}
