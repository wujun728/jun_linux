/*
 * 大端字节序和小端字节序
 */
#include <stdio.h>
/*共同体，所有变量指向同一块内存区域，长度以最长的变量为准*/
typedef union{
	unsigned short int value;
	unsigned char byte[2];
}to;
int main(){
	to typeorder;
	typeorder.value=0xabcd;
	/*小端字节序检查*/
	if(typeorder.byte[0]==0xcd && typeorder.byte[1]==0xab){
		printf("小端字节序"
				"byte[0]:0x%x,byte[1]:0x%x\n",
				typeorder.byte[0],
				typeorder.byte[1]);
	}
	if(typeorder.byte[0]==0xab && typeorder.byte[1]==0xcd){
		printf("大端字节序"
				"byte[0]:0x%x,byte[1]:0x%x\n",
				typeorder.byte[0],
				typeorder.byte[1]);
	}
	return 0;
}

