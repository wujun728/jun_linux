/*
 * 该示例程序用于模拟DOS系统下kbhit函数
 * 该函数可检测在没有实际进行读写操作之前检测某个键是否被按过
 */
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <term.h>
#include <curses.h>
#include <unistd.h>

static struct termios init_settings,new_settings;
static int peek_character = -1;
void init_keyboard();
void close_keyboard();
int kbhit();
int readch();

int main()
{
	int ch = 0;

	init_keyboard();
	while(ch != 'q'){
		printf("looping\n");
		sleep(1);
		if(kbhit()){
			ch = readch();
			printf("you hit %c\n",ch);
		}
	}
	close_keyboard();
	exit(0);
}

//该函数将终端配置为“read调用直到有字符可以读取时才返回”的工作模式
void init_keyboard()
{
	tcgetattr(0,&init_settings);
	new_settings = init_settings;
	//设置终端参数
	new_settings.c_lflag &= ~ICANON;//关闭标准处理
	new_settings.c_lflag &= ~ECHO;//关闭回显
	new_settings.c_lflag &= ~ISIG;//关闭信号处理
	//以下值只能用于非标准模式，结合起来共同控制对输入的读取
	//MIN > 0,TIME = 0 read调用将一直等待，直到有MIN个字符读取才返回 
	new_settings.c_cc[VMIN] = 1;
	new_settings.c_cc[VTIME] = 0;
	tcsetattr(0,TCSANOW,&new_settings);

}

void close_keyboard()
{
	//还原终端设置
	tcsetattr(0,TCSANOW,&init_settings);
}

//该函数将终端工作模式改为“read调用检查输入并立刻返回”的工作模式
//在该函数中，你实际上已将按键对应的字符读取了，但它只在需要时才从readch函数读取
int kbhit()
{
	char ch;
	int nread;

	if(peek_character != -1)
		return 1;
	//read调用总是立刻返回。若有待处理字符则返回，没有则返回0
	new_settings.c_cc[VMIN]=0;
	tcsetattr(0,TCSANOW,&new_settings);
	nread = read(0,&ch,1);
	new_settings.c_cc[VMIN]=1;
	tcsetattr(0,TCSANOW,&new_settings);

	if(nread == 1){
		peek_character = ch;
		return 1;
	}
	return 0;

}

int readch()
{
	char ch;

	if(peek_character != -1){
		ch = peek_character;
		peek_character = -1;
		return ch;
	}
	read(0,&ch,1);
	return ch;

}
