#!/bin/bash
#
# For RedHat (thanks to Sudhaker Raj):
# chkconfig: 345 95 05
# description: Starts and stops the XAMPP \
#              used to control Apache, MySQL, ProFTPD.
# For SuSE:
### BEGIN INIT INFO
# Provides:                     apache2 httpd2 xampp
# Required-Start:               $local_fs $remote_fs $network
# Required-Stop:                $local_fs $remote_fs $network
# Default-Start:                3 5
# Default-Stop:                 0 1 2 6
# Short-Description:            XAMPP
# Description:                  Starts and stops XAMPP
### END INIT INFO
###############################################################################
# Copyright 2002-2009 by Apache Friends, GPL-licensed
# Authors:
#   - Kai 'Oswald' Seidler, oswald@apachefriends.org
#   - Kristian W. Marcroft, kris@apachefriends.org 
#   - Christian Speich, kleinweby@apachefriends.org

osguess() {
	if test -f /etc/redhat-release
	then
		if egrep "9 " /etc/redhat-release > /dev/null
		then
			echo "rh9"
			return 0
		else
		        echo "linux"
			return 0
		fi
	elif test "$(uname)" = "Darwin"
	then
		echo "macosx"
		return 0
	else
		if test -f /etc/vfstab
		then
			echo "solaris"
			return 0
		else
			echo "linux"
			return 0
		fi
	fi
}

case $(osguess) in
	solaris)
		XAMPP_OS="Solaris"
		XAMPP_ROOT="/opt/xampp"
		;;
	linux|rh9)
		XAMPP_OS="Linux"
		XAMPP_ROOT="/opt/lampp"
		;;
	macosx)
		XAMPP_OS="Mac OS X"
		XAMPP_ROOT="/Applications/XAMPP/xamppfiles"
		;;
esac

export XAMPP_OS
export XAMPP_ROOT

. $XAMPP_ROOT/share/xampp/xampplib

version=$(cat $XAMPP_ROOT/lib/VERSION)
bon=""
boff=""
lc="$XAMPP_ROOT/etc/xampp"
de="false"
case $LANG in
        de*) de="true";;
esac
export de

