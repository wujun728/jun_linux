#/bin/bash
Date=`date +%Y_%m%d_%H%M`
standdate=`date "+%Y-%m-%d %H:%M:%S"`
ROOT=`pwd`
log=$ROOT/log/$Date.log
mysqldump_cmd="--default-character-set=utf8 --max_allowed_packet=1048576 --net_buffer_length=16384"
mysql_cmd="--default-character-set=utf8 --max_allowed_packet=1048576 --net_buffer_length=16384"
import_tmp=$ROOT/import_tmp
export_tmp=$ROOT/export_tmp

prepare()
{
[[ -d $log ]] || mkdir -p $ROOT/log/
[[ -d $import_tmp/$Date ]] || mkdir -p  $import_tmp/$Date
[[ -d $export_tmp/$Date ]] || mkdir -p  $export_tmp/$Date

echo "请在脚本所在目录执行脚本,导入的sql文件请放在同目录下."
read -p  "请输入需要导入/导出的数据库:	"  databases
read -p  "请输入该数据库的root密码:  "  password
}

run_action()
{


if ! mysql -uroot -p"$password" -e "show databases " --batch | grep "\<$databases\>" > /dev/null 2>&1
then 
echo "开始日期: $standdate"
echo "数据库:$databases 不存在,退出数据操作，请确认是否存在该数据库或者是否输错该数据名和密码."
echo "开始日期: $standdate" >> $log
echo "数据库:$databases 不存在,退出数据操作，请确认是否存在该数据库或者是否输错该数据名和密码." >> $log
exit
fi 


echo "开始日期: $standdate"
echo "导入/导出的数据库为:$databases" 
echo "导入/导出的sql文件为:$sql"
echo "开始日期: $standdate" >> $log
echo "导入/导出的数据库为:$databases"   >> $log
echo "导入/导出的sql文件为:$sql"   >> $log

sleep 3

date_start=`date +%s`

runcmd1
if [[ $?  -eq 0 ]];then 

sqlsize=`du -sh $sql |awk '{print $1}'`

echo "$databases 数据导入/导出,成功.!导入/出的文件或目录为$sql,其大小为$sqlsize!"
echo "$databases 数据导入/导出,成功.!导入/出的文件或目录为$sql,其大小为$sqlsize!"  >> $log
else 
echo "$databases 数据导入/导出,失败,退出!"
echo "$databases 数据导入/导出,失败,退出!" >> $log
exit
fi

#mysqldump  -uroot -p"$password" --log-error=$log $mysqldump_cmd $databases > $sql
#mysql  -uroot -p"$password" --log-error=$log $mysql_cmd $databases <  $sql

date_end=`date +%s`
time_take=$(($date_end - $date_start))
time_take1=$(($time_take / 3600 ))

echo "开始:$date_start 结束：$date_end"
echo "总共耗时:$time_take 秒 / $time_take1 小时"

echo "开始:$date_start 结束：$date_end"   >> $log
echo "总共耗时:$time_take 秒 / $time_take1 小时"  >>  $log
}


import_action()
{
[[ -d $ROOT/log/ ]] || mkdir -p $ROOT/log/
echo  "开始准备从本地导入数据......"
echo  "初始化配置......"
echo  "开始准备从本地导入数据......" >  $log
echo  "初始化配置......"  >>  $log
sleep 1
###函数 
prepare
read -p "请输入导入数据库的.sql文件/tar.gz压缩包/sql文件夹/xtrabackup文件夹,请填写绝对路径:  " sql_file
sqlfilename=`echo $sql_file |awk -F'/' '{print $NF}'`
sqlnum=`echo $sqlfilename |grep "sql$" |wc -l`
sqlnum1=`echo $sqlfilename |grep "tar.gz$" |wc -l`
sql_file_size=`du -sh $sql_file |awk '{print $1}'`
echo "导入数据库的文件或目录的大小为: $sql_file_size"
echo "导入数据库的文件或目录的大小为: $sql_file_size"  >> $log

###导入数据为单个sql文件
if [[ $sqlnum -eq 1 ]] ;then
echo "导入数据库的文件为单个.sql文件.导入方式为: mysql"
echo "导入数据库的文件为单个.sql文件." >>  $log
sql=$sql_file
runcmd1(){
echo "请选择从本地数据导入到本地的方式:"
echo "1.mysql --default-character-set=utf8 "
echo "2.mysql  $mysql_cmd"
echo "3.other"
read -p "请选择以上4种方式的一种(写序号即可)：  "   choice
case $choice in
1)

mysql  -uroot -p"$password"  --default-character-set=utf8 $databases <  $sql

;;
2)

