#include <stdio.h>
#include <term.h>
#include <curses.h>
#include <stdlib.h>

int main()
{
	int nrows,ncolumns;
	//初始化终端类型，第一个参数为空，则只用环境变量TERM的值，一般是xterm
	//如果该函数出错，会输出一条诊断信息unknown terminal type.并导致程序直接退出
	setupterm(NULL,fileno(stdout),(int *)0);
	//返回指定功数值能标志的值
	nrows=tigetnum("lines");
	ncolumns=tigetnum("cols");
	printf("This terminal has %d columns and %d rows\n",ncolumns,nrows);
	exit(0);
}
