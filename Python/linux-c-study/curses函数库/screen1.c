#include <unistd.h>
#include <stdlib.h>
#include <curses.h>

int main(){
	initscr();
		
	move(5,15);
	printw("%s","hello world");
	refresh();
	sleep(3);

	endwin();
	exit(EXIT_SUCCESS);
}
