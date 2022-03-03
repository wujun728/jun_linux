/*
 * 字节序转换的例子
 */
#include <stdio.h>
#include <arpa/inet.h>

/*16位字节序转换的结构*/
typedef union{
	unsigned short int value;//16位short类型变量，4个字节
	unsigned char byte[2];
}to16;
/*32位字节序转换的结构*/
typedef union{
	unsigned long int value;//32位long型变量，8个字节
	unsigned char byte[4];
}to32;

#define BITS16 16
#define BITS32 32
void showvalue(unsigned char *begin,int flag){
	int num=0,i=0;
	if(flag==BITS16){
		num=2;
	}else if(flag==BITS32){
		num=4;
	}
	for(i=0;i<num;i++){
		printf("%x ",*(begin+i));
	}
	printf("\n");
}
int main(){
	to16 v16_orig,v16_turn1,v16_turn2;
	to32 v32_orig,v32_turn1,v32_turn2;
	v16_orig.value = 0xabcd;
	v16_turn1.value = htons(v16_orig.value);//主机字节序到网络字节序的短整型转换
	v16_turn2.value = htons(v16_turn1.value);

	v32_orig.value = 0x12345678;
	v32_turn1.value=htonl(v32_orig.value);//主机字节序到网路字节序的长整型转换
	v32_turn2.value=htonl(v32_turn1.value);

	/*打印结果*/
	/*16位数值的原始值*/
	printf("16 host to network byte order change:\n");
	printf("\torig:\n");
	showvalue(v16_orig.byte,BITS16);
	/*16位数值第一次转换后的值*/
	printf("\t1 times:");
	showvalue(v16_turn1.byte,BITS16);
	/*16位数值的第二次转换后的值*/
	printf("\t2 times:");
	showvalue(v16_turn2.byte,BITS16);

	/*32位数值的原始值*/
	printf("32 host to network byte order change:\n");
	printf("\torig:\n");
	showvalue(v32_orig.byte,BITS32);
	/*32位数值第一次转换后的值*/
	printf("\t1 times:");
	showvalue(v32_turn1.byte,BITS32);
	/*32位数值的第二次转换后的值*/
	printf("\t2 times:");
	showvalue(v32_turn2.byte,BITS32);


}
/* 打印的结果：
 *
 * 16 host to network byte order change:
 *         orig:
 *        		cd ab
 *         1 times:ab cd
 *         2 times:cd ab
 * 32 host to network byte order change:
 *         orig:
 *              78 56 34 12
 *         1 times:12 34 56 78
 *         2 times:78 56 34 12
 *
 */
