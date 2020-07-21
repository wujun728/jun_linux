#!/bin/bash

wifi=hongfu

while :
do
  ping -c 5 www.baidu.com >/dev/null 2>&1
  if [ "$?" != "0" ]
  then
    echo "try again."
    sleep 3
    netctl stop $wifi >/dev/null 2>&1
    sleep 3
    netctl start $wifi >/dev/null 2>&1
  else
    echo "wifi is good, sleep a while."
    sleep 20
  fi
done
