#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, use sudo sh $0"
    exit 1
fi

clear
echo "========================================================================="
echo "Add ProFTPd Virtual Host for LNMT v0.1 ,  Written by Xiao Dong "
echo "========================================================================="
echo "LNMT is a tool to auto-compile & install Nginx + MySQL + Tomcat on Linux "
echo "This script is a tool to add virtual host for ProFTPd "
echo "For more information please visit http://lnmt.org/"
echo ""
echo "========================================================================="

	username=""
	read -p "Please input a username:" username
	if [ "$username" = "" ]; then
		echo "UserName can't be NULL!"
		sleep 2
		exit 1
	fi
	
	if cat /etc/passwd | awk -F : '{print $1}' | grep $username >/dev/null 2>&1
	then
		echo "User: $username is exist!"
		echo "Please rerun this script,input a new username!"
		sleep 5
		exit 1
	else
		echo "User $username will add to your system."
	fi
	
	userpass=""
	echo "Please set password for $username:"
	read userpass

	if [ "$userpass" == "" ]; then

	  echo "Password can't be NULL!"
	  sleep 2
	  exit 1
	else
		echo "Password: $userpass"
	fi

	userdir=""
	echo "Please set the directory of $username"
	read -p "Please input full path:" userdir

	if [ "$userdir" == "" ]; then

	  echo "Directory can't be NULL!"
	  sleep 2
	  exit 1
	else
		echo "Directory: $userdir"
	fi


	get_char()
	{
	SAVEDSTTY=`stty -g`
	stty -echo
	stty cbreak
	dd if=/dev/tty bs=1 count=1 2> /dev/null
	stty -raw
	stty echo
	stty $SAVEDSTTY
	}
	echo ""
	echo "Press any key to start create ProFTPd virtul host..."
	char=`get_char`


if [ ! -d /usr/local/proftpd/etc/vhost ]; then
	mkdir /usr/local/proftpd/etc/vhost
fi

if [ ! -d $userdir ]; then
	echo "Create Virtul Host directory......"
	mkdir $userdir
fi

useradd -s /sbin/nologin -d $userdir -c "lnmt proftpd user" $username
cat >/tmp/$user.passwd<<eof
$username:$userpass
eof

chpasswd < /tmp/$user.passwd

cat >/usr/local/proftpd/etc/vhost/$username.conf<<eof
<Directory $userdir>
     <Limit ALL>
          AllowUser $username
     </Limit>
</Directory>
eof

echo "Restart ProFTPd......"
/etc/init.d/proftpd stop
/etc/init.d/proftpd start

echo "========================================================================="
echo "Add ProFTPd Virtual Host for LNMT v0.1 ,  Written by Xiao Dong "
echo "========================================================================="
echo "For more information please visit http://lnmt.org/"
echo ""
echo "Your UserName:$username"
echo "Your Password:$userpass"
echo "Directory of $username:$userdir"
echo ""
echo "========================================================================="