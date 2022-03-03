#include <unistd.h>
#include <stdlib.h>
#include <curses.h>
#include <string.h>

#define PW_LEN 256
#define NAME_LEN 256

int main()
{
	char name[NAME_LEN];
	char password[PW_LEN];
	const char *real_pwd="123456";
	int i=0;

	initscr();

	move(5,10);
	printw("%s","Please login:");

	move(7,10);
	printw("%s","Username: ");
	getstr(name);

	move(8,10);
	printw("%s","Password: ");
	refresh();

	cbreak();//该模式下，键盘一经输入就立刻返回
	noecho();//关闭回显模式
	
	//分配存储密码的内存空间
	memset(password,'\0',sizeof(password));
	while(i<PW_LEN){
		//循环获取每一个输入的字符
		password[i]=getch();
		//当遇到'\n'则结束
		if(password[i]=='\n') break;
		move(8,20+i);
		//用'*'代替输入的字符
		addch('*');
		refresh();
		i++;
	}
	echo();
	nocbreak();

	move(11,10);
	if(strncmp(real_pwd,password,strlen(real_pwd))==0) printw("%s","Correct");
	else printw("%s","Wrong");
	printw("%s"," password  ");
	refresh();
	sleep(2);


	endwin();
	exit(EXIT_SUCCESS);

}
