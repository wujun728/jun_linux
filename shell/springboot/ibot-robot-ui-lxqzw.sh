#/bin/sh
# chkconfig: 345 99 01
# description:ibot-robot-ui-lxqzw

##############################
PRG="$0"
while [ -h "$0" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done
#############################
##########################
# custom variables start
###########################
APP_NAME=ibot-robot-ui-lxqzw
APP_HOME=`dirname "$PRG"`
PID_FILE=$APP_HOME/$APP_NAME.pid
APP_ARGS="--spring.config.location=$APP_HOME/config/"
CMD="/usr/local/jdk1.8.0_121/bin/java -jar $APP_HOME/boot/ibot-robot-ui-lxqzw-1.1.jar $APP_ARGS"
###########################
# custom variables end
###########################
source /etc/init.d/functions
#########################
# define funcation start
##########################
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$0
createLockFile(){
    [ -w $lock_dir ] && touch $lock_file
}

start (){
	[ -e $APP_HOME/logs ] || mkdir $APP_HOME/logs -p

	if [ -f $PID_FILE ]
	then
		echo 'alread running...'
	else
		echo $CMD
		nohup $CMD >> $APP_HOME/logs/$APP_NAME.log 2>&1 &
		echo $! > $PID_FILE
		createLockFile
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
	start
}

status(){
	if [ -f $PID_FILE ]
	then
		cat $PID_FILE
	else
		echo 'not running...'
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
