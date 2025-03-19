#!/bin/sh
#chkconfig:35 80 20
#description aria2c.sh
#启动 aria2c服务,无配置文件
ulimit -n 10240
ulimit -u 10240

#aria2c --enable-rpc=true --rpc-allow-origin-all=true --rpc-listen-port=6800 \
#--rpc-secret=pandownload --rpc-listen-all=true --disable-ipv6=true

##########################
# custom variables start
###########################
APP_PROG=/usr/bin/aria2c
PORT=6800
PID_FILE=/var/run/aria2c-server.pid
###########################
# custom variables end
###########################

APP_ARGS=--enable-rpc=true --rpc-allow-origin-all=true --rpc-listen-port=$PORT --rpc-secret=pandownload --rpc-listen-all=true --disable-ipv6=true

source /etc/init.d/functions

#########################
# define funcation start
##########################
start(){
	if [ -f $PID_FILE ]
	then
		echo 'alread running...'
	else
		nohup $APP_PROG $APP_ARGS &
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