#!/bin/bash

backup_pid_string=`tail -1 backup.log`
if [ -z "$backup_pid_string" ]; then
	echo "xtrabackup pid not found, xtrabackup will not restart."
else
	backup_pid=${backup_pid_string#*:}
	echo "old pid is "$backup_pid
	echo "restarting xtrabackup..."
	kill -9 $backup_pid && ./runBackup.sh & >> backup.log
	echo "xtrabackup restarted."
fi