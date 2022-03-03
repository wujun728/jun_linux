# 函数申明 #

----------

> 要使用termios.h头文件中的函数需要与函数库curses链接<br >
> gcc *.c -lcurses

#### termios结构 ####
	#include <termios.h>
	struct termios{
		tcflag_t c_iflag;//输入模式
		tcflag_t c_oflag;//输出模式
		tcflag_t c_cflag;//控制模式
		tcflag_t c_lflag;//本地模式
		cc_t c_cc[NCCS];//特殊控制字符
	};

#### 获取与当前终端对应的termios的结构 ####
	#include <termios.h>
	int tcgetattr(int fd,struct termios *termios_p);

#### 设置当前终端对应的termios ####
	#include <termios.h>
	int tcsetattr(int fd,int actions,const struct termios *termios_p);
参数actions控制修改方式：

- TCSANOW : 立即对值修改<br />
- TCSADRAIN : 等当前输出完成后再对值进行修改
- TCSAFLUSH : 	 等当前输出完成后再对值进行修改，但丢弃还未从read调用返回的当前可用的任何输入

> 程序有责任将终端设置恢复到程序开始之前运行的状态，这一点是非常重要的。


**如果没有安装curses函数库，得提前安装<br />`sudo apt-get install libncurses5-dev`**


