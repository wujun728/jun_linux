#!/bin/bash


if [ "$#" != "1" ];then
	echo "使用方法: $0 ip_address"
	exit 1
fi

cd ~/work/vpn/config
sudo openvpn sitechVPN.ovpn &

while :;
do
	if [ `ifconfig|grep tun0|wc -l` != "0" ]; then
		echo "VPN连接成功"
		break;
	else
		echo "等待VPN连接..."
		sleep 1
	fi
done

sudo route add -net 130.89.200.0 netmask 255.255.255.0 dev tun0

rdesktop -g 1024x768 -P -z -r sound:off -u Administrator $1:3389
