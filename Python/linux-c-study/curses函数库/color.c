/*
 * 处理终端颜色显示
 */
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <curses.h>

int main()
{
	int i;

	initscr();

	//检查终端是否支持彩色显示
	if(!has_colors()){
		endwin();
		fprintf(stderr,"Error - no color support on this terminal\n");
		exit(1);
	}

	//初始化终端色彩显示
	if(start_color() != OK){
		endwin();
		fprintf(stderr,"Error - could not initialize colors\n");
		exit(1);
	}

	clear();
	//输出色彩数和色彩模式
	mvprintw(5,5,"There are %d COLORS, and %d COLOR_PARIRS available",COLORS,COLOR_PAIRS);
	refresh();

	//初始化色彩
	//两个颜色分别代表前景色和背景色
	init_pair(1,COLOR_RED,COLOR_BLACK);
	init_pair(2,COLOR_RED,COLOR_GREEN);
	init_pair(3,COLOR_GREEN,COLOR_RED);
	init_pair(4,COLOR_YELLOW,COLOR_BLUE);
	init_pair(5,COLOR_BLACK,COLOR_WHITE);
	init_pair(6,COLOR_MAGENTA,COLOR_BLUE);
	init_pair(7,COLOR_CYAN,COLOR_WHITE);

	//循环显示不同色彩组合的效果
	for(i=1;i<= 7;i++){
		attroff(A_BOLD);
		attrset(COLOR_PAIR(i));
		mvprintw(5+i,5,"Color pair %d",i);
		attrset(COLOR_PAIR(i) | A_BOLD);
		mvprintw(5+i,25,"Bold color pair %d",i);
		refresh();
		sleep(2);
	}

	endwin();
	exit(EXIT_SUCCESS);
}
