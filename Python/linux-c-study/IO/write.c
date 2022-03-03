#include <unistd.h>
#include <stdlib.h>
int main()
{
	if(write(1,"here is some data\n",18)!=18){
		write(2,"here is some data!!!",21);
	}	
	exit(0);
}
