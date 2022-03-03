#include <unistd.h>
#include <stdlib.h>
#include <curses.h>

int main()
{
	WINDOW *new_window_ptr;
	WINDOW *popup_window_ptr;
	int x_loop;
	int y_loop;
	char a_letter='a';

	initscr();
	move(5,5);
	printw("%s","Testing multiple windows");
	refresh();
	for(y_loop=0;y_loop<LINES-1;y_loop++){
		for(x_loop=0;x_loop<COLS-1;x_loop++){
			//移动到屏幕的指定位置，并输出字符
			mvwaddch(stdscr,y_loop,x_loop,a_letter);
			a_letter++;
			if(a_letter>'z') a_letter='a';
		}
	}
	refresh();
	sleep(2);

	//创建一个新的窗口
	new_window_ptr=newwin(10,20,5,5);
	mvwprintw(new_window_ptr,2,2,"%s","hello world");
	mvwprintw(new_window_ptr,5,2,"%s","notice how very long lines wrap inside the window");
	wrefresh(new_window_ptr);
	sleep(2);
	a_letter='0';
	for(y_loop=0;y_loop<LINES-1;y_loop++){
		for(x_loop=0;x_loop<COLS-1;x_loop++){
			//移动到屏幕的指定位置，并输出字符
			mvwaddch(stdscr,y_loop,x_loop,a_letter);
			a_letter++;
			if(a_letter>'9') a_letter='0';
		}
	}
	refresh();
	sleep(2);

	//第二次循环输出的时候，新的窗口被遮住了
	//但该窗口本身并没有被修改，直接刷新什么效果也没有
	//得先调用touchwin函数让curses以为该窗口被刷新了
	touchwin(new_window_ptr);
	wrefresh(new_window_ptr);
	sleep(2);

	//再添加一个加框的重叠窗口
	popup_window_ptr=newwin(10,20,8,8);
	box(popup_window_ptr,'|','-');
	mvwprintw(popup_window_ptr,5,2,"%s","Pop Up Window!");
	wrefresh(popup_window_ptr);
	sleep(2);

	//然后，在清屏和删除这两个新窗口之前在屏幕上轮流显示他们
	touchwin(new_window_ptr);
	wrefresh(new_window_ptr);
	sleep(2);
	wclear(new_window_ptr);
	wrefresh(new_window_ptr);
	sleep(2);
	delwin(new_window_ptr);
	touchwin(popup_window_ptr);
	wrefresh(popup_window_ptr);
	sleep(2);
	delwin(popup_window_ptr);
	touchwin(stdscr);
	refresh();
	sleep(2);

	endwin();
	exit(EXIT_SUCCESS);
}
