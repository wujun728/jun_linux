#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install LNMT"
    exit 1
fi

clear
echo "========================================================================="
echo "LNMT V0.1 for CentOS/RedHat Linux Server, Written by Xiao Dong"
echo "========================================================================="
echo "A tool to auto-compile & install Nginx + MySQL + JRE + Tomcat on Linux "
echo ""
echo "For more information please visit http://lnmt.org/"
echo "========================================================================="
cur_dir=$(pwd)
files_dir=$cur_dir/files
conf_dir=$cur_dir/conf
script_dir=$cur_dir/script
sys_bit=$(getconf LONG_BIT)
#soft version default value
pcre_version="8.12"
nginx_version="1.7.9"
mysql_version="5.5.37"
jre_version="7u75"
jre_tar_dir="jre1.7.0_75"
tomcat_version="7.0.57"


#set mysql root password
echo "========================================"

mysql_root_pwd="root"
echo "Please input the root password of mysql:"
read -p "(Default password: root):" mysql_root_pwd
if [ "$mysql_root_pwd" = "" ]; then
	mysql_root_pwd="root"
fi
echo "==========================="
echo "MySQL root password:$mysql_root_pwd"
echo "==========================="

#do you want to install the InnoDB Storage Engine?
echo "================================================"

install_innodb="n"
echo "Do you want to install the InnoDB Storage Engine?"
read -p "(Default no,if you want please input: y ,if not please press the enter button):" install_innodb

case "$install_innodb" in
y|Y|Yes|YES|yes|yES|yEs|YeS|yeS)
echo "You will install the InnoDB Storage Engine"
install_innodb="y"
;;
n|N|No|NO|no|nO)
echo "You will NOT install the InnoDB Storage Engine!"
install_innodb="n"
;;
*)
echo "INPUT error,The InnoDB Storage Engine will NOT install!"
install_innodb="n"
esac
	
#which MySQL version do you want to install?
echo "==========================================="
echo "which MySQL version do you want to install?"

is_install_mysql55="y"
echo "Install MySQL 5.5.37,Please input y or press Enter"
echo "Install MariaDB 5.5.37,Please input md"
read -p "(Please input y , n or md):" is_install_mysql55

case "$is_install_mysql55" in
y|Y|Yes|YES|yes|yES|yEs|YeS|yeS)
echo "You will install MySQL 5.5.37"
is_install_mysql55="y"
mysql_version="5.5.37"
;;
md|MD|Md|mD)
echo "You will install MariaDB 5.5.37"
is_install_mysql55="md"
mysql_version="5.5.37"
;;
*)
echo "INPUT error,You will install MySQL 5.5.37"
is_install_mysql55="y"
mysql_version="5.5.37"
esac

#Get system bit version
case "$sys_bit" in
64)
sys_bit="x64"
;;
32)
sys_bit="x86"
;;
*)
echo "We don't know your system bit version,We think it's about x86 bit system"
sys_bit="x86"
esac

#which JRE version do you want to install?
echo "========================================="
echo "which JRE version do you want to install?"
echo "Install JRE 1.7,Please input 7 or press Enter"
echo "Install JRE 1.8,Please input 8"
read -p "(Please input 7 or 8):" jre_version

case "$jre_version" in
7)
echo "You will install JRE 1.7(7u75_$sys_bit)"
jre_version="7u75"
;;
8)
echo "You will install JRE 1.8(8u31_$sys_bit)"
jre_version="8u31"
;;
*)
echo "INPUT error,You will install JRE 1.7(7u75_$sys_bit)"
jre_version="7u75"
esac

#which Apache Tomcat version do you want to install?
echo "===================================================="
echo "which Apache Tomcat version do you want to install?"
echo "Install Tomcat 7,Please input 7 or press Enter"
echo "Install Tomcat 8,Please input 8"
read -p "(Please input 7 or 8):" tomcat_version

