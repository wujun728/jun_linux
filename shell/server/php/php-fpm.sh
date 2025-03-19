#!/bin/sh
# chkconfig: 345 99 01
# description:php-fpm-server

#########################
# get APP_HOME start
#########################
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
PRGDIR=`dirname "$PRG"`
PRG=`basename "$PRG"`


#########################
# get APP_HOME end
#########################
##########################
# custom variables start
###########################
PID=/var/run/$PRG.pid
EXEC=$PRGDIR/sbin/php-fpm

###########################
# custom variables end
###########################

#########################
# define funcation start
##########################
start(){
	if [ -f $PID ]; then
		echo "fail $PRG is running pid:$PID"
	else 
		$EXEC -g $PID
		echo "success $PRG is running pid:$PID"
	fi
}

stop(){
	if [ -f $PID ]; then 
		kill -INT `cat $PID`
	else
		echo "$PRG is not running"
	fi
}

restart(){
	if [ -f $PID ]; then 
		kill -USR2 `cat $PID`
	else
		echo "$PRG is not running"
	fi	
}

status(){
	if [ -f $PID ]; then 
		echo "$PRG is running pid:$PID"
	else
		echo "$PRG is not running"
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