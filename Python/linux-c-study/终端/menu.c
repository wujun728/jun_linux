#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>

char *menu[] = {
	"a - add new record",
	"d - delete record",
	"q - quit",
	NULL,
};
int getchoice(char *greet,char *choices[],FILE *in,FILE *out);

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
	}while(choice != 'q');
	//还原设置
	tcsetattr(fileno(input),TCSANOW,&init);
	exit(0);
}

int getchoice(char *greet,char *choices[],FILE *in,FILE *out)
{
	int chosen = 0;
	int selected;
	char **option;
	do{
		fprintf(out,"Choice: %s\n",greet);
		option = choices;
		while(*option){
			fprintf(out,"%s\n",*option);
			option++;
		}
		do{
			selected = fgetc(in);
		}while(selected=='\n' || selected=='\r');//在非标准模式下默认的回车和换行符之间的映射已经不存在了，要对'\r'进行检查
		option = choices;
		while(*option){
			if(selected == *option[0]){
				chosen = 1;
				break;
			}
			option++;
		}
		if(!chosen){
			fprintf(out,"Incorrect choice, select again\n");
		}
	}while(!chosen);
	return selected;
}
/*
 *	do{
 *		selected = getchar();
 *	}while(selected=='\n');
 *	这段代码如果直接写成：
 *	selected = getchar();
 *	那么每当你做出正确选择的时候，屏幕上都会提示Incorrect choice, select again.
 *	原因是：
 *	Linux会暂存用户输入的内容，直到用户按下回车键，然后将用户选择的字符和紧随其后的回车符一起传递给程序，
 *	当你输完一个选项时并按下回车时，程序就调用getchar函数处理输入，而当下一次循环中，由于上一次的回车符尚未处理，
 *	再次调用getcgar函数时，它并不会等待你输入，而是直接取走上次的回车符
 * 
 *  如果不希望程序中与用户交互部分被重定向，但允许其他的输入和输出被重定向，你就需要将与用户交互的部分与stdout、stderr分开
 *  Linux踢狗一个特殊设备/dev/tty来解决这个问题，该设备始终指向当前终端或登录会话
 */