case "$tomcat_version" in
7)
echo "You will install Apache Tomcat 7.0.57"
tomcat_version="7.0.57"
;;
8)
echo "You will install Apache Tomcat 8.0.18"
tomcat_version="8.0.18"
;;
*)
echo "INPUT error,You will install Apache Tomcat 7.0.57"
tomcat_version="7.0.57"
esac

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
echo "Press any key to start...or Press Ctrl+c to cancel"
char=`get_char`

function initInstall()
{
	cat /etc/issue
	uname -a
	MemTotal=`free -m | grep Mem | awk '{print  $2}'`  
	echo -e "\n Memory is: ${MemTotal} MB "
	#Set timezone
	rm -rf /etc/localtime
	ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

	yum install -y ntp
	ntpdate -u pool.ntp.org
	date

	rpm -qa|grep httpd
	rpm -e httpd
	rpm -qa|grep mysql
	rpm -e mysql

	yum -y remove httpd*
	yum -y remove mysql-server mysql mysql-libs

	yum -y install yum-fastestmirror
	yum -y remove httpd
	#yum -y update

	#Disable SeLinux
	if [ -s /etc/selinux/config ]; then
	sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
	fi

	cp /etc/yum.conf /etc/yum.conf.lnmt
	sed -i 's:exclude=.*:exclude=:g' /etc/yum.conf

	for packages in patch make cmake gcc gcc-c++ gcc-g77 file libtool libtool-libs kernel-devel curl curl-devel openssl openssl-devel vim-minimal nano fonts-chinese gettext gettext-devel unzip ncurses ncurses-devel;
	do yum -y install $packages; done

	mv -f /etc/yum.conf.lnmt /etc/yum.conf
}

