#!/bin/sh
# chkconfig:35 85 15
# description:webssh
ulimit -n 102400
ulimit -u 102400
#############################
# get app_home start
#############################
PRG="$0"
while [ -h "$PRG" ]; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done
APP_HOME=`dirname "$PRG"`
PRG=`basename $PRG`
################################
# get app_home end
#############################

##########################
# custom variables start
###########################
EXEC=/usr/local/bin/wssh
ARGS="--policy=reject --fbidhttp=False"
PID_FILE=/var/run/webssh.pid
LOG=/var/log/webssh/webssh.log
CMD="$EXEC $ARGS"
lock_file=/var/lock/subsys/$PRG
###########################
# custom variables end
###########################

source /etc/init.d/functions
#########################
# define funcation start
##########################
start(){
	#创建日志目录
	if [ -e $PID_FILE ];then
		echo "$PRG already running...."
  else
    echo "Starting $PRG:"
		echo $CMD
		nohup $CMD >> $LOG 2>&1 &
    if [ $? = 0 ];then
			touch $lock_file
			echo $! > $PID_FILE
			echo "successed"
		else
		  echo
			echo "failed"
		fi
 fi
	
}

stop(){
	if [ -e $PID_FILE ];then
		echo "Stopping $PRG:"
		killproc -p $PID_FILE
		if [ $? = 0 ];then
			rm -f $lock_file
			rm -rf $PID_FILE
			echo "successed"
		else
		  echo
			echo "failed"
		fi
	else
		echo "$PRG not start"
	fi
}

restart(){
	stop
	sleep 2
	start
}

status(){
	cat $PID_FILE
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