mysql  -uroot -p"$password"  $mysql_cmd $databases <  $sql
;;
3)
read -p "请输入其他导入数据的方式,格式如下：
/usr/bin/mysql  -uroot -p"$password"  --default-character-set=utf8 "$databases" <  "$sql"
请输入: "  cmdread

$cmdread

;;
esac
}
###函数 
run_action
echo "数据导入方式为:mysql" >> $log
exit
fi

###导入数据为压缩文件，自动解压tar后对文件类型进行判断
###暂时只添加了对mydumper多线程备份进行导入操作
if [[ $sqlnum1 -eq 1  ]];then
echo "导入数据库的文件为.tar.gz文件."
echo "开始解压缩文件......"
echo "导入数据库的文件为.tar.gz文件." >>  $log
echo "开始解压缩文件......"  >>  $log
tar -zxf  $sql_file  -C  $import_tmp/$Date
echo "解压的文件在: $import_tmp/$Date"
echo "解压的文件在: $import_tmp/$Date"  >>  $log
read -p "请重新输入导入数据库的源目录/源sql文件/解压后:  " sql_file1
sql=$sql_file1
fi

if [[ -d $sql_file1   ]];then 
cd $sql_file1 
dumper=`ls |grep "schema.sql$" |wc -l`
if [[ $dumper -ne 0  ]];then 
echo "导入数据库的文件为多个mydumper文件.导入方式为: myloader"
sql=$sql_file1
runcmd1(){
/usr/local/bin/myloader -u root -p "$password" -B  $databases  -d $sql  -o
}
###函数 
run_action
echo "数据导入方式为:myloader" >> $log
exit
fi
fi



###直接为mydumper文件
if [[ -d $sql_file   ]];then
cd $sql_file
dumper=`ls |grep "schema.sql$" |wc -l`
if [[ $dumper -ne 0  ]];then
echo "导入数据库的文件为多个mydumper文件.导入方式为: myloader"
sql=$sql_file
runcmd1(){
/usr/local/bin/myloader -u root -p "$password" -B  $databases -o -d $sql
}
###函数 
run_action
echo "数据导入方式为:myloader" >> $log
exit
fi
fi

###直接为xtrabackupex备份文件
if [[ -d $sql_file   ]];then
cd $sql_file
xtrabackup=`ls |grep "xtrabackup" |wc -l`
if [[ $xtrabackup -ne 0  ]];then
echo "导入数据库的文件为xtrabackup文件.导入方式为: innobackupex"
echo "缺省定义mysql的配置文件为:/etc/my.cnf,如若不是请手动修改!"
read -p "是否恢复一次完整备份？Y/N : "  readrestore
if [[ $readrestore == "Y"  ]] ;then
continue
else
echo "由于你选择的不是完整备份的恢复，请手动修改恢复动作,退出!"
exit

fi

