#!/bin/sh
#chkconfig:2345 85 14
#description:spring-boot
#author litongjava
# 启动spring-boot项目,
# 本脚本适用于 使用独立的jar文件并且配置文件也在jar中,

##################################
# get app home
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
APP_HOME=`dirname "$PRG"`
##################################

##################################
# define variable
APP_NAME=spring-boot
CONFIG_FILE=$APP_HOME/application.properties
BOOT_ARGS="-Dspring.config.location=$CONFIG_FILE"
PID_FILE=$APP_HOME/$APP_NAME.pid
#如果系统中不存在java_home,手动指定java_home
if [ 0"$JAVA_HOME" = "0" ]; then
  JAVA_HOME=/usr/java/jdk1.8.0_211
fi
JAVA=$JAVA_HOME/bin/java

VM_ARGS="-Djasypt.encryptor.password="
JAVA_OPTS="$VM_ARGS -jar"
RETVAL=0
##################################

################################
# define function start
################################

createLockFile(){
  lock_dir=/var/lock/subsys
  lock_file_path=$lock_dir/$APP_NAME
  if [ -w $lock_dir ]
  then
    touch $lock_file_path
  fi
}

start(){
  [ -e $APP_HOME/logs ] || mkdir $APP_HOME/logs -p

  if [ -f $PID_FILE ]
  then 
    echo "$PID_FILE file exists, process already running,the pid file is $(cat $PID_FILE)"
  else
    createLockFile
	  CMD="$JAVA $JAVA_OPTS $APP_HOME/*.jar $BOOT_ARGS"
	  echo "$CMD >> $APP_HOME/logs/$APP_NAME.log"
    nohup $CMD >> $APP_HOME/logs/$APP_NAME.log 2>&1 &
    # $! 获取最后一个进程的id,先执行nohup命令,在执行 java命令,获取到的是java命令的pid
    RETVAL=$!
    echo $RETVAL >> $PID_FILE
    echo "server start OK,the PID = $RETVAL"
  fi  
}

stop(){
  if [ -f $PID_FILE ]
  then
    kill `cat $PID_FILE`
    rm -rf $PID_FILE
  else
    echo "$PID_FILE is not exists,process is not running"
  fi
}
################################
# define function stop
################################


##################################
# do action start
##################################
ACTION=$1
case $ACTION in
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
    echo "usage {start|stop|restart}"
  ;;
esac