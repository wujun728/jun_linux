#include <sys/select.h>
#include <sys/time.h>
#include <unistd.h>
#include <sys/types.h>
int child_events=0;
void child_sig_handler(int x){
	child_events++;
	signal(SIGCHLD,child,child_sig_events);
}
int main(){
	sigset_t sigmask,orig_sigmask;
	sigemptyset(&sigmask);
	sigaddset(&sigmask,SIGCHLD);
	sigprocmask(SIG_BLOCK,&sigmask,&orig_sigmask);
	signal(SIGCHLD,child_sig_handler());
	for(;;){
		for(;child_events > 0;child_events--){
			/*处理动作*/
		}
		r=pselect(nfds,&rd,&wr,&er,0,&orig_sigmask);
	}
}
