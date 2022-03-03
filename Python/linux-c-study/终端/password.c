#include <termios.h>
#include <stdio.h>
#include <stdlib.h>

#define PASSWORD_LAN 8

int main()
{
	struct termios init,new;
	char password[PASSWORD_LAN+1];
	//该语句用于获取标准输入的当前设置，并将其保存到刚才创建的termios结构中
	tcgetattr(fileno(stdin),&init);
	new=init;
	new.c_lflag &=~ECHO;

	printf("Enter passwprd:");

	//接下来用new变量中的值设置终端属性并读取用户密码。然后还原设置并输出密码
	if(tcsetattr(fileno(stdin),TCSAFLUSH,&new)!=0){
		fprintf(stderr,"Could not set attributes\n");
	}else{
		fgets(password,PASSWORD_LAN,stdin);
		tcsetattr(fileno(stdin),TCSANOW,&init);
		fprintf(stdout,"\nYou entered %s\n",password);
	}
	exit(0);
}
