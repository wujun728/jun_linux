#!/bin/sh
NGINX_CMD="/opt/local/nginx/sbin/nginx"
NGINX_CONF="/opt/local/nginx/conf/nginx.conf"
RETVAL=0
start() {
   echo "Starting NGINX Web Server: \c"
   $NGINX_CMD -c $NGINX_CONF &
   RETVAL=$?
   [ $RETVAL -eq 0 ] && echo "ok" || echo "failed"
   return $RETVAL
}
stop() {
   echo "Stopping NGINX Web Server: \c"
   NGINX_PID=`ps -ef |grep $NGINX_CMD |grep -v grep |awk '{print $2}'`
   kill $NGINX_PID
   RETVAL=$?
   [ $RETVAL -eq 0 ] && echo "ok" || echo "failed"
   return $RETVAL
}
case "$1" in
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
      echo "Usage: $0 {start|stop|restart}"
      exit 1
esac
exit $RETVAL