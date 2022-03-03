/*
 * keypad模式下处理箭盘上的方向键和功能键
 */
#include <unistd.h>
#include <curses.h>
#include <stdlib.h>

#define LOCAL_ESCAPE_KEY 27

int main()
{
	int key,i;

	initscr();
	crmode();
	keypad(stdscr,TRUE);
	noecho();
	clear();
	mvprintw(5,5,"Key pad demonstration. Press 'q' to quit");
	move(7,5);
	refresh();
	key=getch();

	i=7;
	while(key != ERR && key != 'q'){
		move(i,5);
		clrtoeol;

		if((key >= 'A' && key <='Z') || 
				(key >= 'a' && key <= 'z')){
			printw("key was %c",(char)key);
		}else{
			switch(key){
				case LOCAL_ESCAPE_KEY:
					printw("%s","Escape key");
					break;
				case KEY_END:
					printw("%s","End key");
					break;
				case KEY_BEG:
					printw("%s","Escape key");
					break;
				case KEY_RIGHT:
					printw("%s","Right key");
					break;
				case KEY_LEFT:
					printw("%s","Left key");
					break;
				case KEY_UP:
					printw("%s","Up key");
					break;
				case KEY_DOWN:
					printw("%s","Down key");
					break;
				default:
					printw("%s%d","Unknow key:",key);
			}
		}
		refresh();
		key = getch();
		i++;

	}
	endwin();
	exit(EXIT_SUCCESS);
}