function checkAndDownloadFiles()
{
echo "============================Check files=================================="
if [ -d $files_dir ]; then
  echo "files folder [found]"
  else
  echo "Error: files folder not found!!!create it now......"
  mkdir $files_dir
fi
cd $files_dir
if [ -s pcre-$pcre_version.tar.gz ]; then
  echo "pcre-$pcre_version.tar.gz [found]"
  else
  echo "Error: pcre-$pcre_version.tar.gz not found!!!download now......"
  wget -c http://lnmt.org/online/depends/pcre/pcre-$pcre_version.tar.gz
fi

if [ -s nginx-$nginx_version.tar.gz ]; then
  echo "nginx-$nginx_version.tar.gz [found]"
  else
  echo "Error: nginx-$nginx_version.tar.gz not found!!!download now......"
  wget -c http://lnmt.org/online/nginx/nginx-$nginx_version.tar.gz
fi

if [ "$is_install_mysql55" = "y" ]; then
	if [ -s mysql-$mysql_version.tar.gz ]; then
	  echo "mysql-$mysql_version.tar.gz [found]"
	  else
	  echo "Error: mysql-$mysql_version.tar.gz not found!!!download now......"
	  wget -c http://lnmt.org/online/mysql/mysql-$mysql_version.tar.gz
	fi
else 
	if [ -s mariadb-$mysql_version.tar.gz ]; then
	  echo "mariadb-$mysql_version.tar.gz [found]"
	  else
	  echo "Error: mariadb-$mysql_version.tar.gz not found!!!download now......"
	  wget -c http://lnmt.org/online/mysql/mariadb-$mysql_version.tar.gz
	fi
fi

if [ -s mysql-openssl.patch ]; then
  echo "mysql-openssl.patch [found]"
  else
  echo "Error: mysql-openssl.patch not found!!!download now......"
  wget -c http://lnmt.org/online/mysql/ext/mysql-openssl.patch
fi

if [ -s jre-$jre_version-$sys_bit.tar.gz ]; then
  echo "jre-$jre_version-$sys_bit.tar.gz [found]"
  else
  echo "Error: jre-$jre_version-$sys_bit.tar.gz not found!!!download now......"
  wget -c http://lnmt.org/online/jre/jre-$jre_version-$sys_bit.tar.gz
fi

if [ -s apache-tomcat-$tomcat_version.tar.gz ]; then
  echo "apache-tomcat-$tomcat_version.tar.gz [found]"
  else
  echo "Error: apache-tomcat-$tomcat_version.tar.gz not found!!!download now......"
  wget -c http://lnmt.org/online/apache/apache-tomcat-$tomcat_version.tar.gz
fi

#check demo files
if [ -s web.zip ]; then
  echo "web.zip [found]"
  else
  echo "Error: web.zip not found!!!download now......"
  wget -c http://lnmt.org/online/web/web.zip
fi

#check service script files
if [ -d $script_dir ]; then
  echo "script folder [found]"
  else
  echo "Error: script folder not found!!!create it now......"
  mkdir $script_dir
fi

cd $script_dir
if [ -s lnmt ]; then
  echo "lnmt shell script [found]"
  else
  echo "Error: lnmt shell script not found!!!download now......"
  wget -c http://lnmt.org/online/script/lnmt
fi

if [ -s init.d.nginx ]; then
  echo "init.d.nginx [found]"
  else
  echo "Error: init.d.nginx not found!!!download now......"
  wget -c http://lnmt.org/online/script/init.d.nginx
fi

if [ -s init.d.tomcat ]; then
  echo "init.d.tomcat [found]"
  else
  echo "Error: init.d.tomcat not found!!!download now......"
  wget -c http://lnmt.org/online/script/init.d.tomcat
fi

#check config files
if [ -d $conf_dir ]; then
  echo "script folder [found]"
  else
  echo "Error: script folder not found!!!create it now......"
  mkdir $conf_dir
fi

cd $conf_dir
if [ -s tomcat.$tomcat_version.server.xml ]; then
  echo "tomcat.$tomcat_version.server.xml [found]"
  else
  echo "Error: tomcat.$tomcat_version.server.xml not found!!!download now......"
  wget -c http://lnmt.org/online/conf/tomcat.$tomcat_version.server.xml
fi
if [ -s nginx.conf ]; then
  echo "nginx.conf [found]"
  else
  echo "Error: nginx.conf not found!!!download now......"
  wget -c http://lnmt.org/online/conf/nginx.conf
fi

cd $cur_dir
echo "============================check files=================================="
}

function installMySQL55()
{
echo "============================Install MySQL $mysql_version=================================="
cd $files_dir

rm -f /etc/my.cnf
tar zxf mysql-$mysql_version.tar.gz
cd mysql-$mysql_version/
patch -p1 < $files_dir/mysql-openssl.patch
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DWITH_READLINE=1 -DWITH_SSL=system -DWITH_ZLIB=system -DWITH_EMBEDDED_SERVER=1 -DENABLED_LOCAL_INFILE=1
make && make install

groupadd mysql
useradd -s /sbin/nologin -M -g mysql mysql

cp support-files/my-medium.cnf /etc/my.cnf
sed '/skip-external-locking/i\datadir = /usr/local/mysql/var' -i /etc/my.cnf
if [ $install_innodb = "y" ]; then
sed -i 's:#innodb:innodb:g' /etc/my.cnf
sed -i 's:/usr/local/mysql/data:/usr/local/mysql/var:g' /etc/my.cnf
else
sed '/skip-external-locking/i\default-storage-engine=MyISAM\nloose-skip-innodb' -i /etc/my.cnf
fi

/usr/local/mysql/scripts/mysql_install_db --defaults-file=/etc/my.cnf --basedir=/usr/local/mysql --datadir=/usr/local/mysql/var --user=mysql
chown -R mysql /usr/local/mysql/var
chgrp -R mysql /usr/local/mysql/.
cp support-files/mysql.server /etc/init.d/mysql
chmod 755 /etc/init.d/mysql

cat > /etc/ld.so.conf.d/mysql.conf<<EOF
/usr/local/mysql/lib
/usr/local/lib
EOF
ldconfig

ln -s /usr/local/mysql/lib/mysql /usr/lib/mysql
ln -s /usr/local/mysql/include/mysql /usr/include/mysql
if [ -d "/proc/vz" ];then
ulimit -s unlimited
fi
/etc/init.d/mysql start

ln -s /usr/local/mysql/bin/mysql /usr/bin/mysql
ln -s /usr/local/mysql/bin/mysqldump /usr/bin/mysqldump
ln -s /usr/local/mysql/bin/myisamchk /usr/bin/myisamchk
ln -s /usr/local/mysql/bin/mysqld_safe /usr/bin/mysqld_safe

/usr/local/mysql/bin/mysqladmin -u root password $mysql_root_pwd

cat > /tmp/mysql_sec_script<<EOF
use mysql;
update user set password=password('$mysql_root_pwd') where user='root';
delete from user where not (user='root') ;
delete from user where user='root' and password=''; 
drop database test;
DROP USER ''@'%';
flush privileges;
EOF

/usr/local/mysql/bin/mysql -u root -p$mysql_root_pwd -h localhost < /tmp/mysql_sec_script

rm -f /tmp/mysql_sec_script

/etc/init.d/mysql restart
/etc/init.d/mysql stop

cd $cur_dir
echo "============================MySQL $mysql_version install completed========================="
}

