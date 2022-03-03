#include <stdio.h>
#include <stdlib.h>
#include <sys/uio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
static struct iovec *vs=NULL,*vc=NULL;
void sig_proccess(int signo){
	printf("catch a exit signal!\n");
	free(vc);
	free(vs);
	exit(1);
}
void sig_pipe(int sign){
	printf("catch a SIGPIPE signal\n");
	free(vc);
	free(vs);
}
void proccess_conn_server(int s){
	ssize_t size = 0;
	char buffer[30];
	struct msghdr msg;
	/*申请3个向量*/
	struct iovec *v=(struct iovec *)malloc(3*sizeof(struct iovec));
	if(!v){
		printf("not have enough memory\n");
	}
	vs = v;	/*挂载全局变量，便于释放管理*/
	/*初始化消息*/
	msg.msg_name = NULL;
	msg.msg_namelen = 0;
	msg.msg_control = NULL;
	msg.msg_controllen = 0;
	msg.msg_iov = v;
	msg.msg_iovlen = 30;
	msg.msg_flags = 0;

	v[0].iov_base = buffer;
	v[1].iov_base = buffer + 10;
	v[2].iov_base = buffer + 20;
	v[0].iov_len = v[1].iov_len = v[2].iov_len = 10;

	for(;;){
		size = recvmsg(s,&msg,0);	/*从套接字s中读取3块数据到向量v中*/
		write(1,"get data\n",9);
		if(size == 0){
			return;
		}
		sprintf(v[0].iov_base,"%d ",size);
		sprintf(v[1].iov_base,"bytes alt");
		sprintf(v[2].iov_base,"ogether\n");
		/*写入字符串长度*/
		v[0].iov_len = sizeof(v[0].iov_base);
		v[1].iov_len = sizeof(v[1].iov_base);
		v[2].iov_len = sizeof(v[2].iov_base);
		//write(1,v[0].iov_base,size);
		sendmsg(s,&msg,0);
	}
	
}
void proccess_conn_client(int s){
	ssize_t size = 0;
	char buffer[30];
	struct msghdr msg;
	struct iovec *v=(struct iovec *)malloc(3*sizeof(struct iovec));
	if(!v){
		printf("not enough memory\n");
		return;
	}
	vc = v;
	msg.msg_name = NULL;
	msg.msg_namelen = 0;
	msg.msg_control = NULL;
	msg.msg_controllen = 0;
	msg.msg_iov = v;
	msg.msg_iovlen = 30;
	msg.msg_flags = 0;

	v[0].iov_base = buffer;
	v[1].iov_base = buffer + 10;
	v[2].iov_base = buffer + 20;
	v[0].iov_len = v[1].iov_len = v[2].iov_len = 10;
	int i = 0;
	for(;;){
		size = read(0,v[0].iov_base,10);
		if(size > 0){
			v[0].iov_len = size;
			sendmsg(s,&msg,0);
			v[0].iov_len = v[1].iov_len = v[2].iov_len = 10;
			size = recvmsg(s,&msg,0);
			for(i = 0;i < 3;i++){
				if(v[i].iov_len > 0){
					write(0,v[i].iov_base,v[i].iov_len);
				}
			}
		}
	}
}
