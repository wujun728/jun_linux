#include <stdio.h>
#include <term.h>
#include <curses.h>
#include <stdlib.h>

int main()
{
	char *cursor;
	char *esc_sequence;
	//在对终端进行操作之前，必须要先对终端进行初始化
	setupterm(NULL,fileno(stdout),(int *)0);
	//获取xterm终端类型的光标移动功能标志cup的值
	cursor=tigetstr("cup");
	//用实际数值替换功能参数标志中的参数，并返回一个可用的escape转义序列
	esc_sequence=tparm(cursor,5,30);
	//将该转移序列发送到终端
	putp(esc_sequence);
	printf("The cursor has been moved\n");
	exit(0);
}
