#include <stdio.h>
int main()
{
	FILE *fp;
	int c,i=1;
	fp=fopen("fgetc.c","r");
	printf("%d\t",i);	
	while((c=fgetc(fp))!=EOF){
		if((char)c=='\n'){
			printf("\n%d\t",++i);
		}else{
			printf("%c",c);
		}
	}
	fclose(fp);
}
