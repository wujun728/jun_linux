#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(){
	printf("Running pas with execlp\n");
	//该函数会替换当前进程
	execlp("ps","ps","ax",0);
	printf("你肯定不会看到这条输出\n");
	exit(0);

}
/*
 * execlp()会从PATH 环境变量所指的目录中查找符合参数file的文件名，
 * 找到后便执行该文件，然后将第二个以后的参数当做该文件的argv[0]、argv[1]……，
 * 最后一个参数必须用空指针(NULL)作结束。如果用常数0来表示一个空指针，
 * 则必须将它强制转换为一个字符指针，否则将它解释为整形参数，
 * 如果一个整形数的长度与char * 的长度不同，那么exec函数的实际参数就将出错。
 * 如果函数调用成功,进程自己的执行代码就会变成加载程序的代码,
 * execlp()后边的代码也就不会执行了.
 */
