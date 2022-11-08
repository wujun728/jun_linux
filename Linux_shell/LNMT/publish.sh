#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to publish LNMT"
    exit 1
fi

clear
echo "========================================================================="
echo "LNMT publish application for CentOS/RedHat Linux Server, Written by Xiao Dong"
echo "========================================================================="
echo "A tool to auto-compile & install Nginx + MySQL + JRE + Tomcat on Linux "
echo ""
echo "For more information please visit http://lnmt.org/"
echo "========================================================================="

cur_dir=$(pwd)

echo "========================================"

pub_ver="alpha"
echo "Please input the publish version of lnmt(alpha, beta, rc or release):"
read -p "(Default version: alpha):" pub_ver
if [ "$pub_ver" = "" ]; then
	pub_ver="alpha"
fi
echo "==========================="
echo "Publish version:$pub_ver"
echo "==========================="

app_ver="alpha"
echo "Please input the application version of lnmt:"
read -p "(Default version: 0.1):" app_ver
if [ "$app_ver" = "" ]; then
	app_ver="0.1"
fi
echo "==========================="
echo "Public version:$app_ver"
echo "==========================="

build_dir=$cur_dir/lnmt/build
app_dir=$build_dir/lnmt-full-$pub_ver-$app_ver
files_dir=$app_dir/files
conf_dir=$app_dir/conf
script_dir=$app_dir/script
publish_dir=$cur_dir/lnmt/$pub_ver

echo "Checking publish available..."
if [ -s $publish_dir/lnmt-full-$pub_ver-$app_ver.tar.gz ]; then
  echo "[ERROR]The $pub_ver version with application version $app_ver has already published, delete it if unuseable."
  exit 0
  else
  echo "Status: OK."
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
echo "Press any key to start...or Press Ctrl+c to cancel"
char=`get_char`

# also can be folder
is_local=n
site="http://lnmt.org"

site_online=$site/online
ol_shell=$site_online/shell
ol_apache=$site_online/apache
ol_conf=$site_online/conf
ol_depends=$site_online/depends
ol_jre=$site_online/jre
ol_mysql=$site_online/mysql
ol_nginx=$site_online/nginx
ol_script=$site_online/script
ol_web=$site_online/web

# ------- shell folder -------
shell_centos_sh=$ol_shell/centos.sh
shell_proftpd_sh=$ol_shell/proftpd.sh
shell_reset_mysql_root_password_sh=$ol_shell/reset_mysql_root_password.sh
shell_LICENSE=$ol_shell/LICENSE
shell_proftpd_vhost_sh=$ol_shell/proftpd_vhost.sh
shell_uninstall_sh=$ol_shell/uninstall.sh
# ------- apache folder -------
apache_tomcat7=$ol_apache/apache-tomcat-7.0.57.tar.gz
apache_tomcat8=$ol_apache/apache-tomcat-8.0.18.tar.gz
# ------- conf folder -------
conf_nginx=$ol_conf/nginx.conf
conf_tomcat7_xml=$ol_conf/tomcat.7.0.57.server.xml
conf_tomcat8_xml=$ol_conf/tomcat.8.0.18.server.xml
# ------- depends folder -------
depends_pcre=$ol_depends/pcre/pcre-8.12.tar.gz
# ------- jre folder -------
jre_7x64=$ol_jre/jre-7u75-x64.tar.gz
jre_7x86=$ol_jre/jre-7u75-x86.tar.gz
jre_8x64=$ol_jre/jre-8u31-x64.tar.gz
jre_8x86=$ol_jre/jre-8u31-x86.tar.gz
# ------- mysql folder -------
mysql_ext_openssl=$ol_mysql/ext/mysql-openssl.patch
mysql_mariadb=$ol_mysql/mariadb-5.5.37.tar.gz
mysql_mysql=$ol_mysql/mysql-5.5.37.tar.gz
# ------- nginx folder -------
nginx_nginx=$ol_nginx/nginx-1.7.9.tar.gz
# ------- script folder -------
script_nginx=$ol_script/init.d.nginx
script_proftpd=$ol_script/init.d.proftpd
script_tomcat=$ol_script/init.d.tomcat
script_lnmt=$ol_script/lnmt
# ------- web folder -------
web_root=$ol_web/web.zip

