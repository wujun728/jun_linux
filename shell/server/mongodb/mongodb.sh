#!/bin/bash
#chkconfig:2345 80 20
#description:mongodb
#mongodb单机版启动脚本
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
lock_name=`basename $PRG`
################################
# get app_home end
#############################

##########################
# custom variables start
###########################
EXEC=$APP_HOME/bin/mongod
PID_FILE=$APP_HOME/mongodb.pid
CONFIG=$APP_HOME/config/mongodb.conf

###########################
# custom variables end
###########################

##########################
# define funcation start
##########################
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$lock_name
createLockFile(){
    [ -w $lock_dir ] && touch $lock_file
}

start(){
	echo "Starting $PRG: "
	if [ -f $PID_FILE ]; then
		echo "$PRG Already Running!!"
	else
	    #启动程序
	    $EXEC --config $CONFIG
	    echo $! > $PID_FILE
	    createLockFile

	    if [ $? = 0 ]; then
	        echo "successed"
	    else
	        echo "failed"
	    fi
	fi
}

stop (){
    if [ -f $PID_FILE ];then
        $EXEC --config $CONFIG --shutdown
        rm -rf $PID_FILE $lock_file
    else
        echo "$PRG not running"
    fi
}

restart (){
	stop
	start
}
###########################
# define funcation end
###########################

##################################################
# Do the action
##################################################
ACTION=$1
case "$ACTION" in
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
		echo "usage {start|stop|restart}"
		;;
esac