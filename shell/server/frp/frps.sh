#!/bin/sh
#chkconfig:345 98 02
#description:fps.sh

###########################
# custom variables start
###########################
APP_HOME=/opt/frp
APP_NAME=frp
PID_FILE=/var/run/$APP_NAME.pid
CMD="$APP_HOME/frps -c $APP_HOME/frps.ini"

###########################
# custom variables end
###########################
source /etc/init.d/functions
##########################
# define funcation start
##########################
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$APP_NAME
createLockFile(){
  [ -w $lock_dir ] && touch $lock_file
}

start(){
  if [ -f $PID_FILE ]
  then
    echo 'alread running...'
  else
    echo $CMD
    nohup $CMD >> /var/log/$APP_NAME.log 2>&1 &
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