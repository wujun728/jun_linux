/*
 * 该小程序程序模仿了tee命令
 * 例如：cat test1.txt | ./tee.out ./test2.txt
 * 等于：cat test1.txt | tee ./test2.txt
 */
#include <stdio.h>
#include <stdlib.h>
#define SIZE 1

int main(int argc,char *argv[])
{
	//判断是否传入两个参数
	if(argc != 2){
		printf("please give me right argument!");
		exit(1);
	}

	FILE *fp;
	int nread;
	char c[SIZE];//用于存放数据的数组
	fp = fopen(argv[1],"w");//写方式打开该文件
	while((nread=fread(c,sizeof(char),SIZE,stdin)) > 0){
		printf("%s",c);//将字符输出到屏幕上
		fwrite(c,sizeof(char),SIZE,fp);//写入文件
	}
	fclose(fp);

}
/*
 * 不过在实际测试中发现一些问题：
 * 如果预先定义的长度大于实际读入的数据长度
 * 那么多出来的会被乱码填充
 * 而且对中文支持也不太好，屏幕会显示乱码，但写入文件的内容正常
 */
