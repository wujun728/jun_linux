#!/bin/bash
#*************************************************************************
#desc:磁盘监控脚本
#author:beginman
#每两小时执行一次
#0 */2 * * * /bin/sh /home/team/shells/disk_mintor.sh  
#*************************************************************************

diskinfo="/tmp/diskinfo.txt"

for d in `df -P | grep /dev | awk '{print $5}'| sed 's/%//g'`
do
	if [ $d -gt 90 ];then
		df -h>>$diskinfo;
		#sendmail
		mutt -s "disk warining!" "1373763906@qq.com" <${diskinfo} -a ${diskinfo}
		exit 0;
	fi
done
	

