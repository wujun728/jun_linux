#!/usr/bin/env bash

# Program: MySQL 增量备份脚本 使用 percona xtrabackup
# Author : yaoy
# Date   : 2016-08-01


# 读取配置文件中的所有变量值, 设置为全局变量
# 配置文件
# mysql 备份目录
#backup_dir=`sed '/^backup_dir=/!d;s/.*=//' $conf_file`
backup_dir=$BACKUP_DIR/$POD_NAME
conf_file="$backup_dir/conf/mysql_increment_hot_backup.conf"
# mysql 用户
user=`sed '/^user=/!d;s/.*=//' $conf_file`
# mysql 密码
password=`cat /config-center/ln/MYSQL_ROOT_PASSWORD`
#password=`sed '/^password=/!d;s/.*=//' $conf_file`
# percona-xtrabackup 备份软件路径
xtrabackup_dir=`sed '/^xtrabackup_dir=/!d;s/.*=//' $conf_file`
# 全备是在一周的第几天
#full_backup_week_day=`sed '/^full_backup_week_day=/!d;s/.*=//' $conf_file`
# mysql 全备前缀标识
full_backup_prefix=`sed '/^full_backup_prefix=/!d;s/.*=//' $conf_file`
# mysql 增量备前缀标识
increment_prefix=`sed '/^increment_prefix=/!d;s/.*=//' $conf_file`
# mysql 配置文件
mysql_conf_file=`sed '/^mysql_conf_file=/!d;s/.*=//' $conf_file`
# 备份错误日志文件
error_log=$backup_dir`sed '/^error_log=/!d;s/.*=//' $conf_file`
# 备份索引文件
index_file=$backup_dir`sed '/^index_file=/!d;s/.*=//' $conf_file`
# 备份指定表
backtables=$BACK_TABLES
#backtables=`sed '/^back_tables=/!d;s/.*=//' $conf_file`

# 备份日期
backup_date=`date +%F`
# 备份日期
backup_time=`date +%H-%M-%S`
# 备份日期
#backup_week_day=`date +%u`

# 创建相关目录
log_dir=$backup_dir/log
var_dir=$backup_dir/var
mkdir -p $backup_dir
mkdir -p $log_dir
mkdir -p $var_dir


# 全量备份
function full_backup() {
  backup_folder=${full_backup_prefix}_${backup_date}_${backup_time}
  #_${backup_week_day}

  mkdir -p $backup_dir/$backup_folder
  if [ ! -n "$backtables" ]; then
    $xtrabackup_dir/bin/innobackupex \
      --defaults-file=$mysql_conf_file \
      --user=$user \
      --password=$password \
      --no-timestamp \
      $backup_dir/$backup_folder > $log_dir/${backup_folder}.log 2>&1
  else
    $xtrabackup_dir/bin/innobackupex \
      --defaults-file=$mysql_conf_file \
      --user=$user \
      --password=$password \
      --databases="$backtables" \
      --no-timestamp \
      $backup_dir/$backup_folder > $log_dir/${backup_folder}.log 2>&1
  fi
  
  return $?
}

# 增量备份
function increment_backup() {
  backup_folder=${increment_prefix}_${backup_date}_${backup_time}
  #_${backup_week_day}
  incr_base_folder=`sed -n '$p' $index_file | \
                   awk -F '[, {}]*' '{print $2}' | \
                   awk -F ':' '{print $2}'`

  mkdir -p $backup_dir/$backup_folder
  if [ ! -n "$backtables" ]; then
    $xtrabackup_dir/bin/innobackupex \
      --defaults-file=$mysql_conf_file \
      --user=$user \
      --password=$password \
      --no-timestamp \
      --incremental \
      $backup_dir/$backup_folder \
      --incremental-basedir=$backup_dir/$incr_base_folder > $log_dir/${backup_folder}.log 2>&1
  else
    $xtrabackup_dir/bin/innobackupex \
      --defaults-file=$mysql_conf_file \
      --user=$user \
      --password=$password \
      --databases="$backtables" \
      --no-timestamp \
      --incremental \
      $backup_dir/$backup_folder \
      --incremental-basedir=$backup_dir/$incr_base_folder > $log_dir/${backup_folder}.log 2>&1
  fi


  return $?
}

# 删除之前的备份(一般在全备完成后使用)
function delete_before_backup() {
  cat $index_file | awk -F '[, {}]*' '{print $2}' | \
    awk -v backup_dir=$backup_dir -F ':' '{if($2!=""){printf("rm -rf %s/%s\n", backup_dir, $2)}}' | \
    /bin/bash
  
  cat $index_file | awk -F '[, {}]*' '{print $2}' | \
    awk -v log_dir=$log_dir -F ':' '{if($2!=""){printf("rm -rf %s/%s.log\n", log_dir, $2)}}' | \
    /bin/bash
}

# 备份索引文件
function backup_index_file() {
  cp $index_file ${index_file}_$(date -d "1 day ago" +%F)
}

# 备份索引文件
function send_index_file_to_remote() {
  echo 'send index file ok'
}

