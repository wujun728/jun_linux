#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, use sudo sh $0"
    exit 1
fi

clear
echo "========================================================================="
echo "Uninstall LNMT,  Written by Xiao Dong"
echo "========================================================================="
echo "A tool to auto-compile & install Nginx + MySQL + Tomcat on Linux "
echo ""
echo "For more information please visit http://lnmt.org/"
echo ""
echo 'Please backup your mysql data and configure files first!!!!!'
echo ""
echo "========================================================================="
shopt -s extglob
if [ -s /usr/local/mariadb/bin/mysql ]; then
	ismysql="no"
else
	ismysql="yes"
fi

echo ""
	uninstall="y"
	echo "INPUT y to uninstall LNMT, n to exit"
	read -p "(Please input y or n):" uninstall

	case "$uninstall" in
	y|Y|Yes|YES|yes|yES|yEs|YeS|yeS)
	echo "You will uninstall LNMT"
	echo -e "\033[31mPlease backup your configure files and mysql data!!!!!!\033[0m"
	echo 'The following directory or files will be remove!'
	cat << EOF
/usr/local/nginx
/usr/local/mysql
/etc/my.cnf
/root/vhost.sh
/root/lnmt
/root/run.sh
/etc/init.d/nginx
/etc/init.d/mysql
EOF
	;;
	n|N|No|NO|no|nO)
	echo "Bye."
	exit 0
	esac

	echo -e "\033[31mPlease backup your configure files and mysql data!!!!!!\033[0m"

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
	echo "Press any key to start uninstall or Press Ctrl+c to cancel"
	char=`get_char`

function uninstall_lnmt
{
	/etc/init.d/nginx stop
	if [ "$ismysql" = "no" ]; then
		/etc/init.d/mariadb stop
	else
		/etc/init.d/mysql stop
	fi
	
	rm -rf /usr/local/nginx
	if [ "$ismysql" = "no" ]; then
		rm -rf /usr/local/mariadb/!(var|data)
	else
		rm -rf /usr/local/mysql/!(var|data)
	fi

	rm -f /etc/my.cnf
	rm -f /root/vhost.sh
	rm -f /root/lnmt
	rm -f /root/run.sh
	rm -f /etc/init.d/nginx
	if [ "$ismysql" = "no" ]; then
		rm -f /etc/init.d/mariadb
	else
		rm -f /etc/init.d/mysql
	fi
	echo "LNMT Uninstall completed."
}

uninstall_lnmt

echo "========================================================================="
echo "Uninstall LNMT,  Written by Xiao Dong"
echo "========================================================================="
echo "A tool to auto-compile & install Nginx + MySQL + Tomcat on Linux "
echo ""
echo "For more information please visit http://lnmt.org/"
echo ""
echo "========================================================================="