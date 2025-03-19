#!/bin/sh
#chkconfig:35 88 20
#description:redis.sh
#redis单机版启动脚本
# redis-server启动会自动创建pid文件,pid文件的路劲在redis.conf中设置

##########################
# custom variables start
###########################
APP_HOME=/opt/redis
PROG=redis
CONF=/$APP_HOME/conf/redis.conf
PID_FILE=/var/run/redis.pid
EXEC=$APP_HOME/bin/redis-server

###########################
# custom variables end
###########################
. /etc/init.d/functions
#########################
# define funcation start
##########################

#创建lockfile文件
createLockFile(){
	lock_dir=/var/lock/subsys
	lock_file=$lock_dir/$PROG
	[ -w $lock_dir ] && touch $lock_file
}

start(){
	if [ -f $PID_FILE ]
	then
		echo "$PID_FILE exists, process is already running or crashed"
	else
		$EXEC $CONF
		if [ $? = 0 ];then
			createLockFile
			echo "Starting Redis server..."
		fi
	fi
}

stop(){
	if [ ! -f $PID_FILE ]
	then
		echo "$PID_FILE does not exist, process is not running"
	else
		killproc -p $PID_FILE
		echo "Stopping ..."
		if [ $? = 0 ];then
			rm -f $lock_file
			echo "Waiting for Redis to shutdown ..."
			sleep 1
			echo "successed"
		else
			echo "failed"
		fi
	fi
}

##########################
# define function end
##########################

case "$1" in
    start)
        start
        ;;
    stop)
		stop
        ;;
    restart)
		stop
		start
		;;
	*)
		echo " uages {start|stop|restart}"
esac