sql=$sql_file
runcmd1(){
datedir=$(mysql -p"$password"  -e "show variables like 'datadir'"  --batch |grep "datadir" |awk '{print $2}')
############################################################################################################
#增量备份增加以下操作,第一次增量恢复分3个步骤
#innobackupex --apply-log --redo-only /data/mysql_backup/centos_full_backup  --user=root --password=$password
#innobackupex --apply-log --redo-only /data/mysql_backup/centos_full_backup  --incremental-dir=/data/mysql_backup/2013_1119 --user=root --password=$password
#上面是做针对完备的一次增量备份恢复的操作，如果是针对增量的增量，则添加以下操作。
#innobackupex --apply-log --redo-only /data/mysql_backup/centos_full_backup  --incremental-dir=/data/mysql_backup/2013_1120 --user=root --password=$password
#############################################################################################################
innobackupex --apply-log  $sql    --user=root --password=$password

if [[ -f /etc/init.d/mysqld ]];then
echo  "开始停止mysql......"
/etc/init.d/mysqld  stop
elif [[  -f /etc/init.d/mysql  ]];then 
echo "开始停止mysql......"
/etc/init.d/mysql  stop
fi 

if [[ $? -eq 0 ]] ;then 
cd $datedir
[[ -d /data/tmp/$Date ]] || mkdir  -p /data/tmp/$Date 
mv ./*  /data/tmp/$Date
echo "$datedir原始数据文本备份到/data/tmp/$Date目录!"

innobackupex  --copy-back --defaults-file=/etc/my.cnf  $sql 
chown mysql.mysql  $datedir -R

fi

}
###函数 
run_action
echo "数据导入方式为:innobackupex" >> $log
exit
fi
fi


}



export_action()
{
[[ -d $log ]] || mkdir -p $ROOT/log/
echo  "开始准备从本地导出数据......"
echo  "初始化配置......"
echo  "开始准备从本地导出数据......" >  $log
echo  "初始化配置......"  >>  $log
sleep 1
###调用函数
prepare

datarr=$(mysql -u"root" -p"$password" -e "show variables like 'datadir'" --batch |grep "datadir" |awk '{print $2}')
dataexsize=$(du -sh $datarr"$databases" |awk '{print $1}')

echo "该$databases数据的数据库文件大小为:$dataexsize"
echo "该$databases数据的数据库文件大小为:$dataexsize" >> $log
echo "请选择从本地数据导出到本地的方式:"
echo "1.mysqldumper --default-character-set=utf8 "
echo "2.mysqldumper $mysqldump_cmd"
echo "3.mydumper -u xxx -p 'xxx' -B XXX -o xxx"
echo "4.mydumper -u xxx -p 'xxx' -B XXX -o xxx -c"
echo "5.innobackupex --user=xxx --password=xxx --no-timestamp --defaults-file=xxx --include="" (完整备份版)"
read -p "请选择以上4种方式的一种(写序号即可)：  "   choice
case $choice in 
1)
sqldir=$export_tmp/$Date 
sql=$sqldir/$databases"_"$Date.sql
runcmd1(){
mysqldump -u"root" -p"$password" --default-character-set=utf8 --databases $databases > $sql
}
run_action
echo "数据导出方式为:msyqldump" >> $log
;;
2)
sqldir=$export_tmp/$Date
sql=$sqldir/$databases"_"$Date.sql
runcmd1(){
mysqldump -u"root" -p"$password" --default-character-set=utf8 $mysqldump_cmd --databases $databases > $sql
}
run_action
echo "数据导出方式为:msyqldump,加调优参数！" >> $log

;;
3)
sqldir=$export_tmp/$Date
sql=$sqldir/$databases"_"$Date
runcmd1(){
/usr/local/bin/mydumper -u root -p  "$password" -B $databases -o $sql
}
run_action
echo "数据导出方式为:mydumper" >> $log
;;
4)
sqldir=$export_tmp/$Date
sql=$sqldir/$databases"_"$Date
runcmd1(){
/usr/local/bin/mydumper -u root -p  "$password" -B $databases -o $sql -c
}
run_action
echo "数据导出方式为:mydumper,压缩版" >> $log
;;
5)
sqldir=$export_tmp/$Date
sql=$sqldir/$databases"_"$Date
echo "缺省定义mysql的配置文件为:/etc/my.cnf,如若不是请手动修改!"
runcmd1(){
innobackupex --user=root --password=$password --no-timestamp --defaults-file=/etc/my.cnf --include="$databases.*|mysql.*"   $sql  
}
run_action
echo "数据导出方式为:percona xtrabackup(innobackupex),完整备份版" >> $log
;;



*)
echo "请选择正确的导出方式!"
;;
esac

}

case $1 in 
import)


import_action

;;
export)

export_action

;;
*)
echo "请输入正确的字符串:import/export"

;;
esac


