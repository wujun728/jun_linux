#include <unistd.h>
#include <stdlib.h>
#include <curses.h>

int main()
{
	WINDOW *sub_window_ptr;
	int x_loop;
	int y_loop;
	int counter;
	char a_letter='1';

	initscr();

	for(y_loop=0;y_loop<LINES-1;y_loop++){
		for(x_loop=0;x_loop<COLS-1;x_loop++){
			mvwaddch(stdscr,y_loop,x_loop,a_letter);
			a_letter++;
			if(a_letter>'9') a_letter='1';
		}
	}
	//创建一个新的卷动子窗口，必须在刷新屏幕之前对父窗口调用touchwin函数
	sub_window_ptr=subwin(stdscr,10,20,10,10);
	scrollok(sub_window_ptr,1);

	touchwin(stdscr);
	refresh();
	sleep(2);
	//删除子窗口中的内容，重新输出一些文字，然后刷新它
	werase(sub_window_ptr);
	mvwprintw(sub_window_ptr,2,0,"%s","this window will now scroll");
	wrefresh(sub_window_ptr);
	sleep(2);

	for(counter=1;counter<10;counter++){
		wprintw(sub_window_ptr,"%s","this text is both wrapping and scrolling");
		//开启滚动后，在子窗口中，显示不下会自动向上滚动
		//同时也可以在输出完一行是时，再用scroll函数另起一行，接着输出
		scroll(sub_window_ptr);
		wrefresh(sub_window_ptr);
		sleep(2);
	}
	//循环结束后删除子窗口，并刷新屏幕
	delwin(sub_window_ptr);

	touchwin(stdscr);
	refresh();
	sleep(2);

	endwin();
	exit(EXIT_SUCCESS);
}
/*
 * 注意：子窗口的行为与新窗口非常相似，但区别是：子窗口没有独立的屏幕字符存储空间，
 * 他们与其父窗口共享同一字符存储空间
 * 这意味着，对子窗口的任何修改都会反映到其父窗口中去，所以删除子窗口时，屏幕显示不会发生变化
 *
 * 子窗口的作用是，提供一种更加简洁的方式来卷动另一窗口里的部分内容。
 */