function startApache() {
	apachedefines=""
	ssl=0
	php=0
	
	if test -f $lc/startssl
	then
		ssl=1
		apachedefines="$apachedefines -DSSL"
	fi
	
	if true
	then
		php=1
		apachedefines="$apachedefines -DPHP"
	fi
	
	printf "XAMPP: $($GETTEXT 'Starting %s...')" "Apache"
	
	if testrun "$XAMPP_ROOT/logs/httpd.pid" httpd
	then
		$GETTEXT -s "already running."
		return 0
	fi
	
	if testport 80
	then
		$GETTEXT -s "fail."
		echo "XAMPP: " $($GETTEXT 'Another web server is already running.')
		return 1
	fi
	
	if test $ssl -eq 1 && testport 443
	then
		$GETTEXT -s "fail."
		echo "XAMPP: " $($GETTEXT 'Another web server with SSL is already running.')
		return 1
	fi
	
	syntaxCheckMessage=$($XAMPP_ROOT/bin/httpd -t $apachedefines 2>&1)
	
	if test $? -ne 0
	then
		$GETTEXT -s "fail."
		echo "$syntaxCheckMessage"
		return 1
	fi
	
	"$XAMPP_ROOT/bin/apachectl" -k start -E "$XAMPP_ROOT/logs/error_log" $apachedefines > /dev/null 2>&1 
	
	if test $? -ne 0
	then
		$GETTEXT -s "fail."
		
		## TODO: run the diagnose script
		
		$XAMPP_ROOT/share/xampp/diagnose
		
		return $?
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function startMySQL() {
	
	printf "XAMPP: $($GETTEXT 'Starting %s...')" "MySQL"

	if testrun "$XAMPP_ROOT/var/mysql/$(hostname).pid" mysqld
	then
		$GETTEXT -s "already running."
		return 0
	fi
	
	if testport 3308
	then
		$GETTEXT -s "fail."
		echo "XAMPP: " $($GETTEXT 'Another MySQL daemon is already running.')
		return 1
	fi
	
	$XAMPP_ROOT/bin/mysql.server start > /dev/null &
	
	if test $? -ne 0
	then
		$GETTEXT -s "fail."
				
		printf "$($GETTEXT -s 'Last 10 lines of \"%s\":')\n" "$XAMPP_ROOT/var/mysql/$(hostname).err"
		
		tail -n 10 "$XAMPP_ROOT/var/mysql/$(hostname).err"
		
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function startProFTPD() {
	
	printf "XAMPP: $($GETTEXT 'Starting %s...')" "ProFTPD"

	if testrun "$XAMPP_ROOT/var/proftpd.pid" proftpd
	then
		$GETTEXT -s "already running."
		return 0
	fi
	
	if testport 21
	then
		$GETTEXT -s "fail."
		echo "XAMPP: " $($GETTEXT 'Another FTP daemon is already running.')
		return 1
	fi
	
	$XAMPP_ROOT/sbin/proftpd > $XAMPP_ROOT/var/proftpd/start.err 2>&1
	
	if test $? -ne 0
	then
		$GETTEXT -s "fail."
				
		printf "$($GETTEXT -s 'Contents of \"%s\":')\n" "$XAMPP_ROOT/var/proftpd/start.err"
		
		cat "$XAMPP_ROOT/var/proftpd/start.err"
		
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function startWebmin() {
	
	printf "XAMPP: $($GETTEXT 'Starting %s...')" "Webmin"

	if testrun "$XAMPP_ROOT/var/webmin/miniserv.pid" miniserv
	then
		$GETTEXT -s "already running."
		return 0
	fi
	
	$XAMPP_ROOT/etc/webmin/start quiet 2>&1
	
	if test $? -ne 0
	then
		$GETTEXT -s "fail."
		
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function stopApache() {
	
	printf "XAMPP: $($GETTEXT 'Stopping %s...')" "Apache"
	
	if ! test -f "$XAMPP_ROOT/logs/httpd.pid"
	then
		$GETTEXT -s "not running."
		return 0
	fi
	
        if test -f $lc/startssl
	then
	    ssl=1
	    apachedefines="$apachedefines -DSSL"
	fi
	
	if true
	then
	    php=1
	    apachedefines="$apachedefines -DPHP"
	fi

	$XAMPP_ROOT/bin/apachectl -k stop $apachedefines > /dev/null 2>&1
	
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "apachectl returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function stopMySQL() {
	
	printf "XAMPP: $($GETTEXT 'Stopping %s...')" "MySQL"
	
	if ! test -f "$XAMPP_ROOT/var/mysql/$(hostname).pid"
	then
		$GETTEXT -s "not running."
		return 0
	fi
	
	$XAMPP_ROOT/bin/mysql.server stop > /dev/null 2>&1
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "mysql.server returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function stopProFTPD() {
	
	printf "XAMPP: $($GETTEXT 'Stopping %s...')" "ProFTPD"
	
	if ! test -f "$XAMPP_ROOT/var/proftpd.pid"
	then
		$GETTEXT -s "not running."
		return 0
	fi
	
	kill $(cat $XAMPP_ROOT/var/proftpd.pid)
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "kill returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function stopWebmin() {
	
	printf "XAMPP: $($GETTEXT 'Stopping %s...')" "Webmin"
	
	if ! test -f "$XAMPP_ROOT/var/webmin/miniserv.pid"
	then
		$GETTEXT -s "not running."
		return 0
	fi
	
	$XAMPP_ROOT/etc/webmin/stop quiet
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "stop returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function reloadApache() {
	
	printf "XAMPP: $($GETTEXT 'Reload %s...')" "Apache"
	
	if ! test -f "$XAMPP_ROOT/logs/httpd.pid"
	then
		$GETTEXT -s "not running."
		return 1
	fi
	
	kill -USR1 $(cat "$XAMPP_ROOT/logs/httpd.pid")
	
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "kill returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function reloadMySQL() {
	
	printf "XAMPP: $($GETTEXT 'Reload %s...')" "MySQL"
	
	if ! test -f "$XAMPP_ROOT/var/mysql/$(hostname).pid"
	then
		$GETTEXT -s "not running."
		return 1
	fi
	
	kill -HUP $(cat "$XAMPP_ROOT/var/mysql/$(hostname).pid")
	
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "kill returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

function reloadProFTPD() {
	
	printf "XAMPP: $($GETTEXT 'Reload %s...')" "ProFTPD"
	if ! test -f "$XAMPP_ROOT/var/proftpd.pid"
	then
		$GETTEXT -s "not running."
		return 1
	fi
	kill -HUP $(cat "$XAMPP_ROOT/var/proftpd.pid")
		
	error=$?
	
	if test $error -ne 0
	then
		$GETTEXT -s "fail."
		echo "kill returned $error."	
		return 1
	fi
	
	$GETTEXT -s "ok."
	return 0
}

# XAMPP is currently 32 bit only
case `uname -m` in
	*_64)
	if $XAMPP_ROOT/bin/php -v > /dev/null 2>&1
	then
		:
	else
		$GETTEXT -s "XAMPP is currently only availably as 32 bit application. Please use a 32 bit compatibility library for your system."
		exit 1
	fi
	;;
esac

# do we have that new red hat linux 9 with posix native threads?
if test $(osguess) = "rh9"
then
	# for now disable PNTL. if PNTL gets more popular we will support it. - oswald [8apr3]
	export LD_ASSUME_KERNEL=2.2.5
	#echo "XAMPP: DISABLE PNTL..."
fi

LIBRARY_PATH="$XAMPP_ROOT/lib"
# Do we use Oracle? If yes, add Oracle's lib directory to LD_LIBRARY_PATH - oswald [6jul5]
if test -f $XAMPP_ROOT/etc/xampp/oraclelib
then
    export LIBRARY_PATH="$(cat $XAMPP_ROOT/etc/xampp/oraclelib):$LIBRARY_PATH"
fi

if test "$(osguess)" = "macosx"
then
    # Thanks to drosenbe! - oswald [3sep10]
    if test -z $DYLD_LIBRARY_PATH
    then
	export DYLD_LIBRARY_PATH="$LIBRARY_PATH"
    else
	export DYLD_LIBRARY_PATH="$LIBRARY_PATH:$DYLD_LIBRARY_PATH"
    fi
else
    # Thanks to drosenbe! - oswald [3sep10]
    if test -z $LD_LIBRARY_PATH
    then
	export LD_LIBRARY_PATH="$LIBRARY_PATH"
    else
	export LD_LIBRARY_PATH="$LIBRARY_PATH:$LD_LIBRARY_PATH"
    fi
fi

iswebmin="false";
if test -d $XAMPP_ROOT/webmin
then
	iswebmin="true";
fi

# Hack to let XAMPP run with SELinux (for Fedora)
if test "$(osguess)" = "linux"; then
	 $XAMPP_ROOT/share/xampp/selinux
fi

if test "$(osguess)" = "macosx" && ! test -f "$lc/rights_fixed" && test $(id -u) -eq 0
then
	$GETTEXT -s -n "File permissions are being checked..."
	$XAMPP_ROOT/bin/fix_rights
	if test $? -eq 0
	then
		$GETTEXT -s "ok."
	else
		$GETTEXT -s "fail"
	fi
fi

case $1 in
	"start")
		printf "$($GETTEXT 'Starting XAMPP for %s %s...')\n" "$XAMPP_OS" "$version"

		checkRoot
		
		error=0
		
		startApache || error=1
		startMySQL || error=1
		if test -f $lc/startftp
		then
			startProFTPD || error=1
		fi
		if $iswebmin && test -f $lc/startwebmin
		then
			startWebmin || error=1
		fi
		
		exit $error
		;;

	"reload")
		printf "$($GETTEXT 'Reload XAMPP for %s %s...')\n" "$XAMPP_OS" "$version"
		
		checkRoot
		
		error=0
		reloadApache || error=1
		reloadMySQL || error=1
		reloadProFTPD || error=1
		exit $error
		;;
		
	"enablessl")
		checkRoot
		
		echo -n "XAMPP: " $($GETTEXT 'XAMPP: Enable SSL...')
		
		if test -f "$lc/startssl"
		then
			$GETTEXT -s "already enabled."
			exit 0
		fi
		
		errmsg=$(touch "$lc/startssl" 2>&1)
		
		if test $? -ne 0
		then
			$GETTEXT -s "fail."
			echo $errmsg
			exit 1
		fi
		
		$GETTEXT -s "ok."
		
		if ($XAMPP_ROOT/share/xampp/statusraw | grep -q "APACHE RUNNING")
		then
			$0 restartapache
			exit $?
		fi
		
		exit 0
		
		;;
	
	"disablessl")
		checkRoot
		
		echo -n "XAMPP: " $($GETTEXT 'Disable SSL...')
		
		if ! test -f "$lc/startssl"
		then
			$GETTEXT -s "already disabled."
			exit 0
		fi
		
		errmsg=$(rm "$lc/startssl" 2>&1)
		
		if test $? -ne 0
		then
			$GETTEXT -s "fail."
			echo $errmsg
			exit 1
		fi
		
		$GETTEXT -s "ok."
		
		if ($XAMPP_ROOT/share/xampp/statusraw | grep -q "APACHE RUNNING")
		then
			$0 restartapache
			exit $?
		fi
		
		exit 0
		
		;;

	"startapache")
	
		checkRoot
	
		startApache
		exit $?
		;;

	"startmysql")
	
		checkRoot
	
		startMySQL
		exit $?
		;;
		
	"startwebmin")
		if ! $iswebmin
		then
			echo "XAMPP: " $($GETTEXT -s "Webmin isn't installed.")
			exit 1
		fi
		
		checkRoot
		
		if test "$2" != "%"
		then
			touch $lc/startwebmin
		fi

		startWebmin
		exit $?
		;;

	"startftp")
	
		checkRoot
	
		if test "$2" != "%"
		then
			touch $lc/startftp
		fi
		if test -f $lc/startftp
		then
			startProFTPD
		fi
		;;

	"stop")
		printf "$($GETTEXT 'Stopping XAMPP for %s %s...')\n" "$XAMPP_OS" "$version"

		checkRoot

		error=0

		stopApache || error=1
		stopMySQL || error=1
		if test -f $lc/startftp
		then
			stopProFTPD || error=1
		fi
		if $iswebmin && test -f $lc/startwebmin
		then
			stopWebmin || error=1
		fi

		exit $?
		;;

	"stopapache")
		checkRoot
		
		stopApache
		exit $?
		;;

	"reloadapache")
		checkRoot
		
		reloadApache
		exit $?
		;;

	"stopmysql")
		stopMySQL
		exit $?
		;;
		
	"stopwebmin")
		if ! $iswebmin
		then
			echo "XAMPP: " $($GETTEXT "Webmin isn't installed.")
			exit 1
		fi
		
		checkRoot
		
		if test "$2" != "%"
		then
			rm $lc/startwebmin
		fi
			
		stopWebmin
		exit $?
		;;

	"reloadmysql")
	
		checkRoot
	
		reloadMySQL
		exit $?
		;;


	"stopftp")
		checkRoot
	
		if test "$2" != "%"
		then
			rm $lc/startftp 2> /dev/null
		fi
		stopProFTPD
		exit $?
		;;

	"reloadftp")
		checkRoot
	
		reloadProFTPD
		exit $?
		;;

	"wizard")
		checkRoot
	
		$XAMPP_ROOT/bin/php $XAMPP_ROOT/share/xampp/wizard.php
		;;

	"restartapache")
		checkRoot
		
		stopApache
		sleep 1
		startApache
		exit $?
		;;

	"restart")
		printf "$($GETTEXT 'Restarting XAMPP for %s %s...')\n" "$XAMPP_OS" "$version"
		
		checkRoot
		
		stopApache
		stopMySQL
		if test -f $lc/startftp
		then
			stopProFTPD
		fi
		if $iswebmin && test -f $lc/startwebmin
		then
			stopWebmin
		fi
		
		sleep 1
		error=0
		
		startApache || error=1
		startMySQL || error=1
		if test -f $lc/startftp
		then
			startProFTPD || error=1
		fi
		if $iswebmin && test -f $lc/startwebmin
		then
			startWebmin || error=1
		fi
		exit $?
		;;

	"security")
		checkRoot
	
		$XAMPP_ROOT/share/xampp/checkall
		;;
	"oci8")
                checkRoot

		$XAMPP_ROOT/share/xampp/oci8install
		;;
	"backup")
		checkRoot
		
		$XAMPP_ROOT/share/xampp/backup $2
		;;
		
	"status")
		$XAMPP_ROOT/share/xampp/status
		;;

	"statusraw")
		$XAMPP_ROOT/share/xampp/statusraw
		;;

