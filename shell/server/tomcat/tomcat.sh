#!/bin/sh
# chkconfig: 345 99 01
# description:tomcat-server

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

echo $1;

#########################
# get APP_HOME end
#########################


##########################
# custom variables start
###########################
CATALINA_HOME=`dirname "$PRG"`
CATALINA_BASE=$CATALINA_HOME
PROG=tomcat
PID_FILE=/var/run/tomcat.pid
RETVAL=0
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$PROG
###########################
# custom variables end
###########################

#########################
# define funcation start
##########################
start(){	
	if [ -e $PID_FILE ];then 
		echo "$PROG already start"
	else 
		if [ -x $CATALINA_HOME/bin/startup.sh ];then
			$CATALINA_HOME/bin/startup.sh
			RETVAL=$!
			if [ $? = 0 ];then
				echo $RETVAL > $PID_FILE
				touch $lock_file
				echo "successed"
			else
				echo "failed"
			fi
		else
			echo "Permission denied $CATALINA_HOME/bin/startup.sh"
		fi
	fi
}

stop(){
	if [ ! -e $PID_FILE ];then 
		echo "$PROG not started"
	
	else 
		if [ -x $CATALINA_HOME/bin/shutdown.sh ];then
			echo $"Stopping Tomcat"
			$CATALINA_HOME/bin/shutdown.sh
			if [ $? = 0 ]; then 
				rm -f $PID_FILE $lock_file
				echo "successed"
			else
				echo "failed"
			fi
		fi

	fi
}

restart(){
	stop
	sleep 5
	start
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
	*)
		echo usage "{start|stop|restart|status}"
	;;
esac