function installMariaDB()
{
echo "============================Install MariaDB $mysql_version=================================="
cd $files_dir

rm -f /etc/my.cnf
tar zxf mariadb-$mysql_version.tar.gz
cd mariadb-$mysql_version/
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mariadb -DWITH_ARIA_STORAGE_ENGINE=1 -DWITH_XTRADB_STORAGE_ENGINE=1 -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DWITH_MYISAM_STORAGE_ENGINE=1 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DWITH_READLINE=1 -DWITH_SSL=system -DWITH_ZLIB=system -DWITH_EMBEDDED_SERVER=1 -DENABLED_LOCAL_INFILE=1
make && make install

groupadd mariadb
useradd -s /sbin/nologin -M -g mariadb mariadb

cp support-files/my-medium.cnf /etc/my.cnf
sed '/skip-external-locking/i\pid-file = /usr/local/mariadb/var/mariadb.pid' -i /etc/my.cnf
sed '/skip-external-locking/i\log_error = /usr/local/mariadb/var/mariadb.err' -i /etc/my.cnf
sed '/skip-external-locking/i\basedir = /usr/local/mariadb' -i /etc/my.cnf
sed '/skip-external-locking/i\datadir = /usr/local/mariadb/var' -i /etc/my.cnf
sed '/skip-external-locking/i\user = mariadb' -i /etc/my.cnf
if [ $install_innodb = "y" ]; then
sed -i 's:#innodb:innodb:g' /etc/my.cnf
sed -i 's:/usr/local/mariadb/data:/usr/local/mariadb/var:g' /etc/my.cnf
else
sed '/skip-external-locking/i\default-storage-engine=MyISAM\nloose-skip-innodb' -i /etc/my.cnf
fi

/usr/local/mariadb/scripts/mysql_install_db --defaults-file=/etc/my.cnf --basedir=/usr/local/mariadb --datadir=/usr/local/mariadb/var --user=mariadb
chown -R mariadb /usr/local/mariadb/var
chgrp -R mariadb /usr/local/mariadb/.
cp support-files/mysql.server /etc/init.d/mariadb
chmod 755 /etc/init.d/mariadb

cat > /etc/ld.so.conf.d/mariadb.conf<<EOF
/usr/local/mariadb/lib
/usr/local/lib
EOF
ldconfig

if [ -d "/proc/vz" ];then
ulimit -s unlimited
fi
/etc/init.d/mariadb start

ln -s /usr/local/mariadb/bin/mysql /usr/bin/mysql
ln -s /usr/local/mariadb/bin/mysqldump /usr/bin/mysqldump
ln -s /usr/local/mariadb/bin/myisamchk /usr/bin/myisamchk
ln -s /usr/local/mariadb/bin/mysqld_safe /usr/bin/mysqld_safe

/usr/local/mariadb/bin/mysqladmin -u root password $mysql_root_pwd

cat > /tmp/mariadb_sec_script<<EOF
use mysql;
update user set password=password('$mysql_root_pwd') where user='root';
delete from user where not (user='root') ;
delete from user where user='root' and password=''; 
drop database test;
DROP USER ''@'%';
flush privileges;
EOF

/usr/local/mariadb/bin/mysql -u root -p$mysql_root_pwd -h localhost < /tmp/mariadb_sec_script

rm -f /tmp/mariadb_sec_script

/etc/init.d/mariadb restart
/etc/init.d/mariadb stop

cd $cur_dir
echo "============================MariaDB $mysql_version install completed========================="
}