# 添加索引, 索引记录了当前最新的备份
function append_index_to_file() {
#  echo "{week_day:$backup_week_day, \
#  dir:${1}_${backup_date}_${backup_time}_${backup_week_day}, \
  echo "{dir:${1}_${backup_date}_${backup_time}, \
         type:${1}, \
         date:${backup_date}}" >> $index_file
}

# 记录 错误消息到文件
function logging_backup_err() {
#  echo "{week_day:$backup_week_day, \
#dir:${1}_${backup_date}_${backup_time}_${backup_week_day}, \
  echo "{dir:${1}_${backup_date}_${backup_time}, \
         type:${1}, \
         date:${backup_date}}" >> $error_log
}

# 清空索引
function purge_index_from_file() {
  > $index_file
}

# 清空错误日志信息
function purge_err_log() {
  > $error_log
}

# 打包备份
function tar_backup_file() {
  echo "tar $1 ok"
}

# 发送备份到远程
function send_backup_to_remote() {
  echo "send $1 remote ok"
}
 
# 判断是应该全备还是增量备份
# 0:full, 1:incr
function get_backup_type() {
#  full_backup_week_day=`sed '/^full_backup_week_day=/!d;s/.*=//' $conf_file`
  last_full_backup_day=`sed '/^last_full_backup_day=/!d;s/.*=//' $conf_file`
  backup_type=1
#  if [ "$full_backup_week_day" -eq `date +%u` ]; then
#    backup_type=0
#  else
#    backup_type=1
#  fi

  if [ "$last_full_backup_day"x = `date +%F`x ]; then
    backup_type=1
  else
    backup_type=0
  fi

  if [ ! -n "`cat $index_file`" ]; then
    backup_type=0
  fi
  return $backup_type
}

# 测试配置文件正确性
function test_conf_file() {
  # 判断每个变量是否在配置文件中有配置，没有则退出程序
  if [ ! -n "$user" ]; then echo 'fail: configure file user not set'; exit 2; fi
  if [ ! -n "$password" ]; then echo 'fail: env root password not set'; exit 2; fi
  if [ ! -n "$backup_dir" ]; then echo 'fail: env BACKUP_DIR not set'; exit 2; fi
#  if [ ! -n "$full_backup_week_day" ]; then echo 'fail: configure file full_backup_week_day not set'; exit 2; fi
  if [ ! -n "$full_backup_prefix" ]; then echo 'fail: configure file full_backup_prefix not set'; exit 2; fi
  if [ ! -n "$increment_prefix" ]; then echo 'fail: configure file increment_prefix not set'; exit 2; fi
  if [ ! -n "$mysql_conf_file" ]; then echo 'fail: configure file mysql_conf_file not set'; exit 2; fi
  if [ ! -n "$error_log" ]; then echo 'fail: configure file error_log not set'; exit 2; fi
  if [ ! -n "$index_file" ]; then echo 'fail: configure file index_file not set'; exit 2; fi
  if [ ! -n "$POD_NAME" ]; then echo 'fail: env POD_NAME not set'; exit 2; fi
}

# 执行
function run() {
  # 检测配置文件值
  test_conf_file

  # 判断是执行全备还是曾量备份
  get_backup_type
  backup_type=$?
  case $backup_type in
    0 )
      # 全量备份
      full_backup 
      backup_ok=$?
      if [ 0 -eq "$backup_ok" ]; then
      # 全备成功
        # # 打包最新备份
        # tar_backup_file $full_backup_prefix
        # # 将tar备份发送到远程
        # send_backup_to_remote $full_backup_prefix
        # 备份索引文件
        backup_index_file
        # # 发送索引文件到远程
        # send_index_file_to_remote
        # 清除之前的备份
        delete_before_backup
        # 清除索引文件
        purge_index_from_file
        # 添加索引, 索引记录了当前最新的备份
        append_index_to_file $full_backup_prefix
	# 修改上一次成功备份的日期
	sed -i  "s#last_full_backup_day=.*#last_full_backup_day=$backup_date#" $conf_file
      else
      # 全备失败
        # 删除备份目录
        rm -rf ${backup_dir}/${full_backup_prefix}_${backup_date}_${backup_time}
	#_${backup_week_day}
        # 记录错误日志
        logging_backup_err $full_backup_prefix
      fi
      ;;
    1 )
      # 增量备份
      increment_backup
      backup_ok=$?
      if [ 0 -eq "$backup_ok" ]; then
      # 增量备份成功
        # # 打包最新备份
        # tar_backup_file $increment_prefix
        # # 将tar备份发送到远程
        # send_backup_to_remote $increment_prefix
        # 添加索引, 索引记录了当前最新的备份
        append_index_to_file $increment_prefix
      else
      # 增量备份失败
        # 删除备份目录
        rm -rf ${backup_dir}/${full_backup_prefix}_${backup_date}_${backup_time}
	#_${backup_week_day}
        # 记录错误日志
        logging_backup_err $increment_prefix
      fi
      ;;
  esac
}

run
