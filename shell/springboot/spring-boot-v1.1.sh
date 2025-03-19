#!/bin/sh
# chkconfig: 345 99 01
# description: spring-boot-app

##############################
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
#############################
##########################
# custom variables start
###########################

if [ 0"$JAVA_HOME" = "0" ]; then
  JAVA_HOME=/usr/java/jdk1.8.0_211
fi

APP_HOME=`dirname "$PRG"`
APP_NAME=`basename "$PRG"`
PID_FILE=$APP_HOME/$APP_NAME.pid

OOM="-XX:+HeapDumpOnOutOfMemoryError"
#JAVA_OPTS="-Xdebug -Xrunjdwp:server=y,transport=dt_socket,suspend=n"
CP="$APP_HOME/lib/*:$APP_HOME/config:$APP_HOME/static"
MAIN_CLASS="com.litong.spring.boot.video.player.Application"
MAIN_ARGS="--spring.profiles.active=online"
CMD="$JAVA_HOME/bin/java -Xverify:none $JAVA_OPTS -cp $CP $MAIN_CLASS $MAIN_ARGS"
###########################
# custom variables end
###########################

#########################
# define funcation start
##########################
lock_dir=/var/lock/subsys
lock_file=$lock_dir/$APP_NAME
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
    echo "[start success]"
  fi

}

stop(){
  if [ -f $PID_FILE ]
  then
    kill `cat $PID_FILE`
    rm -f $PID_FILE
    echo "[stop success]"
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