#!/bin/bash
# chkconfig:35 85 15
# description:ngixn
# nginx单机版启动脚本
# nginx 会自动创建PID_FILE
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
PRG=`basename $PRG`
################################
# get app_home end
#############################


##########################
# custom variables start
###########################
nginx_config=$APP_HOME/conf/nginx.conf
EXEC=$APP_HOME/sbin/nginx
#nginx自动创建的pid文件路径
#PID_FILE=$APP_HOME/logs/nginx.pid
PID_FILE=/var/run/nginx.pid
lock_dir=/var/lock/subsys/
lock_file=/var/lock/subsys/$PRG

###########################
# custom variables end
###########################

########### source libiary start #################
. /etc/rc.d/init.d/functions
. /etc/sysconfig/network
########### source libiary end ################

##########################
# define funcation start
##########################

#是否有可执行权限,如果没有退出
[ -x $EXEC ] || exit 0
start(){
    if [ -e $PID_FILE ];then
        echo "$PRG already running...."
    else
        echo $"Starting $PRG: "
        #使用daemon启动ngxin,使用-c指定配置文件
        $EXEC -c ${nginx_config}

        if [ $? = 0 ];then
			touch $lock_file;
			echo "successed"
		else
		    echo
			echo "failed"
		fi
    fi
}

stop(){
	if [ -e $PID_FILE ];then
		echo -n "Stopping $PRG:"
		$EXEC -s stop
		if [ $? = 0 ];then
			rm -f $lock_file
			echo "successed"
		else
		    echo
			echo "failed"
		fi
	else
		echo "nginx not start"
	fi
}

restart(){
    stop
    sleep 1
    start
}

reload () {
	if [ -e $PID_FILE ];then
		#重启程序
		$EXEC -s reload
		echo "Reloading $PROG"

		if [ $? = 0 ]; then
		    echo_success
		else
		    echo_failure
		fi
	else
		echo "$PRG not start"
	fi
}

status(){
    netstat -tnlp|grep nginx
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
    reload)
        reload
        ;;
    status)
        status
        ;;
    *)
        echo usage "{start|stop|restart||status}"
    ;;
esac