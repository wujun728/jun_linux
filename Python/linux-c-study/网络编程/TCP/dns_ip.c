/*
 * 	IP地址与域名之间的相互转换
 */
#include <netdb.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>

int main(int argc,char *argv[]){
	char *host=NULL;
	if(argc==1){
		host="www.baidu.com";
	}else if(argc==2){
		host=argv[1];
	}else{
		host="www.baidu.com";
	}
	struct hostent *ht=NULL;
	char str[30];
	ht=gethostbyname(host);
	//打印相关信息
	if(ht){
		int i=0;
		printf("get the host:%s\n",host);
		printf("name:%s\n",ht->h_name);
		printf("type:%s\n",ht->h_addrtype==AF_INET?"IPv4":"IPv4");
		printf("length:%d\n",ht->h_length);
		//打印IP地址
		for(i=0;;i++){
			if(ht->h_addr_list[i]!=NULL){
				printf("IP:%s\n",inet_ntop(ht->h_addrtype,
										ht->h_addr_list[i],
										str,30));
			}else{
				break;
			}
		}
		for(i=0;;i++){
			if(ht->h_aliases[i]!=NULL){
				printf("alias %d:%s\n",i,ht->h_aliases[i]);
			}else{
				break;
			}
		}
		return 0;
	}else{
		printf("don't have more information about %s\n",host);
		return 1;
	}
}