function installNginx()
{
echo "============================Install Nginx================================="
groupadd www
useradd -s /sbin/nologin -g www www
cd $files_dir
tar zxf pcre-$pcre_version.tar.gz
cd pcre-$pcre_version/
./configure
make && make install
cd ../

ldconfig

tar zxf nginx-$nginx_version.tar.gz
cd nginx-$nginx_version/
./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-ipv6
make && make install
cd ../

ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx

rm -f /usr/local/nginx/conf/nginx.conf
cd $conf_dir
cp nginx.conf /usr/local/nginx/conf/nginx.conf

cd $script_dir
cp vhost.sh /root/vhost.sh
chmod +x /root/vhost.sh

mkdir -p /home/webroot/default
chmod +w /home/webroot/default
mkdir -p /home/weblogs
chmod 777 /home/weblogs

cd $cur_dir
}

function installJRE()
{
	cd $files_dir
	tar -zxvf jre-$jre_version-$sys_bit.tar.gz -C /usr/local/
	mv -f /usr/local/$jre_tar_dir /usr/local/jre
	/usr/local/jre/bin/java -version
}

function installTomcat()
{
	cd $files_dir
	tar -zxvf apache-tomcat-$tomcat_version.tar.gz -C /usr/local/
	mv -f /usr/local/apache-tomcat-$tomcat_version /usr/local/tomcat
	cd $conf_dir
	cp -rf tomcat.$tomcat_version.server.xml /usr/local/tomcat/conf/server.xml
}

function initDemoRoot()
{
	cd $files_dir
	unzip web.zip -d /home/webroot/default
	cd $cur_dir
}

function addAndStartup()
{
	echo "============================add nginx&tomcat&mysql on startup============================"
	cp $script_dir/lnmt /root/lnmt
	chmod +x /root/lnmt
	
	cp $script_dir/init.d.nginx /etc/init.d/nginx
	chmod +x /etc/init.d/nginx

	chkconfig --level 345 nginx on
	
	cp $script_dir/init.d.tomcat /etc/init.d/tomcat
	chmod +x /etc/init.d/tomcat

	chkconfig --level 345 tomcat on
	
	if [ "$is_install_mysql55" = "md" ]; then
		chkconfig --level 345 mariadb on
	else
		chkconfig --level 345 mysql on
	fi

	if [ "$is_install_mysql55" = "md" ]; then
		sed -i 's:/etc/init.d/mysql:/etc/init.d/mariadb:g' /root/lnmt
	fi
	echo "===========================add nginx&tomcat&mysql on startup completed===================="
	
	echo "Starting LNMT..."
	if [ "$is_install_mysql55" = "md" ]; then
		/etc/init.d/mariadb start
	else
		/etc/init.d/mysql start
	fi
	/etc/init.d/nginx start
	/etc/init.d/tomcat start

	#add iptables firewall rules
	if [ -s /sbin/iptables ]; then
	/sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT
	/sbin/iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
	/sbin/iptables -I INPUT -p tcp --dport 3306 -j DROP
	/sbin/iptables-save
	fi
}

