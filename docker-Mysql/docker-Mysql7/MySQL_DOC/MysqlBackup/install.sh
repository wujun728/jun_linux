#!/bin/bash
#Author: QingFeng
#Update Date: 2014-12-15 
#My Blog: http://my.oschina.net/pwd/blog

PWD=$(pwd $0)
pks=$PWD/packages
pksbud=$PWD/packages/build
sms=sms_install.tar.gz
smsdirname=$(echo  $sms|sed  's/.tar.gz//')
init_conf=$PWD/packages/conf
mydumpergz=mydumper-0.5.2.tar.gz
xtrabackgz=$PWD/packages/percona-xtrabackup-2.1.6-702.rhel5.x86_64.rpm
mydumperdir=$(echo  $mydumpergz|sed  's/.tar.gz//')


datef() { date "+%Y/%m/%d %H:%M" ; }
print_log() { echo "[$(datef)] $1" ; }
###查看并设置服务器编码为UTF-8
check_charaset=$(echo $LANG |grep -i utf-8 )
if [[ ! -n $check_charaset   ]];then
export LANG=$check_charaset.UTF-8
fi 

###安装短信报警
sms_install()
{
if [[ ! -f  /usr/local/bin/sendsmspost.pl  ]];then
cd  $pks
tar -zxf $sms -C $pksbud
cd  $pksbud/$smsdirname
/bin/bash install.sh
fi  
}

###初始化数据库备份目录
# define directory
init_dir()
{
print_log "开始初始化数据库备份目录."
ROOT=/data/bw_mon/bw_mysqlbk
LOG=$ROOT/log
RUN=$ROOT/run
LOCAL_DATA=$ROOT/local_data
CONF=$ROOT/conf

if [[ -d $ROOT  ]];then
print_log "$ROOT 该目录已经存在.开始备份并移除该目录..."
mv $ROOT  /data/bw_mon/bw_mysqlbk_bak_`date -I`
print_log "移除完成,备份目录为:/data/bw_mon/bw_mysqlbk_bak_`date -I` ."
fi


[[ -d $ROOT ]] ||  mkdir -p $ROOT
[[ -d $LOG  ]]  || mkdir -p $LOG
[[ -d $RUN  ]]  || mkdir -p $RUN
[[ -d $LOCAL_DATA ]] || mkdir -p $LOCAL_DATA
[[ -d $CONF ]]  ||  mkdir -p $CONF

cp $init_conf/*  $CONF 
cp $PWD/bw_mysqlbk.sh  $ROOT
cp $PWD/imexport.sh  $ROOT
print_log "初始化数据库备份目录完成."
}

###安装mydumper多线程备份
install_mydumper()
{
check_cmake=$(cmake --help)
if [[ $? -ne 0  ]] ;then
print_log "开始安装Cmake编译环境."
yum install cmake -y
fi 
if [[ ! -f /usr/local/bin/mydumper  ]];then 
print_log "开始安装mydumper多线程备份."
cd  $pks
tar -zxf $mydumpergz -C $pksbud
cd  $pksbud/$mydumperdir

if [[ -f CMakeCache.txt  ]];then
rm -f CMakeCache.txt
fi 
yum install pcre -y 

cmake .
make && make install
print_log "安装mydumper多线程备份完成." 
else
print_log "mydumper多线程备份已经安装."
fi


}

###安装xtrabackup备份
install_xtra()
{
if [[ ! -f /usr/bin/innobackupex  ]];then
print_log "开始安装xtrabackup备份."
yum localinstall  $xtrabackgz  -y --nogpgcheck
#cd /tmp
#wget http://www.percona.com/redir/downloads/XtraBackup/LATEST/RPM/rhel5/x86_64/percona-xtrabackup-2.1.6-702.rhel5.x86_64.rpm
#yum localinstall  percona-xtrabackup-2.1.6-702.rhel5.x86_64.rpm   -y –nogpgcheck  
print_log "安装xtrabackup备份完成."
else
print_log "xtrabackup已经安装."
fi
}

init_dir
install_xtra
install_mydumper
sms_install
print_log  "所有安装都已经完成!!"
