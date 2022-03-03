#include <stdio.h>
#include <stdlib.h>

int main()
{
	register int i,k;
	register double sum=0.0;
	for(i=0;i<1000000000;i++){
		sum*=sum;
	}
	printf("done\n");
}
/*
 * 执行time ./register.out
 * 这是未设置寄存器变量的执行时间
 * real	0m8.077s
 * user	0m7.440s
 * sys	0m0.024s
 * 这是设置寄存器变量后的执行时间
 * real	0m1.825s
 * user	0m1.668s
 * sys	0m0.008s
 * 可以看出差距还是很明显的
 */
