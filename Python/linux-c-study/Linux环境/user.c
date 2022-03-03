#include <sys/types.h>
#include <pwd.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
	uid_t uid;
	gid_t gid;

	struct passwd *pw;
	uid=getuid();
	gid=getgid();

	//getlogin函数返回当前用户的登录名
	printf("User is %s\n",getlogin());
	//输出当前用户的UID和GID
	printf("User IDs:uid=%d,gid=%d\n",uid,gid);
	
	//通过当前用户UID获得该用户信息
	pw=getpwuid(uid);
	printf("UID passwd entry:\n name=%s,uid=%d,gid=%d,home=%s,shell=%s\n",pw->pw_name,pw->pw_uid,pw->pw_gid,pw->pw_dir,pw->pw_shell);

	//通过用户名获得该用户信息
	pw=getpwnam("root");
	printf("root passwd entry:\n");
	printf("name=%s,uid=%d,gid=%d,home=%s,shell=%s\n",pw->pw_name,pw->pw_uid,pw->pw_gid,pw->pw_dir,pw->pw_shell);

	exit(0);
}
