/*
 * 菜单示例程序的最终版本
 * 程序运行时会清屏，选择菜单项后也会执行清屏操作
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <term.h>
#include <curses.h>

static FILE *output_stream=(FILE *)0;

char *menu[] = {
	"a - add new record",
	"d - delete record",
	"q - quit",
	NULL,
};
int getchoice(char *greet,char *choices[],FILE *in,FILE *out);
int char_to_terminal(int char_to_write);

int main()
{
	int choice = 0;
	FILE *input;
	FILE *output;
	struct termios init,new;
	//判断是否是将信息输出到屏幕上，禁止重定向
	if(!isatty(fileno(stdout))){
		fprintf(stderr,"You are not a terninal!\n");
	}
	input = fopen("/dev/tty","r");
	output = fopen("/dev/tty","w");
	if(!input || !output){
		fprintf(stderr,"Unable to open /dev/tty\n");
		exit(1);
	}
	tcgetattr(fileno(input),&init);
	new=init;
	new.c_lflag &= ~ICANON;
	new.c_lflag &= ~ECHO;
	new.c_cc[VMIN] = 1;
	new.c_cc[VTIME] =0;
	new.c_lflag &= ~ISIG;//禁用对类似ctrl+c的组合件的处理
	if(tcsetattr(fileno(input),TCSANOW,&new)!=0){
		fprintf(stderr,"Could not set attributes\n");
	}
	do{
		choice = getchoice("please select an action",menu,input,output);
		printf("You have chosen:%c\n",choice);
		sleep(1);
	}while(choice != 'q');
	//还原设置
	tcsetattr(fileno(input),TCSANOW,&init);
	exit(0);
}

int getchoice(char *greet,char *choices[],FILE *in,FILE *out)
{
	int chosen = 0;
	int selected;
	int screenrow,screencol=10;
	char **option;
	char *cursor,*clear;

	output_stream=out;

	setupterm(NULL,fileno(out),(int *)0);
	cursor=tigetstr("cup");
	clear=tigetstr("clear");

	screenrow=4;
	tputs(clear,1,char_to_terminal);
	tputs(tparm(cursor,screenrow,screencol),1,char_to_terminal);
	fprintf(out,"choice: %s", greet);
	screenrow +=2;
	option=choices;
	while(*option){
		tputs(tparm(cursor,screenrow,screencol),1,char_to_terminal);
		fprintf(out,"%s",*option);
		screenrow++;
		option++;
	}
	fprintf(out,"\n");
	do{
		fflush(out);
		selected=fgetc(in);
		option = choices;
		while(*option){
			if(selected == *option[0]){
				chosen = 1;
				break;
			}
			option++;
		}
		if(!chosen){
			tputs(tparm(cursor,screenrow,screencol),1,char_to_terminal);
			fprintf(out,"Incorrect choice, select again\n");
		}
	}while(!chosen);
	tputs(clear,1,char_to_terminal);
	return selected;
}
int char_to_terminal(int char_to_write)
{
	if(output_stream) putc(char_to_write,output_stream);
	return 0;
}
