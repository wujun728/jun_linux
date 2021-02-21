#!/usr/bin/env bash
# filename: bind_addr.sh
# docker默认使用’bridge’来设置container的网络模式（即从与docker0同网段的未使用的IP中取一个作为container的IP），我们这里使用’none‘来实现自己手动配置container的网络。

if [ `id -u` -ne 0 ];then
    echo '必须使用root权限'
    exit
fi

if [ $# != 2 ]; then
    echo "使用方法: $0 容器名字 IP"
    exit 1
fi

container_name=$1
bind_ip=$2

container_id=`docker inspect -f '{{.Id}}' $container_name 2> /dev/null`
if [ ! $container_id ];then
    echo "容器不存在"
    exit 2
fi
bind_ip=`echo $bind_ip | egrep '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'`
if [ ! $bind_ip ];then
    echo "IP地址格式不正确"
    exit 3
fi

container_minid=`echo $container_id | cut -c 1-10`
container_netmask=`ip addr show docker0 | grep "inet\b" | awk '{print $2}' | cut -d / -f2`
container_gw=`ip addr show docker0 | grep "inet\b" | awk '{print $2}' | cut -d / -f1`

bridge_name="veth_$container_minid"
container_ip=$bind_ip/$container_netmask
pid=`docker inspect -f '{{.State.Pid}}' salt-master 2> /dev/null`
if [ ! $pid ];then
    echo "获取容器$container_name的id失败"
    exit 4
fi

if [ ! -d /var/run/netns ];then
    mkdir -p /var/run/netns
fi

ln -sf /proc/$pid/ns/net /var/run/netns/$pid

ip link add $bridge_name type veth peer name X
brctl addif docker0 $bridge_name
ip link set $bridge_name up
ip link set X netns $pid
ip netns exec $pid ip link set dev X name eth0
ip netns exec $pid ip link set eth0 up
ip netns exec $pid ip addr add $container_ip dev eth0
ip netns exec $pid ip route add default via $container_gw