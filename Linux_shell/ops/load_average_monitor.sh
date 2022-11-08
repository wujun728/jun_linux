#!/bin/sh
#*************************************************************************
#desc:	平均负载监控，如果负载一直大于或接近逻辑CPU的个数(这里如果平均负载在90%以上)则说明CPU很繁忙，负载很高
#		服务器性能低下，这个时候要通过vmstat查看并考虑优化或增大服务器性能
#author:beginman
#*************************************************************************
physical_cpu=`cat /proc/cpuinfo | grep "physical id"|sort|wc -l`
load_average_15min=`uptime | awk "{print $12}"`
let "value=load_average_15min/physical_cpu"
if [ $(echo "$value>=0.9"|bc) = 1 ]; then
	echo "CPU负载超过90%."
	mutt -s "CPU负载报警" 1373763906@qq.com `uptime`
fi

