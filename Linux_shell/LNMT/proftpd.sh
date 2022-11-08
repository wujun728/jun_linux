#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    printf "Error: You must be root to run this script!\n"
    exit 1
fi
clear
printf "=========================================================================\n"
printf "ProFTPd for LNMT V0.1  ,  Written by Xiao Dong \n"
printf "=========================================================================\n"
printf "LNMT is a tool to auto-compile & install Nginx + MySQL + Tomcat on Linux \n"
printf "This script is a tool to install ProFTPd for LNMT \n"
printf "\n"
printf "For more information please visit http://lnmt.org \n"
printf "\n"
printf "Usage: ./proftpd.sh \n"
printf "=========================================================================\n"
cur_dir=$(pwd)
files_dir=$cur_dir/files
script_dir=$cur_dir/script


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
	echo "Press any key to start install ProFTPd..."
	char=`get_char`

	
echo "============================Check files=================================="
if [ -d $files_dir ]; then
  echo "files folder [found]"
  else
  echo "Error: files folder not found!!!create it now......"
  mkdir $files_dir
fi
if [ -d $script_dir ]; then
  echo "files folder [found]"
  else
  echo "Error: files folder not found!!!create it now......"
  mkdir $script_dir
fi
cd $files_dir
if [ -s proftpd-1.3.4b.tar.gz ]; then
  echo "proftpd-1.3.4b.tar.gz [found]"
  else
  echo "Error: proftpd-1.3.4b.tar.gz not found!!!download now......"
  wget -c ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.4b.tar.gz
fi
cd $script_dir
if [ -s init.d.proftpd ]; then
  echo "ProFTPd service script [found]"
  else
  echo "Error: ProFTPd service script not found!!!download now......"
  wget -c http://lnmt.org/online/script/init.d.proftpd
fi
	

echo "Install building packages..."
cat /etc/issue | grep -Eqi '(Debian|Ubuntu)' && apt-get update;apt-get install build-essential gcc g++ make -y || yum -y install make gcc gcc-c++ gcc-g77

cd $files_dir
echo "Start download files..."
#wget -c ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.4b.tar.gz
tar zxf proftpd-1.3.4b.tar.gz
cd proftpd-1.3.4b
./configure --prefix=/usr/local/proftpd
make && make install
cd ../

ln -s /usr/local/proftpd/sbin/proftpd /usr/local/bin/
ln -s /usr/local/proftpd/bin/ftpasswd /usr/local/bin/

mkdir /usr/local/proftpd/var/log/
mkdir /usr/local/proftpd/etc/vhost/

cat >/usr/local/proftpd/etc/proftpd.conf<<EOF
# This is a basic ProFTPD configuration file (rename it to
# 'proftpd.conf' for actual use.  It establishes a single server
# and a single anonymous login.  It assumes that you have a user/group
# "nobody" and "ftp" for normal operation and anon.

ServerName                      "ProFTPD FTP Server for LNMT"
ServerType                      standalone
DefaultServer                   on

# Port 21 is the standard FTP port.
Port                            21

# Don't use IPv6 support by default.
UseIPv6                         off

# Umask 022 is a good standard umask to prevent new dirs and files
# from being group and world writable.
Umask                           022

# To prevent DoS attacks, set the maximum number of child processes
# to 30.  If you need to allow more than 30 concurrent connections
# at once, simply increase this value.  Note that this ONLY works
# in standalone mode, in inetd mode you should use an inetd server
# that allows you to limit maximum number of processes per service
# (such as xinetd).
MaxInstances                    30

# Set the user and group under which the server will run.
User                            nobody
Group                           nogroup

PassivePorts                    20000 30000
# To cause every FTP user to be "jailed" (chrooted) into their home
# directory, uncomment this line.


DefaultRoot ~

AllowOverwrite    on

AllowRetrieveRestart   on
AllowStoreRestart      on
UseReverseDNS off
IdentLookups off
#DisplayLogin welcome.msg
ServerIdent off
RequireValidShell off
AuthUserFile /usr/local/proftpd/etc/ftpd.passwd
AuthOrder mod_auth_file.c mod_auth_unix.c

# Normally, we want files to be overwriteable.
AllowOverwrite          on

# Bar use of SITE CHMOD by default
<Limit SITE_CHMOD>
  DenyAll
</Limit>
SystemLog     /usr/local/proftpd/var/log/proftpd.log
Include /usr/local/proftpd/etc/vhost/*.conf
EOF


cd $script_dir
#wget -c http://lnmt.org/online/script/init.d.proftpd
cp init.d.proftpd /etc/init.d/proftpd
chmod +x /etc/init.d/proftpd

cat /etc/issue | grep -Eqi '(Debian|Ubuntu)' && update-rc.d -f proftpd defaults;ln -s /usr/sbin/nologin /sbin/nologin || chkconfig --level 345 proftpd on

if [ -s /sbin/iptables ]; then
/sbin/iptables -I INPUT -p tcp --dport 21 -j ACCEPT
/sbin/iptables -I INPUT -p tcp --dport 20 -j ACCEPT
/sbin/iptables -I INPUT -p tcp --dport 20000:30000 -j ACCEPT
/sbin/iptables-save
fi

cd $cur_dir
cp proftpd_vhost.sh /root/proftpd_vhost.sh

clear
printf "=======================================================================\n"
printf "Starting ProFTPd...\n"
/etc/init.d/proftpd start
printf "=======================================================================\n"
printf "Install ProFTPd completed, enjoy it!\n"
printf "=======================================================================\n"
printf "Install ProFTPd for LNMT V0.1  ,  Written by Xiao Dong \n"
printf "=======================================================================\n"
printf "LNMT is a tool to auto-compile & install Nginx + MySQL + Tomcat on Linux \n"
printf "This script is a tool to install ProFTPd for lnmt \n"
printf "\n"
printf "For more information please visit http://lnmt.org \n"
printf "=======================================================================\n"
