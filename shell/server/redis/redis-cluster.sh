
#!/bin/sh
# chkconfig: 2345 80 90
#
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.
​
REDISPORT1=7001
REDISPORT2=7002
REDISPORT3=7003
REDISPORT4=7004
REDISPORT5=7005
REDISPORT6=7006

EXEC=/export/servers/redis-5.0.4/bin/redis-server
CLIEXEC=/export/servers/redis-5.0.4/bin/redis-cli
​
PIDFILE=/var/run/redis_${REDISPORT1}.pid
​
CONF1="/export/servers/redis-5.0.4/cluster/${REDISPORT1}/${REDISPORT1}.conf"
CONF2="/export/servers/redis-5.0.4/cluster/${REDISPORT2}/${REDISPORT2}.conf"
CONF3="/export/servers/redis-5.0.4/cluster/${REDISPORT3}/${REDISPORT3}.conf"
CONF4="/export/servers/redis-5.0.4/cluster/${REDISPORT4}/${REDISPORT4}.conf"
CONF5="/export/servers/redis-5.0.4/cluster/${REDISPORT5}/${REDISPORT5}.conf"
CONF6="/export/servers/redis-5.0.4/cluster/${REDISPORT6}/${REDISPORT6}.conf"
​
case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
                echo "$PIDFILE exists, process is already running or crashed"
        else
                echo "Starting Redis cluster server..."
                $EXEC $CONF1 &
                $EXEC $CONF2 &
                $EXEC $CONF3 &
                $EXEC $CONF4 &
                $EXEC $CONF5 &
                $EXEC $CONF6 &
                echo "启动成功..."
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
                echo "$PIDFILE does not exist, process is not running"
        else
                PID=$(cat $PIDFILE)
                echo "Stopping ..."
                $CLIEXEC -p $REDISPORT1 shutdown
                $CLIEXEC -p $REDISPORT2 shutdown
                $CLIEXEC -p $REDISPORT3 shutdown
                $CLIEXEC -p $REDISPORT4 shutdown
                $CLIEXEC -p $REDISPORT5 shutdown
                $CLIEXEC -p $REDISPORT6 shutdown
                while [ -x /proc/${PID} ]
                do
                    echo "Waiting for Redis cluster to shutdown ..."
                    sleep 1
                done
                echo "Redis cluster stopped"
        fi
        ;;
    *)
        echo "Please use start or stop as first argument"
        ;;
esac