#!/bin/bash
# chkconfig: 345 99 01
# description:springmvc

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
#如果系统中不存在java_home,手动指定java_home
if [ 0"$JAVA_HOME" = "0" ]; then
  JAVA_HOME=/usr/java/jdk1.8.0_211
fi


#JAVA_OPTS="-Xdebug -Xrunjdwp:server=y,transport=dt_socket,suspend=n"
JAVA_OPTS="-XX:+HeapDumpOnOutOfMemoryError"
APP_NAME=`basename "$PRG"`
APP_HOME=`dirname "$PRG"`
CONF_FILE=$APP_HOME/application.properties
PID_FILE=$APP_HOME/$APP_NAME.pid
MAIN_JAR=$APP_HOME/*.$2
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

#读取配置文件
read_application_properties(){
  retval=""
  if [ -f $CONF_FILE ]
  then
    while read line
    do
      contains=$(echo $line|grep "^#")
      if [[ "$contains" == "" ]];then 
        if [ ! -z $line ]; then 
          retval="$retval --$line"
        fi      
      fi
    done < $CONF_FILE
  fi
  echo "$retval"
}

start (){
  [ -e $APP_HOME/logs ] || mkdir $APP_HOME/logs -p

  if [ -f $PID_FILE ]
  then
    echo 'alread running...'
  else
    APP_ARGS=$(read_application_properties)
    CMD="$JAVA_HOME/bin/java $JAVA_OPTS -jar $MAIN_JAR $APP_ARGS"
    echo $CMD
    echo $CMD >> $APP_HOME/logs/$APP_NAME.log
    nohup $CMD >> $APP_HOME/logs/$APP_NAME.log 2>&1 &
    echo $! > $PID_FILE
    createLockFile
    echo [OK]
  fi
}

stop(){
  if [ -f $PID_FILE ]
  then
    kill `cat $PID_FILE`
    rm -f $PID_FILE
    echo [OK]
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