function checkInstall()
{
	echo "===================================== Check install ==================================="
	clear
	isnginx=""
	ismysql=""
	istomcat=""
	echo "Checking..."
	if [ -s /usr/local/nginx/conf/nginx.conf ] && [ -s /usr/local/nginx/sbin/nginx ]; then
	  echo "Nginx: OK"
	  isnginx="ok"
	  else
	  echo "Error: /usr/local/nginx not found!!!Nginx install failed."
	fi

	if [ "$is_install_mysql55" = "md" ]; then
		if [ -s /usr/local/mariadb/bin/mysql ] && [ -s /usr/local/mariadb/bin/mysqld_safe ] && [ -s /etc/my.cnf ]; then
		  echo "MariaDB: OK"
		  ismysql="ok"
		  else
		  echo "Error: /usr/local/mariadb not found!!!MySQL install failed."
		fi
	else
		if [ -s /usr/local/mysql/bin/mysql ] && [ -s /usr/local/mysql/bin/mysqld_safe ] && [ -s /etc/my.cnf ]; then
		  echo "MySQL: OK"
		  ismysql="ok"
		  else
		  echo "Error: /usr/local/mysql not found!!!MySQL install failed."
		fi
	fi
	
	if [ -s /usr/local/tomcat/conf/server.xml ] && [ -s /usr/local/tomcat/bin/startup.sh ]; then
	  echo "Tomcat: OK"
	  istomcat="ok"
	  else
	  echo "Error: /usr/local/tomcat not found!!!Nginx install failed."
	fi

	if [ "$isnginx" = "ok" ] && [ "$ismysql" = "ok" ]&& [ "$istomcat" = "ok" ]; then
	echo "Install LNMT 0.1 completed! enjoy it."
	echo "========================================================================="
	echo "LNMT V0.1 for CentOS/RedHat Linux Server, Written by Xiao Dong "
	echo "========================================================================="
	echo ""
	echo "For more information please visit http://lnmt.org/"
	echo ""
	echo "lnmt status manage: /root/lnmt {start|stop|reload|restart|kill|status}"
	echo "default mysql root password:$mysql_root_pwd"
	echo "Add VirtualHost : /root/vhost.sh"
	echo ""
	echo "The path of some dirs:"
	echo "mysql dir:   /usr/local/mysql"
	echo "nginx dir:   /usr/local/nginx"
	echo "jre dir:   /usr/local/jre"
	echo "tomcat dir:   /usr/local/tomcat"
	echo "web dir :     /home/webroot/default"
	echo ""
	echo "========================================================================="
	/root/lnmt status
	netstat -ntl
	else
	echo "Sorry,Failed to install LNMT!"
	echo "Please visit http://heylinux.net feedback errors and logs."
	echo "You can download /root/lnmt-install.log from your server,and upload lnmt-install.log to LNMT Forum."
	fi
}

initInstall 2>&1 | tee /root/lnmt-install.log
checkAndDownloadFiles 2>&1 | tee -a /root/lnmt-install.log
if [ "$is_install_mysql55" = "y" ]; then
	installMySQL55 2>&1 | tee -a /root/lnmt-install.log
else
	installMariaDB 2>&1 | tee -a /root/lnmt-install.log
fi
installNginx 2>&1 | tee -a /root/lnmt-install.log
installJRE  2>&1 | tee -a /root/lnmt-install.log
installTomcat  2>&1 | tee -a /root/lnmt-install.log
initDemoRoot 2>&1 | tee -a /root/lnmt-install.log
addAndStartup 2>&1 | tee -a /root/lnmt-install.log
checkInstall 2>&1 | tee -a /root/lnmt-install.log