function download()
{	
	if [ -d $files_dir ]; then
	  echo "files folder [founded]"
	  else
	  echo "files folder not found!!!create it now......"
	  mkdir -p $files_dir
	fi
	
	if [ -d $conf_dir ]; then
	  echo "conf folder [founded]"
	  else
	  echo "conf folder not found!!!create it now......"
	  mkdir -p $conf_dir
	fi
	
	if [ -d $script_dir ]; then
	  echo "script folder [founded]"
	  else
	  echo "script folder not found!!!create it now......"
	  mkdir -p $script_dir
	fi

	# download install script to app folder
	cd $app_dir
	if [ $is_local = "y" ]; then
	cp -rf $shell_centos_sh							$app_dir
	cp -rf $shell_proftpd_sh						$app_dir
	cp -rf $shell_reset_mysql_root_password_sh		$app_dir
	cp -rf $shell_LICENSE							$app_dir
	cp -rf $shell_proftpd_vhost_sh					$app_dir
	cp -rf $shell_uninstall_sh						$app_dir
	else
	wget -c $shell_centos_sh						
	wget -c $shell_proftpd_sh					
	wget -c $shell_reset_mysql_root_password_sh	
	wget -c $shell_LICENSE						
	wget -c $shell_proftpd_vhost_sh				
	wget -c $shell_uninstall_sh					
	fi
	
	# download files to files folder
	cd $files_dir
	if [ $is_local = "y" ]; then
	cp -rf $apache_tomcat7 		$files_dir
	cp -rf $apache_tomcat8 		$files_dir
	cp -rf $jre_7x64			$files_dir
	cp -rf $jre_7x86			$files_dir
	cp -rf $jre_8x64		 	$files_dir
	cp -rf $jre_8x86			$files_dir
	cp -rf $mysql_ext_openssl 	$files_dir
	cp -rf $mysql_mariadb 		$files_dir
	cp -rf $mysql_mysql 		$files_dir
	cp -rf $depends_pcre 		$files_dir
	cp -rf $web_root 			$files_dir
	else
	wget -c $apache_tomcat7 		
	wget -c $apache_tomcat8 		
	wget -c $jre_7x64			
	wget -c $jre_7x86			
	wget -c $jre_8x64		 	
	wget -c $jre_8x86			
	wget -c $mysql_ext_openssl 	
	wget -c $mysql_mariadb 		
	wget -c $mysql_mysql 		
	wget -c $depends_pcre 		
	wget -c $web_root 			
	fi
	
	# download files to conf folder
	cd $conf_dir
	if [ $is_local = "y" ]; then
	cp -rf $conf_nginx			$conf_dir
	cp -rf $conf_tomcat7_xml	$conf_dir
	cp -rf $conf_tomcat8_xml	$conf_dir
	else
	wget -c $conf_nginx			
	wget -c $conf_tomcat7_xml	
	wget -c $conf_tomcat8_xml	
	fi
	
	# download files to script folder
	cd $script_dir
	if [ $is_local = "y" ]; then
	cp -rf $script_nginx	 $script_dir
	cp -rf $script_proftpd	 $script_dir
	cp -rf $script_tomcat	 $script_dir
	cp -rf $script_lnmt		 $script_dir
	else
	wget -c $script_nginx	
	wget -c $script_proftpd	
	wget -c $script_tomcat	
	wget -c $script_lnmt		
	fi
}

function convert2unix()
{
	yum -y install dos2unix
	cd $app_dir
	dos2unix *.sh
	chmod +x *.sh
	cd $script_dir
	dos2unix *
}

function publish()
{
	cd $publish_dir
	if [ -d $publish_dir ]; then
	  echo "$publish_dir folder [found]"
	  else
	  echo "$publish_dir folder not found!!!create it now......"
	  mkdir -p $publish_dir
	fi
	cd $build_dir
	tar zcvf $publish_dir/lnmt-full-$pub_ver-$app_ver.tar.gz lnmt-full-$pub_ver-$app_ver
}

function check()
{
echo "Checking..."
if [ -s $publish_dir/lnmt-full-$pub_ver-$app_ver.tar.gz ]; then
  echo "Publish: OK"
  else
  echo "Error: $publish_dir/lnmt-full-$pub_ver-$app_ver.tar.gz not found!!!lnmt publish failed."
fi
}

download 2>&1 | tee /root/lnmt-publish.log
convert2unix 2>&1 | tee /root/lnmt-publish.log
publish 2>&1 | tee /root/lnmt-publish.log
check 2>&1 | tee /root/lnmt-publish.log