#	"php4")
#		$XAMPP_ROOT/share/xampp/activatephp @PHP4_VERSION@
#		;;
#
#	"php5")
#	        $XAMPP_ROOT/share/xampp/activatephp 5.4.16
#	 	;;

        "phpstatus")
		$XAMPP_ROOT/share/xampp/phpstatus
		;;
	
	start*|stop*|reload*|status*|restart*)
		checkRoot
		
		$XAMPP_ROOT/share/xampp/addons $*
		;;

	"version")
		printf "$($GETTEXT 'Version: XAMPP for %s %s')\n" "$XAMPP_OS" "$version"
		;;

	"fix_rights")
		checkRoot
		
		echo -n "XAMPP: " $($GETTEXT 'File permissions are being checked...')
		$XAMPP_ROOT/bin/fix_rights
		error=$?
		if test $error -eq 0
		then
			$GETTEXT -s "ok."
		else
			$GETTEXT -s "fail."
		fi
		exit $error
		;;

	*)	
		printf "$($GETTEXT 'Usage: %s <action>')\n" "$(basename $0)"
		echo ""
		echo "	start        " $($GETTEXT "Start XAMPP (Apache, MySQL and eventually others)")
		echo "	startapache  " $($GETTEXT "Start only Apache")
		echo "	startmysql   " $($GETTEXT "Start only MySQL")
		echo "	startftp     " $($GETTEXT "Start only ProFTPD")
		$iswebmin && echo "	startwebmin  " $($GETTEXT "Start only Webmin")
		echo ""
		echo "	stop         " $($GETTEXT "Stop XAMPP (Apache, MySQL and eventually others)")
		echo "	stopapache   " $($GETTEXT "Stop only Apache")
		echo "	stopmysql    " $($GETTEXT "Stop only MySQL")
		echo "	stopftp      " $($GETTEXT "Stop only ProFTPD")
		$iswebmin && echo "	stopwebmin   " $($GETTEXT "Stop only Webmin")
		echo ""
		echo "	reload       " $($GETTEXT "Reload XAMPP (Apache, MySQL and eventually others)")
		echo "	reloadapache " $($GETTEXT "Reload only Apache")
		echo "	reloadmysql  " $($GETTEXT "Reload only MySQL")
		echo "	reloadftp    " $($GETTEXT "Reload only ProFTPD")
		echo ""
		echo "	restart      " $($GETTEXT "Stop and start XAMPP")
		echo "	security     " $($GETTEXT "Check XAMPP's security")
		echo ""
		echo "	enablessl    " $($GETTEXT "Enable SSL support for Apache")
		echo "	disablessl   " $($GETTEXT "Disable SSL support for Apache")
		echo ""
		echo "	backup       " $($GETTEXT "Make backup file of your XAMPP config, log and data files")
		echo ""
                echo "	oci8         " $($GETTEXT "Enable the oci8 extenssion")
                echo ""
		if test $(osguess) = "linux" || test $(osguess) = "rh9"
		then
			echo "	panel        " $($GETTEXT "Starts graphical XAMPP control panel")
		fi
		if test $(osguess) = "macosx"
		then
			echo "	fix_rights   " $($GETTEXT "Resets file permissions.")
		fi
		echo ""
		;;
esac