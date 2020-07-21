#!/bin/bash

source /online/.bash_profile

echo "###################### 高拍仪主机关键进程监控 ##########################"

# 5,15,25,35,45,55 * * * * /online/shell/monitor.sh >> /online/shell/monitor.log

echo "检测日期：`date`"
echo "检测主机：`ifconfig bond0|grep "inet\>"|sed 's/^[ ]*//g'|awk '{print $2}'|sed 's/addr://g'`"

tom=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep tomcat|wc -l`

ng=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep nginx|wc -l`

rs=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep rsync|wc -l`


if [ $tom = "0" ];
then
    echo "警告！tomcat进程不存在！"
    while :;
    do
        echo "尝试启动tomcat..."
        sh /online/tomcat/bin/startup.sh
        tom=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep tomcat|wc -l`
        if [ $tom = "0" ];
        then
            echo "启动失败！5秒后将再次尝试启动tomcat..."
            sleep 5
            continue
        else
            echo "tomcat启动成功！"
            break
        fi
    done
else
    echo "tomcat进程正常"
fi


if [ $ng = "0" ];
then
    echo "警告！nginx进程不存在！"
    while :;
    do
        echo "尝试启动nginx..."
        /online/nginx/sbin/nginx
        ng=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep nginx|wc -l`
        if [ $ng = "0" ];
        then
            echo "启动失败！5秒后将再次尝试启动nginx..."
            sleep 5
            continue
        else
            echo "nginx启动成功！"
            break
        fi
    done
else
    echo "nginx进程正常"
fi

if [ $rs = "0" ];
then
    echo "警告！rsync进程不存在！"
    while :;
    do
        echo "尝试启动rsync..."
        rm -f /online/rsync_server/rsyncd.pid
        /bin/bash /online/rsync_server/start_rsync.sh &
        sleep 1

        rs=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep rs|wc -l`
        if [ $rs = "0" ];
        then
            echo "启动失败！5秒后将再次尝试启动rsync..."
            sleep 5
            continue
        else
            echo "rsync启动成功！"
            break
        fi
    done
else
    echo "rsync进程正常"
fi
echo "###################### 高拍仪主机关键进程监控 ##########################"

