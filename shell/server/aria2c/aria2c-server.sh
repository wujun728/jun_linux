#!/bin/sh
#chkconfig:35 80 20
#description aria2c.sh
#有配置文件
ulimit -n 10240
ulimit -u 10240

##########################
# custom variables start
###########################
APP_PROG=/usr/bin/aria2c
PID_FILE=/var/run/aria2c-server.pid
CONF=/etc/aria2/aria2.conf

###########################
# custom variables end
###########################


source /etc/init.d/functions

#########################
# define funcation start
##########################
start(){
	if [ -f $PID_FILE ]
	then
		echo 'alread running...'
	else
		$APP_PROG --conf-path=$CONF -D
		echo $! > $PID_FILE
		echo_success
	fi
}

stop(){
	if [ -f $PID_FILE ]
	then
		killproc -p $PID_FILE
		rm -f $PID_FILE
		echo_success
	else
		echo 'not running...'
	fi
}

restart(){
	stop
	sleep 3
	start
}

status(){
	if [ -f PID_FILE ]
	then
		echo 'running'
	else
		echo 'not running'
	fi
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