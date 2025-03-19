#!/bin/bash
# description: apache of xampp
# chkconfig: - 85 15

PRG="$0"
while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done
##########################
# custom variables start
###########################
#APP_HOME=`dirname "$PRG"`
APP_HOME=/opt/lampp
APP_NAME=`basename "$PRG"`

###########################
# custom variables end
###########################
source /etc/init.d/functions

#########################
# define funcation start
##########################
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$APP_NAME
createLockFile(){
	[ -w $lock_dir ] && touch $lock_file	
}
start(){
	$APP_HOME/xampp startapache
	createLockFile
	echo_success
}

stop(){
	$APP_HOME/xampp stopapache
	echo_success
}

restart(){
	$APP_HOME/xampp restartapache
}

status(){
	$APP_HOME/xampp status
}


##########################
# define function end
##########################
ACTION=$1
case $ACTION in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		restart
		;;
	status)
		status
		;;
	*)
		echo usage "{start|stop|restart|status}"
	;;
esac